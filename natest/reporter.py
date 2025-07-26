"""
Test result reporting for Dana tests.

Formats and displays test results with Dana context.
"""

import logging
import sys
from typing import TextIO

from rich.console import Console
from rich.table import Table
from rich.text import Text

from .executor import DanaTestResult

logger = logging.getLogger(__name__)


class DanaTestReporter:
    """Formats and displays Dana test results"""

    def __init__(self, output: TextIO = None, use_color: bool = True, verbose: bool = False):
        self.output = output or sys.stdout
        self.console = Console(file=self.output, color_system="auto" if use_color else None)
        self.verbose = verbose
        logger.debug(f"Initialized reporter with color: {use_color}, verbose: {verbose}")

    def generate_report(self, results: list[DanaTestResult]) -> None:
        """
        Generate complete test report

        Args:
            results: List of test results to report
        """
        if not results:
            self.console.print("No test results to report", style="yellow")
            return

        self._print_header(results)
        self._print_test_results(results)
        self._print_summary(results)

    def _print_header(self, results: list[DanaTestResult]) -> None:
        """Print report header"""
        total_tests = len(results)
        self.console.print(f"\n🧪 Running {total_tests} Dana test file(s)\n")

    def _print_test_results(self, results: list[DanaTestResult]) -> None:
        """Print individual test results"""
        for result in results:
            self._print_single_result(result)

    def _print_single_result(self, result: DanaTestResult) -> None:
        """Print result for a single test file"""
        status_icon = self._get_status_icon(result.success)
        status_color = self._get_status_color(result.success)

        # Test file name and status
        test_line = Text()
        test_line.append(f"{status_icon} ")
        test_line.append(result.file_path.name, style="bold")
        test_line.append(" ... ", style="dim")
        status_text = "PASSED" if result.success else "FAILED"
        test_line.append(status_text, style=status_color)

        if result.duration > 0:
            test_line.append(f" ({result.duration:.2f}s)", style="dim")

        self.console.print(test_line)

        # Print detailed output if verbose or if there are errors
        if self.verbose or not result.success:
            self._print_detailed_output(result)

    def _print_detailed_output(self, result: DanaTestResult) -> None:
        """Print detailed test output"""
        if result.output:
            # Print Dana output (log statements, etc.)
            output_lines = result.output.strip().split("\n")
            for line in output_lines:
                if line.strip():
                    self.console.print(f"    {line}", style="dim")

        if result.errors:
            # Print errors in red
            error_lines = result.errors.strip().split("\n")
            for line in error_lines:
                if line.strip():
                    self.console.print(f"    Error: {line}", style="red")

        # Print assertion results if any
        if result.assertions:
            for assertion in result.assertions:
                if assertion["type"] == "pass":
                    self.console.print(f"    ✅ {assertion['message']}", style="green")
                elif assertion["type"] == "fail":
                    self.console.print(f"    ❌ {assertion['message']}", style="red")

    def _print_summary(self, results: list[DanaTestResult]) -> None:
        """Print test summary"""
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed

        total_duration = sum(r.duration for r in results)

        self.console.print()

        # Summary table
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="bold")
        table.add_column("Count")

        table.add_row("Total files", str(total))
        if passed > 0:
            table.add_row("✅ Passed", str(passed), style="green")
        if failed > 0:
            table.add_row("❌ Failed", str(failed), style="red")
        table.add_row("⏱️  Duration", f"{total_duration:.2f}s")

        self.console.print(table)

        # Overall result
        if failed == 0:
            self.console.print("\n🎉 All tests passed!", style="bold green")
        else:
            self.console.print(f"\n💥 {failed} test file(s) failed", style="bold red")

    def _get_status_icon(self, success: bool) -> str:
        """Get icon for test status"""
        return "✅" if success else "❌"

    def _get_status_color(self, success: bool) -> str:
        """Get color for test status"""
        return "green" if success else "red"

    def print_discovery_results(self, discovered_files: list[str]) -> None:
        """Print test discovery results"""
        if not discovered_files:
            self.console.print("No Dana test files found", style="yellow")
            return

        self.console.print(f"\n🔍 Discovered {len(discovered_files)} Dana test file(s):")
        for file_path in discovered_files:
            self.console.print(f"  • {file_path}", style="dim")
        self.console.print()

    def print_error(self, message: str) -> None:
        """Print error message"""
        self.console.print(f"❌ Error: {message}", style="red")

    def print_warning(self, message: str) -> None:
        """Print warning message"""
        self.console.print(f"⚠️  Warning: {message}", style="yellow")
