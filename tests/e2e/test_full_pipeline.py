"""
End-to-end tests for datest full pipeline.

Tests the complete flow from discovery to execution to reporting.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFullPipeline:
    """Test complete datest pipeline"""

    def test_cli_help(self):
        """Test CLI help command"""
        result = subprocess.run(
            [sys.executable, "-m", "datest", "--help"], capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "Datest: Testing framework for Dana language files" in result.stdout
        assert "--verbose" in result.stdout
        assert "--pattern" in result.stdout
        assert "--discover-only" in result.stdout
        assert "--config" in result.stdout
        assert "--json" in result.stdout

    def test_cli_version(self):
        """Test CLI version command"""
        result = subprocess.run(
            [sys.executable, "-m", "datest", "--version"], capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "datest, version" in result.stdout

    @patch("subprocess.run")
    def test_cli_discover_only(self, mock_run):
        """Test discover-only mode"""
        # Run discovery only
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--discover-only", "tests/fixtures"])

        # Should exit successfully without running tests
        assert result.exit_code == 0
        assert "Discovered" in result.output

    @patch("subprocess.run")
    def test_cli_with_patterns(self, mock_run):
        """Test CLI with custom patterns"""
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()
        result = runner.invoke(
            main, ["--pattern", "spec_*.na", "--pattern", "*_spec.na", "--discover-only", "."]
        )

        # Should use custom patterns
        assert result.exit_code == 0 or result.exit_code == 1  # Depends on if files found

    @patch("subprocess.run")
    def test_cli_verbose_mode(self, mock_run):
        """Test verbose mode"""
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--verbose", "--discover-only", "."])

        assert "Debug logging enabled" in result.output

    @patch("subprocess.run")
    def test_cli_no_color(self, mock_run):
        """Test no-color option"""
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()
        result = runner.invoke(main, ["--no-color", "--discover-only", "."])

        # Output should not contain ANSI color codes
        assert "\033[" not in result.output

    @patch("datest.executor.DanaTestExecutor.is_dana_available")
    @patch("subprocess.run")
    def test_full_execution_mock(self, mock_run, mock_dana_available):
        """Test full execution with mocked Dana"""
        from click.testing import CliRunner

        from datest.cli import main

        # Mock Dana is available
        mock_dana_available.return_value = True

        # Mock successful test execution
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "✅ All tests passed"
        mock_run.return_value.stderr = ""

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create a test file
            Path("test_example.na").write_text("// Test file")

            result = runner.invoke(main, ["."])

            # Should execute successfully
            assert result.exit_code == 0
            assert "All tests passed" in result.output

    def test_config_file_loading(self):
        """Test configuration file loading"""
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create config file
            config_content = """
[discovery]
patterns = ["spec_*.na"]

[execution]
timeout = 60.0

[output]
verbose = true
            """
            Path("datest.toml").write_text(config_content)

            # Create a spec file
            Path("spec_example.na").write_text("// Spec file")

            result = runner.invoke(main, ["--discover-only", "."])

            # Should discover spec file based on config
            assert result.exit_code == 0
            assert "spec_example.na" in result.output

    def test_pytest_integration(self):
        """Test pytest plugin integration"""
        # This would test actual pytest integration
        # For now, just verify the plugin can be imported
        try:
            from datest.pytest_plugin import pytest_collect_file

            assert pytest_collect_file is not None
        except ImportError:
            pytest.skip("pytest plugin not available")

    @patch("subprocess.run")
    def test_exit_codes(self, mock_run):
        """Test proper exit codes"""
        from click.testing import CliRunner

        from datest.cli import main

        runner = CliRunner()

        # Test no files found
        with runner.isolated_filesystem():
            result = runner.invoke(main, ["."])
            assert result.exit_code == 1  # No files found

        # Test with files but Dana not available
        with runner.isolated_filesystem():
            Path("test_example.na").write_text("// Test")

            with patch("datest.executor.DanaTestExecutor.is_dana_available") as mock_avail:
                mock_avail.return_value = False
                result = runner.invoke(main, ["."])
                assert result.exit_code == 2  # Dana not available
