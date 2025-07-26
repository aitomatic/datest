"""
Unit tests for Dana test executor functionality.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch
import subprocess

from datest.executor import DanaTestExecutor
from datest.models import DanaTestResult


class TestDanaTestExecutor:
    """Test DanaTestExecutor class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.executor = DanaTestExecutor()
    
    def test_init_default_config(self):
        """Test initialization with default config"""
        executor = DanaTestExecutor()
        
        assert executor.timeout == 30.0
        assert executor.dana_command == "dana"
        assert executor.use_json_output is False
        assert executor.assertion_parser is not None
    
    def test_init_custom_config(self):
        """Test initialization with custom config"""
        config = {
            "timeout": 60.0,
            "dana_command": "/usr/bin/dana",
            "use_json_output": True
        }
        executor = DanaTestExecutor(config)
        
        assert executor.timeout == 60.0
        assert executor.dana_command == "/usr/bin/dana"
        assert executor.use_json_output is True
    
    @patch("subprocess.run")
    def test_run_dana_file_success(self, mock_run):
        """Test successful Dana file execution"""
        # Mock successful execution
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="✅ All tests passed",
            stderr=""
        )
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        assert isinstance(result, DanaTestResult)
        assert result.success is True
        assert result.exit_code == 0
        assert "✅" in result.output
        
        # Verify subprocess was called correctly
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "dana"
        assert "test.na" in call_args[-1]
    
    @patch("subprocess.run")
    def test_run_dana_file_with_json_output(self, mock_run):
        """Test Dana file execution with JSON output flag"""
        # Configure executor for JSON output
        self.executor.use_json_output = True
        
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"tests": []}',
            stderr=""
        )
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        # Verify --output-json flag was added
        call_args = mock_run.call_args[0][0]
        assert "--output-json" in call_args
    
    @patch("subprocess.run")
    def test_run_dana_file_failure(self, mock_run):
        """Test failed Dana file execution"""
        # Mock failed execution
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="❌ Test failed",
            stderr="Error: Assertion failed"
        )
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        assert result.success is False
        assert result.exit_code == 1
        assert result.errors == "Error: Assertion failed"
    
    @patch("subprocess.run")
    def test_run_dana_file_with_parsed_assertions(self, mock_run):
        """Test that assertions are parsed from output"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="✅ Test 1 passed\n❌ Test 2 failed",
            stderr=""
        )
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        # Should have parsed assertions
        assert len(result.assertions) > 0
        
        # Check for both pass and fail assertions
        passed = [a for a in result.assertions if a.passed]
        failed = [a for a in result.assertions if not a.passed]
        assert len(passed) > 0
        assert len(failed) > 0
        
        # Success should be False due to failed assertion
        assert result.success is False
    
    @patch("subprocess.run")
    def test_run_dana_file_timeout(self, mock_run):
        """Test Dana file execution timeout"""
        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired("dana", timeout=30.0)
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        assert result.success is False
        assert result.exit_code == 124  # Standard timeout exit code
        assert "timed out" in result.errors
    
    @patch("subprocess.run")
    def test_run_dana_file_command_not_found(self, mock_run):
        """Test Dana command not found"""
        # Mock command not found
        mock_run.side_effect = FileNotFoundError("dana not found")
        
        result = self.executor.run_dana_file(Path("test.na"))
        
        assert result.success is False
        assert result.exit_code == 127  # Command not found
        assert "not found" in result.errors
    
    @patch("subprocess.run")
    def test_run_multiple_files(self, mock_run):
        """Test running multiple Dana files"""
        # Mock different results for each file
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="✅ Pass", stderr=""),
            MagicMock(returncode=1, stdout="❌ Fail", stderr="Error"),
            MagicMock(returncode=0, stdout="✅ Pass", stderr=""),
        ]
        
        files = [Path("test1.na"), Path("test2.na"), Path("test3.na")]
        results = self.executor.run_multiple_files(files)
        
        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True
    
    @patch("subprocess.run")
    def test_is_dana_available_true(self, mock_run):
        """Test checking Dana availability when available"""
        mock_run.return_value = MagicMock(returncode=0)
        
        assert self.executor.is_dana_available() is True
        
        # Should call with --version
        call_args = mock_run.call_args[0][0]
        assert call_args == ["dana", "--version"]
    
    @patch("subprocess.run")
    def test_is_dana_available_false(self, mock_run):
        """Test checking Dana availability when not available"""
        mock_run.side_effect = FileNotFoundError()
        
        assert self.executor.is_dana_available() is False
    
    @patch("subprocess.run")
    def test_working_directory(self, mock_run):
        """Test that executor runs in correct working directory"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr=""
        )
        
        test_file = Path("/some/path/test.na")
        self.executor.run_dana_file(test_file)
        
        # Should run in the test file's parent directory
        kwargs = mock_run.call_args[1]
        assert kwargs["cwd"] == test_file.parent