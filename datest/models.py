"""
Data models for Dana test framework.

Defines core data structures for test files, results, and assertions.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DanaTestFile:
    """Represents a Dana test file"""

    path: Path
    name: str

    def __post_init__(self):
        """Ensure name is set from path if not provided"""
        if not self.name:
            self.name = self.path.name


@dataclass
class DanaAssertion:
    """Dana assertion result"""

    line_number: int
    assertion_type: str  # "assert", "log", "error", etc.
    message: str
    passed: bool
    source_line: str | None = None

    def __str__(self) -> str:
        """String representation of assertion"""
        status = "✅" if self.passed else "❌"
        return f"{status} Line {self.line_number}: {self.message}"


@dataclass
class DanaTestResult:
    """Result of running a Dana test file"""

    file_path: Path
    success: bool
    duration: float
    output: str = ""
    errors: str = ""
    exit_code: int = 0
    assertions: list[DanaAssertion] = field(default_factory=list)

    @property
    def failed_assertions(self) -> list[DanaAssertion]:
        """Get only failed assertions"""
        return [a for a in self.assertions if not a.passed]

    @property
    def passed_assertions(self) -> list[DanaAssertion]:
        """Get only passed assertions"""
        return [a for a in self.assertions if a.passed]

    @property
    def test_name(self) -> str:
        """Get test file name without extension"""
        return self.file_path.stem

    def has_errors(self) -> bool:
        """Check if test has any errors"""
        return bool(self.errors) or self.exit_code != 0

    def summary(self) -> str:
        """Get a summary of the test result"""
        total = len(self.assertions)
        passed = len(self.passed_assertions)
        _failed = len(self.failed_assertions)  # Unused but kept for potential future use

        status = "PASSED" if self.success else "FAILED"
        return f"{self.test_name}: {status} ({passed}/{total} assertions, {self.duration:.2f}s)"
