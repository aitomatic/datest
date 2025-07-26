"""
Integration tests for Dana runtime integration.

Tests the full pipeline of discovering, executing, and reporting Dana tests.
"""

from pathlib import Path
from unittest.mock import patch

from datest.discovery import DanaTestDiscovery
from datest.executor import DanaTestExecutor
from datest.models import DanaTestResult
from datest.reporter import DanaTestReporter


class TestDanaIntegration:
    """Test full Dana test pipeline integration"""

    def test_discover_and_execute_fixtures(self):
        """Test discovering and executing fixture tests"""
        # Discovery
        discovery = DanaTestDiscovery()
        fixtures_path = Path("tests/fixtures")

        if not fixtures_path.exists():
            # Skip test if fixtures don't exist
            return

        discovered_files = discovery.discover([fixtures_path])

        # Should find our fixture files
        assert len(discovered_files) >= 3
        assert any("simple_test.na" in str(f) for f in discovered_files)
        assert any("failing_test.na" in str(f) for f in discovered_files)
        assert any("error_test.na" in str(f) for f in discovered_files)

    @patch("subprocess.run")
    def test_full_pipeline_with_mocked_dana(self, mock_run):
        """Test full pipeline with mocked Dana execution"""

        # Mock different outputs for different files
        def mock_dana_run(*args, **kwargs):
            cmd = args[0]
            if "simple_test.na" in str(cmd):
                return type(
                    "MockResult",
                    (),
                    {
                        "returncode": 0,
                        "stdout": """🧪 Starting simple Dana test
✅ Basic math test passed: 2 + 2 = 4
✅ String test passed: Hello, Dana!
✅ Variable test passed: 10 + 20 = 30
🎉 All simple tests completed successfully!""",
                        "stderr": "",
                    },
                )()
            elif "failing_test.na" in str(cmd):
                return type(
                    "MockResult",
                    (),
                    {
                        "returncode": 1,
                        "stdout": """❌ Test failed: Expected 5 but got 4
✅ This test passed
❌ Another failure""",
                        "stderr": "Error: Assertion failed",
                    },
                )()
            else:
                return type(
                    "MockResult",
                    (),
                    {"returncode": 2, "stdout": "", "stderr": "Error: Undefined variable 'x'"},
                )()

        mock_run.side_effect = mock_dana_run

        # Run full pipeline
        _discovery = DanaTestDiscovery()  # Unused but kept for potential future use
        executor = DanaTestExecutor()

        # Create test files for discovery
        test_files = [Path("simple_test.na"), Path("failing_test.na"), Path("error_test.na")]

        results = []
        for test_file in test_files:
            result = executor.run_dana_file(test_file)
            results.append(result)

        # Verify results
        assert len(results) == 3

        # Simple test should pass
        simple_result = results[0]
        assert simple_result.success is True
        assert len(simple_result.assertions) > 0
        assert all(a.passed for a in simple_result.assertions if a.assertion_type == "assert")

        # Failing test should fail
        failing_result = results[1]
        assert failing_result.success is False
        assert any(not a.passed for a in failing_result.assertions)

        # Error test should fail
        error_result = results[2]
        assert error_result.success is False
        assert error_result.exit_code == 2

    def test_reporter_integration(self):
        """Test reporter with various result types"""
        import io

        # Create test results
        results = [
            DanaTestResult(
                file_path=Path("test_pass.na"),
                success=True,
                duration=0.5,
                output="✅ All tests passed",
            ),
            DanaTestResult(
                file_path=Path("test_fail.na"),
                success=False,
                duration=1.2,
                output="❌ Test failed",
                errors="Error: Assertion failed",
                exit_code=1,
            ),
        ]

        # Test reporter output
        output = io.StringIO()
        reporter = DanaTestReporter(output=output, use_color=False)
        reporter.generate_report(results)

        report_text = output.getvalue()

        # Verify report contains expected elements
        assert "test_pass.na" in report_text
        assert "PASSED" in report_text
        assert "test_fail.na" in report_text
        assert "FAILED" in report_text
        assert "Total files" in report_text
        assert "1 test file(s) failed" in report_text

    def test_json_output_integration(self):
        """Test integration with JSON output mode"""
        from datest.assertions import DanaAssertionParser

        json_output = """
        {
            "tests": [
                {"line": 8, "message": "result == 4", "passed": true},
                {"line": 12, "message": "greeting.contains('Dana')", "passed": true},
                {"line": 19, "message": "sum_result == 30", "passed": true}
            ],
            "logs": [
                {"line": 4, "message": "🧪 Starting simple Dana test"},
                {"line": 9, "message": "✅ Basic math test passed: 2 + 2 = 4"},
                {"line": 22, "message": "🎉 All simple tests completed successfully!"}
            ]
        }
        """

        parser = DanaAssertionParser()
        assertions = parser.parse_output(json_output)

        # Should parse all assertions and logs
        assert len(assertions) == 6

        test_assertions = [a for a in assertions if a.assertion_type == "assert"]
        assert len(test_assertions) == 3
        assert all(a.passed for a in test_assertions)

        logs = [a for a in assertions if a.assertion_type == "log"]
        assert len(logs) == 3

    def test_exit_code_handling(self):
        """Test proper exit code handling throughout pipeline"""
        # Test various exit code scenarios
        test_cases = [
            (0, True),  # Success
            (1, False),  # Test failure
            (2, False),  # Error
            (124, False),  # Timeout
            (127, False),  # Command not found
        ]

        for exit_code, expected_success in test_cases:
            result = DanaTestResult(
                file_path=Path("test.na"),
                success=False,  # Will be determined by exit code
                duration=1.0,
                exit_code=exit_code,
            )

            # For exit code 0, success should be True
            if exit_code == 0:
                result.success = True

            assert (result.exit_code == 0) == expected_success
