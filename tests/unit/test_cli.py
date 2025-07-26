"""
Tests for the CLI module.
"""

from pathlib import Path
from unittest.mock import Mock, patch

from datest.cli import main


class TestCLI:
    """Test CLI functionality"""

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_basic_execution(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test basic CLI execution"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config_instance.dana_command = "dana"
        mock_config_instance.timeout = 30.0
        mock_config_instance.use_json_output = False
        mock_config_instance.use_color = True
        mock_config_instance.verbose = False
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na"), Path("test2.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock executor
        mock_executor_instance = Mock()
        mock_executor_instance.is_dana_available.return_value = True
        mock_executor_instance.run_multiple_files.return_value = [
            Mock(success=True),
            Mock(success=True),
        ]
        mock_executor.return_value = mock_executor_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with no arguments (should use default paths)
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=False,
                config=None,
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify discovery was called
        mock_discovery_instance.discover.assert_called_once()

        # Verify executor was called
        mock_executor_instance.run_multiple_files.assert_called_once()

        # Verify reporter was called
        mock_reporter_instance.generate_report.assert_called_once()

        # Verify exit with success
        mock_exit.assert_called_once_with(0)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_discover_only(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test discover-only mode"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na"), Path("test2.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test discover-only mode
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=True,
                config=None,
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify discovery was called
        mock_discovery_instance.discover.assert_called_once()

        # Verify reporter was called for discovery results
        mock_reporter_instance.print_discovery_results.assert_called_once()

        # Verify exit with success
        mock_exit.assert_called_once_with(0)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_no_test_files_found(
        self, mock_exit, mock_echo, mock_reporter, mock_discovery, mock_config
    ):
        """Test when no test files are found"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery with no files
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = []
        mock_discovery.return_value = mock_discovery_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with no test files found
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=False,
                config=None,
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify warning was printed
        mock_reporter_instance.print_warning.assert_called()

        # Verify exit with error
        mock_exit.assert_called_once_with(1)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_dana_not_available(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test when Dana is not available"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config_instance.dana_command = "dana"
        mock_config_instance.timeout = 30.0
        mock_config_instance.use_json_output = False
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock executor with Dana not available
        mock_executor_instance = Mock()
        mock_executor_instance.is_dana_available.return_value = False
        mock_executor.return_value = mock_executor_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with Dana not available
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=False,
                config=None,
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify warning was printed
        mock_reporter_instance.print_warning.assert_called()

        # Verify exit with error
        mock_exit.assert_called_once_with(2)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_with_test_failures(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test when tests fail"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config_instance.dana_command = "dana"
        mock_config_instance.timeout = 30.0
        mock_config_instance.use_json_output = False
        mock_config_instance.use_color = True
        mock_config_instance.verbose = False
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock executor with test failure
        mock_executor_instance = Mock()
        mock_executor_instance.is_dana_available.return_value = True
        mock_executor_instance.run_multiple_files.return_value = [Mock(success=False)]
        mock_executor.return_value = mock_executor_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with test failures
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=False,
                config=None,
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify exit with failure
        mock_exit.assert_called_once_with(1)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_with_exception(self, mock_exit, mock_echo, mock_reporter, mock_config):
        """Test handling of exceptions"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Mock discovery to raise an exception
        with patch("datest.cli.DanaTestDiscovery") as mock_discovery:
            mock_discovery_instance = Mock()
            mock_discovery_instance.discover.side_effect = Exception("Test error")
            mock_discovery.return_value = mock_discovery_instance

            with patch("pathlib.Path.exists", return_value=True):
                main(
                    verbose=False,
                    pattern=(),
                    discover_only=False,
                    config=None,
                    json=False,
                    timeout=None,
                    no_color=False,
                    test_paths=(),
                )

        # Verify error was printed
        mock_reporter_instance.print_error.assert_called_with("Test error")

        # Verify exit with error
        mock_exit.assert_called_once_with(2)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_with_keyboard_interrupt(self, mock_exit, mock_echo, mock_reporter, mock_config):
        """Test handling of keyboard interrupt"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery to raise KeyboardInterrupt
        with patch("datest.cli.DanaTestDiscovery") as mock_discovery:
            mock_discovery_instance = Mock()
            mock_discovery_instance.discover.side_effect = KeyboardInterrupt()
            mock_discovery.return_value = mock_discovery_instance

            with patch("pathlib.Path.exists", return_value=True):
                main(
                    verbose=False,
                    pattern=(),
                    discover_only=False,
                    config=None,
                    json=False,
                    timeout=None,
                    no_color=False,
                    test_paths=(),
                )

        # Verify interrupt message was printed
        mock_echo.assert_called_with("\n\nInterrupted by user", err=True)

        # Verify exit with interrupt code
        mock_exit.assert_called_once_with(130)

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_with_custom_options(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test CLI with custom options"""
        # Mock configuration
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config_instance.dana_command = "dana"
        mock_config_instance.timeout = 30.0
        mock_config_instance.use_json_output = False
        mock_config_instance.use_color = True
        mock_config_instance.verbose = False
        mock_config.find_and_load.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock executor
        mock_executor_instance = Mock()
        mock_executor_instance.is_dana_available.return_value = True
        mock_executor_instance.run_multiple_files.return_value = [Mock(success=True)]
        mock_executor.return_value = mock_executor_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with custom options
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=True,
                pattern=("custom_*.na",),
                discover_only=False,
                config=None,
                json=True,
                timeout=60.0,
                no_color=True,
                test_paths=("custom_path",),
            )

        # Verify configuration was updated
        assert mock_config_instance.verbose is True
        assert mock_config_instance.use_json_output is True
        assert mock_config_instance.timeout == 60.0
        assert mock_config_instance.use_color is False

        # Verify discovery was called with custom patterns
        call_args = mock_discovery.call_args[0][0]
        assert call_args.patterns == ["custom_*.na"]

    @patch("datest.cli.DatestConfig")
    @patch("datest.cli.DanaTestDiscovery")
    @patch("datest.cli.DanaTestExecutor")
    @patch("datest.cli.DanaTestReporter")
    @patch("datest.cli.click.echo")
    @patch("datest.cli.sys.exit")
    def test_main_with_config_file(
        self, mock_exit, mock_echo, mock_reporter, mock_executor, mock_discovery, mock_config
    ):
        """Test CLI with config file"""
        # Mock configuration loading from file
        mock_config_instance = Mock()
        mock_config_instance.test_patterns = ["test_*.na"]
        mock_config_instance.exclude_patterns = [".*"]
        mock_config_instance.recursive = True
        mock_config_instance.max_depth = 10
        mock_config_instance.dana_command = "dana"
        mock_config_instance.timeout = 30.0
        mock_config_instance.use_json_output = False
        mock_config_instance.use_color = True
        mock_config_instance.verbose = False
        mock_config.load_from_file.return_value = mock_config_instance

        # Mock discovery
        mock_discovery_instance = Mock()
        mock_discovery_instance.discover.return_value = [Path("test1.na")]
        mock_discovery.return_value = mock_discovery_instance

        # Mock executor
        mock_executor_instance = Mock()
        mock_executor_instance.is_dana_available.return_value = True
        mock_executor_instance.run_multiple_files.return_value = [Mock(success=True)]
        mock_executor.return_value = mock_executor_instance

        # Mock reporter
        mock_reporter_instance = Mock()
        mock_reporter.return_value = mock_reporter_instance

        # Test with config file
        with patch("pathlib.Path.exists", return_value=True):
            main(
                verbose=False,
                pattern=(),
                discover_only=False,
                config="config.toml",
                json=False,
                timeout=None,
                no_color=False,
                test_paths=(),
            )

        # Verify config was loaded from file
        mock_config.load_from_file.assert_called_once()

        # Verify exit with success
        mock_exit.assert_called_once_with(0)
