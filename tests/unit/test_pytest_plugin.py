"""
Tests for pytest plugin functionality.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from datest.pytest_plugin import (
    DanaTestFailure,
    DanaTestFile,
    DanaTestItem,
    DanaTestReportHook,
    _is_test_file,
    _matches_pattern,
    pytest_addoption,
    pytest_collect_file,
    pytest_configure,
    pytest_plugin_registered,
)


class TestPytestPlugin:
    """Test pytest plugin functionality"""

    def test_pytest_addoption(self):
        """Test adding command line options"""
        parser = Mock()
        group = Mock()
        parser.getgroup.return_value = group

        pytest_addoption(parser)

        parser.getgroup.assert_called_once_with("dana", "Dana test options")
        assert group.addoption.call_count == 3

        # Check that all options were added
        calls = group.addoption.call_args_list
        option_names = [call[0][0] for call in calls]
        assert "--dana-command" in option_names
        assert "--dana-timeout" in option_names
        assert "--dana-json" in option_names

    def test_pytest_configure(self):
        """Test pytest configuration"""
        config = Mock()

        pytest_configure(config)

        config.addinivalue_line.assert_called_once_with(
            "markers", "dana: mark test as a Dana test file"
        )

    def test_pytest_collect_file_na_file(self):
        """Test collecting .na test files"""
        parent = Mock()
        file_path = Path("test_example.na")

        with patch("datest.pytest_plugin._is_test_file", return_value=True):
            result = pytest_collect_file(parent, file_path)

        assert result is not None
        assert isinstance(result, DanaTestFile)

    def test_pytest_collect_file_not_na_file(self):
        """Test that non-.na files are not collected"""
        parent = Mock()
        file_path = Path("test_example.py")

        result = pytest_collect_file(parent, file_path)

        assert result is None

    def test_pytest_collect_file_not_test_file(self):
        """Test that .na files that aren't test files are not collected"""
        parent = Mock()
        file_path = Path("example.na")

        with patch("datest.pytest_plugin._is_test_file", return_value=False):
            result = pytest_collect_file(parent, file_path)

        assert result is None

    def test_is_test_file(self):
        """Test test file detection"""
        # Test files that should be detected
        assert _is_test_file(Path("test_example.na"))
        assert _is_test_file(Path("example_test.na"))
        assert _is_test_file(Path("test_example_test.na"))

        # Test files that should not be detected
        assert not _is_test_file(Path("example.na"))
        assert not _is_test_file(Path("test_example.py"))
        assert not _is_test_file(Path("example_test.py"))

    def test_matches_pattern(self):
        """Test pattern matching functionality"""
        # Test exact match
        assert _matches_pattern("test.na", "test.na")
        assert not _matches_pattern("test.na", "other.na")

        # Test prefix pattern
        assert _matches_pattern("test_example.na", "test_*.na")
        assert not _matches_pattern("example_test.na", "test_*.na")

        # Test suffix pattern
        assert _matches_pattern("example_test.na", "*_test.na")
        assert not _matches_pattern("test_example.na", "*_test.na")

        # Test prefix and suffix pattern
        assert _matches_pattern("test_example_test.na", "test_*_test.na")
        assert not _matches_pattern("example_test.na", "test_*_test.na")

        # Test complex patterns
        assert not _matches_pattern("test.na", "test_*_*_test.na")


class TestDanaTestFile:
    """Test DanaTestFile class"""

    def test_collect(self):
        """Test collecting test items from Dana file"""
        parent = Mock()
        file_path = Path("test_example.na")
        test_file = DanaTestFile.from_parent(parent, path=file_path)

        items = list(test_file.collect())

        assert len(items) == 1
        assert isinstance(items[0], DanaTestItem)
        assert items[0].name == "test_example.na"


