"""
pytest plugin for Dana test file integration.

Allows pytest to discover and run .na Dana test files.
"""

import logging
from pathlib import Path

import pytest

from .executor import DanaTestExecutor

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add Dana-specific command line options"""
    group = parser.getgroup("dana", "Dana test options")

    group.addoption(
        "--dana-command",
        action="store",
        default="dana",
        help="Path to Dana command (default: dana)",
    )

    group.addoption(
        "--dana-timeout",
        action="store",
        type=float,
        default=30.0,
        help="Timeout for Dana test execution in seconds (default: 30)",
    )

    group.addoption(
        "--dana-json",
        action="store_true",
        default=False,
        help="Use JSON output format for Dana tests",
    )


def pytest_configure(config):
    """Configure pytest with Dana test support"""
    # Register Dana test marker
    config.addinivalue_line("markers", "dana: mark test as a Dana test file")


def pytest_collect_file(parent, file_path):
    """Hook to collect Dana test files"""
    path = Path(file_path)

    # Check if this is a Dana test file
    if path.suffix == ".na" and _is_test_file(path):
        return DanaTestFile.from_parent(parent, path=file_path)

    return None


def _is_test_file(path: Path) -> bool:
    """Check if a path is a Dana test file"""
    # Use same patterns as DanaTestDiscovery
    test_patterns = ["test_*.na", "*_test.na"]
    filename = path.name

    return any(_matches_pattern(filename, pattern) for pattern in test_patterns)


def _matches_pattern(filename: str, pattern: str) -> bool:
    """Simple pattern matching for test files"""
    if "*" not in pattern:
        return filename == pattern

    parts = pattern.split("*")
    if len(parts) == 2:
        prefix, suffix = parts
        if prefix and suffix:
            return filename.startswith(prefix) and filename.endswith(suffix)
        elif prefix:
            return filename.startswith(prefix)
        elif suffix:
            return filename.endswith(suffix)

    return False


class DanaTestFile(pytest.File):
    """Represents a Dana test file in pytest"""

    def collect(self):
        """Collect test items from Dana file"""
        # For now, treat entire file as one test
        # Future: could parse file to find individual test functions
        yield DanaTestItem.from_parent(self, name=self.path.name)


class DanaTestItem(pytest.Item):
    """Represents a single Dana test execution"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executor = None
        self.result = None

    def setup(self):
        """Set up Dana test execution"""
        # Get configuration from pytest
        config = {
            "dana_command": self.config.getoption("--dana-command"),
            "timeout": self.config.getoption("--dana-timeout"),
            "use_json_output": self.config.getoption("--dana-json"),
        }

        self.executor = DanaTestExecutor(config)

    def runtest(self):
        """Execute the Dana test file"""
        if not self.executor:
            self.setup()

        # Run the Dana test
        self.result = self.executor.run_dana_file(Path(self.path))

        # Check for failures
        if not self.result.success:
            # Build failure message
            failure_msgs = []

            if self.result.errors:
                failure_msgs.append(f"Errors:\n{self.result.errors}")

            # Add failed assertions
            for assertion in self.result.failed_assertions:
                failure_msgs.append(f"Line {assertion.line_number}: {assertion.message}")

            # Raise test failure
            raise DanaTestFailure("\n".join(failure_msgs))

    def repr_failure(self, excinfo):
        """Represent test failure for pytest output"""
        if isinstance(excinfo.value, DanaTestFailure):
            return f"Dana test failed:\n{excinfo.value}"

        return super().repr_failure(excinfo)

    def reportinfo(self):
        """Report information about the test"""
        return self.path, 0, f"Dana test: {self.name}"


class DanaTestFailure(Exception):
    """Exception raised when a Dana test fails"""

    pass


# Plugin hooks for test reporting
class DanaTestReportHook:
    """Hook for Dana test reporting in pytest"""

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Enhance test report with Dana-specific information"""
        outcome = yield
        report = outcome.get_result()

        if isinstance(item, DanaTestItem) and item.result:
            # Add Dana test result to report
            report.dana_result = item.result

            # Add extra information to report
            if hasattr(report, "sections"):
                # Add Dana output section
                if item.result.output:
                    report.sections.append(("Dana Output", item.result.output))

                # Add assertions summary
                if item.result.assertions:
                    passed = len(item.result.passed_assertions)
                    failed = len(item.result.failed_assertions)
                    summary = f"Assertions: {passed} passed, {failed} failed"
                    report.sections.append(("Dana Assertions", summary))


# Register the plugin
def pytest_plugin_registered(plugin, manager):
    """Register Dana test report hook"""
    if isinstance(plugin, type(pytest_plugin_registered.__module__)):
        manager.register(DanaTestReportHook())
