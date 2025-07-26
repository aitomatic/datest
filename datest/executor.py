"""
Dana test execution using existing Dana runtime.

Executes .na files using subprocess calls to Dana command.
"""

import logging
import subprocess
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DanaTestResult:
    """Result of running a Dana test file"""

    def __init__(
        self,
        file_path: Path,
        success: bool,
        duration: float,
        output: str = "",
        errors: str = "",
        exit_code: int = 0,
    ):
        self.file_path = file_path
        self.success = success
        self.duration = duration
        self.output = output
        self.errors = errors
        self.exit_code = exit_code
        self.assertions = self._parse_assertions()

    def _parse_assertions(self) -> list:
        """Parse assertions from Dana output (basic implementation)"""
        # For Phase 1: basic parsing of log statements and errors
        assertions = []

        # Look for common assertion patterns in output
        lines = self.output.split("\n")
        for i, line in enumerate(lines):
            if "✅" in line:
                assertions.append({"line": i + 1, "type": "pass", "message": line.strip()})
            elif "❌" in line or "Error:" in line:
                assertions.append({"line": i + 1, "type": "fail", "message": line.strip()})

        return assertions


class DanaTestExecutor:
    """Executes Dana test cases using existing Dana runtime"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.timeout = self.config.get("timeout", 30.0)
        self.dana_command = self.config.get("dana_command", "dana")
        logger.debug(f"Initialized executor with timeout: {self.timeout}s")

    def run_dana_file(self, file_path: Path) -> DanaTestResult:
        """
        Execute Dana test file using existing runtime

        Args:
            file_path: Path to Dana test file

        Returns:
            DanaTestResult with execution results
        """
        logger.info(f"Executing Dana file: {file_path}")
        start_time = time.time()

        try:
            # Try to run with Dana command
            result = self._run_subprocess(file_path)
            duration = time.time() - start_time

            success = result.returncode == 0

            logger.debug(
                f"Dana execution completed in {duration:.2f}s, exit code: {result.returncode}"
            )

            return DanaTestResult(
                file_path=file_path,
                success=success,
                duration=duration,
                output=result.stdout,
                errors=result.stderr,
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            logger.error(f"Dana execution timed out after {self.timeout}s")
            return DanaTestResult(
                file_path=file_path,
                success=False,
                duration=duration,
                output="",
                errors=f"Execution timed out after {self.timeout}s",
                exit_code=124,  # Standard timeout exit code
            )
        except FileNotFoundError:
            duration = time.time() - start_time
            logger.error(f"Dana command not found: {self.dana_command}")
            return DanaTestResult(
                file_path=file_path,
                success=False,
                duration=duration,
                output="",
                errors=f"Dana command not found: {self.dana_command}",
                exit_code=127,  # Command not found
            )
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Unexpected error executing Dana file: {e}")
            return DanaTestResult(
                file_path=file_path,
                success=False,
                duration=duration,
                output="",
                errors=f"Execution error: {e}",
                exit_code=1,
            )

    def _run_subprocess(self, file_path: Path) -> subprocess.CompletedProcess:
        """Run Dana file using subprocess"""
        cmd = [self.dana_command, str(file_path)]

        logger.debug(f"Running command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            cwd=file_path.parent,  # Run in the test file's directory
        )

        return result

    def run_multiple_files(self, file_paths: list[Path]) -> list[DanaTestResult]:
        """
        Run multiple Dana test files sequentially

        Args:
            file_paths: List of Dana test file paths

        Returns:
            List of DanaTestResult objects
        """
        results = []

        logger.info(f"Running {len(file_paths)} Dana test files")

        for file_path in file_paths:
            result = self.run_dana_file(file_path)
            results.append(result)

        return results

    def is_dana_available(self) -> bool:
        """Check if Dana command is available"""
        try:
            result = subprocess.run(
                [self.dana_command, "--version"], capture_output=True, timeout=5.0
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