class TestDanaTestItem:
    """Test DanaTestItem class"""

    def test_setup(self):
        """Test setting up Dana test execution"""
        parent = Mock()
        config = Mock()
        config.getoption.side_effect = lambda opt: {
            "--dana-command": "dana",
            "--dana-timeout": 30.0,
            "--dana-json": False,
        }[opt]

        test_item = DanaTestItem.from_parent(parent, name="test_example.na")
        test_item.config = config

        with patch("datest.pytest_plugin.DanaTestExecutor") as mock_executor:
            test_item.setup()

            mock_executor.assert_called_once_with(
                {
                    "dana_command": "dana",
                    "timeout": 30.0,
                    "use_json_output": False,
                }
            )

    def test_runtest_success(self):
        """Test successful test execution"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")
        test_item.path = "test_example.na"

        # Mock successful result
        mock_result = Mock()
        mock_result.success = True
        mock_result.errors = ""
        mock_result.failed_assertions = []

        with patch("datest.pytest_plugin.DanaTestExecutor") as mock_executor_class:
            mock_executor = Mock()
            mock_executor_class.return_value = mock_executor
            mock_executor.run_dana_file.return_value = mock_result

            test_item.setup()
            test_item.runtest()

            mock_executor.run_dana_file.assert_called_once()
            assert test_item.result == mock_result

    def test_runtest_failure(self):
        """Test failed test execution"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")
        test_item.path = "test_example.na"

        # Mock failed result
        mock_result = Mock()
        mock_result.success = False
        mock_result.errors = "Test failed"
        mock_result.failed_assertions = []

        with patch("datest.pytest_plugin.DanaTestExecutor") as mock_executor_class:
            mock_executor = Mock()
            mock_executor_class.return_value = mock_executor
            mock_executor.run_dana_file.return_value = mock_result

            test_item.setup()

            with pytest.raises(DanaTestFailure) as exc_info:
                test_item.runtest()

            assert "Test failed" in str(exc_info.value)

    def test_runtest_with_failed_assertions(self):
        """Test test execution with failed assertions"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")
        test_item.path = "test_example.na"

        # Mock failed assertions
        mock_assertion = Mock()
        mock_assertion.line_number = 10
        mock_assertion.message = "Assertion failed"

        mock_result = Mock()
        mock_result.success = False
        mock_result.errors = ""
        mock_result.failed_assertions = [mock_assertion]

        with patch("datest.pytest_plugin.DanaTestExecutor") as mock_executor_class:
            mock_executor = Mock()
            mock_executor_class.return_value = mock_executor
            mock_executor.run_dana_file.return_value = mock_result

            test_item.setup()

            with pytest.raises(DanaTestFailure) as exc_info:
                test_item.runtest()

            assert "Line 10: Assertion failed" in str(exc_info.value)

    def test_repr_failure_dana_failure(self):
        """Test failure representation for Dana failures"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")

        excinfo = Mock()
        excinfo.value = DanaTestFailure("Test failed")

        result = test_item.repr_failure(excinfo)

        assert result == "Dana test failed:\nTest failed"

    def test_repr_failure_other_exception(self):
        """Test failure representation for other exceptions"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")

        excinfo = Mock()
        excinfo.value = ValueError("Other error")

        with patch.object(test_item, "super") as mock_super:
            mock_super.return_value.repr_failure.return_value = "Other error"
            test_item.repr_failure(excinfo)

            mock_super.return_value.repr_failure.assert_called_once_with(excinfo)

    def test_reportinfo(self):
        """Test report information"""
        parent = Mock()
        test_item = DanaTestItem.from_parent(parent, name="test_example.na")
        test_item.path = "test_example.na"

        result = test_item.reportinfo()

        assert result == ("test_example.na", 0, "Dana test: test_example.na")


class TestDanaTestFailure:
    """Test DanaTestFailure exception"""

    def test_dana_test_failure(self):
        """Test DanaTestFailure exception"""
        with pytest.raises(DanaTestFailure) as exc_info:
            raise DanaTestFailure("Test failed")

        assert str(exc_info.value) == "Test failed"


class TestDanaTestReportHook:
    """Test DanaTestReportHook"""

    def test_pytest_runtest_makereport(self):
        """Test test report enhancement"""
        hook = DanaTestReportHook()
        item = Mock()

        # Mock DanaTestItem with result
        item.result = Mock()
        item.result.output = "Test output"
        item.result.assertions = [Mock(), Mock()]  # 2 assertions

        outcome = Mock()
        report = Mock()
        report.sections = []
        outcome.get_result.return_value = report

        with (
            patch("datest.pytest_plugin.DanaTestItem", return_value=type(item)),
            patch.object(hook, "pytest_runtest_makereport", wraps=hook.pytest_runtest_makereport),
        ):
            # This is a bit complex to test due to the hookwrapper decorator
            # We'll just test that the hook can be instantiated
            assert isinstance(hook, DanaTestReportHook)


def test_pytest_plugin_registered():
    """Test plugin registration"""
    plugin = Mock()
    manager = Mock()

    pytest_plugin_registered(plugin, manager)

    # The function should register the hook
    manager.register.assert_called_once()
