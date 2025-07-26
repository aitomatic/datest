"""
Unit tests for Dana assertion parsing functionality.
"""

from datest.assertions import DanaAssertionParser
from datest.models import DanaAssertion


class TestDanaAssertionParser:
    """Test DanaAssertionParser class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.parser = DanaAssertionParser()

    def test_parse_simple_log_output(self):
        """Test parsing simple log statements"""
        output = """
🧪 Starting simple Dana test
✅ Basic math test passed: 2 + 2 = 4
✅ String test passed: Hello, Dana!
✅ Variable test passed: 10 + 20 = 30
🎉 All simple tests completed successfully!
        """.strip()

        assertions = self.parser.parse_output(output)

        # Should find pass indicators
        assert len(assertions) > 0
        assert any(a.passed for a in assertions)

    def test_parse_assertions_with_failures(self):
        """Test parsing mixed pass/fail assertions"""
        output = """
✅ Test 1 passed
❌ Test 2 failed
✅ Test 3 passed
Error: Assertion failed at line 15
        """.strip()

        assertions = self.parser.parse_output(output)

        # Should find both passes and failures
        passed = [a for a in assertions if a.passed]
        failed = [a for a in assertions if not a.passed]

        assert len(passed) >= 2
        assert len(failed) >= 2

    def test_parse_error_output(self):
        """Test parsing error output"""
        error_output = """
Error: Undefined variable 'x'
Exception: Division by zero at line 42
        """.strip()

        assertions = self.parser.parse_output("", error_output)

        # Should find errors
        assert len(assertions) >= 2
        assert all(not a.passed for a in assertions)
        assert all(a.assertion_type == "error" for a in assertions)

    def test_parse_json_output(self):
        """Test parsing JSON-formatted output"""
        json_output = """
        {
            "tests": [
                {"line": 10, "message": "x == 5", "passed": true, "source": "assert x == 5"},
                {"line": 20, "message": "y != 10", "passed": false, "source": "assert y != 10"}
            ],
            "logs": [
                {"line": 5, "message": "Starting test", "source": "log('Starting test')"}
            ]
        }
        """

        assertions = self.parser.parse_output(json_output)

        assert len(assertions) == 3

        # Check test assertions
        test_assertions = [a for a in assertions if a.assertion_type == "assert"]
        assert len(test_assertions) == 2
        assert test_assertions[0].line_number == 10
        assert test_assertions[0].passed is True
        assert test_assertions[1].line_number == 20
        assert test_assertions[1].passed is False

        # Check logs
        logs = [a for a in assertions if a.assertion_type == "log"]
        assert len(logs) == 1
        assert logs[0].line_number == 5

    def test_parse_empty_output(self):
        """Test parsing empty output"""
        assertions = self.parser.parse_output("")

        # Should return empty list
        assert assertions == []

    def test_parse_log_statements(self):
        """Test parsing log() function calls"""
        output = """
log("Starting tests")
log('Test case 1')
log(f"Result: {result}")
        """.strip()

        assertions = self.parser.parse_output(output)

        # Should find log statements
        logs = [a for a in assertions if a.assertion_type == "log"]
        assert len(logs) >= 1

    def test_extract_test_summary(self):
        """Test extracting test summary"""
        assertions = [
            DanaAssertion(line_number=10, assertion_type="assert", message="test1", passed=True),
            DanaAssertion(line_number=20, assertion_type="assert", message="test2", passed=True),
            DanaAssertion(line_number=30, assertion_type="assert", message="test3", passed=False),
            DanaAssertion(line_number=40, assertion_type="log", message="log msg", passed=True),
        ]

        passed, failed = self.parser.extract_test_summary(assertions)

        assert passed == 2  # Only count assert type
        assert failed == 1

    def test_parse_with_line_numbers(self):
        """Test parsing assertions with line numbers"""
        output = """
Line 10: assert x == 5 passed
Line 20: assertion y != 10 failed
        """.strip()

        assertions = self.parser.parse_output(output)

        # Should extract line numbers
        assert any(a.line_number == 10 for a in assertions)
        assert any(a.line_number == 20 for a in assertions)

    def test_pass_fail_indicators(self):
        """Test various pass/fail indicator patterns"""
        # Test pass indicators
        for indicator in ["✅", "passed", "success", "ok", "PASS"]:
            output = f"Test {indicator}"
            assertions = self.parser.parse_output(output)
            assert len(assertions) > 0
            assert any(a.passed for a in assertions)

        # Test fail indicators
        for indicator in ["❌", "failed", "failure", "error", "FAIL"]:
            output = f"Test {indicator}"
            assertions = self.parser.parse_output(output)
            assert len(assertions) > 0
            assert any(not a.passed for a in assertions)

    def test_mixed_json_and_text(self):
        """Test parsing output with both JSON and text"""
        output = """
Some initial text
{"tests": [{"line": 10, "message": "test", "passed": true}]}
Some trailing text
        """

        assertions = self.parser.parse_output(output)

        # Should parse JSON part
        assert len(assertions) >= 1
        # The JSON parsing should extract the line number from the JSON
        json_assertions = [a for a in assertions if a.line_number == 10]
        assert len(json_assertions) >= 1
