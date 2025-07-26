#!/usr/bin/env python3
"""
Command-line interface for Natest.

Copyright © 2025 Aitomatic, Inc. Licensed under the MIT License.
"""

import logging
import sys
from pathlib import Path

import click

from .discovery import DanaTestDiscovery, DiscoveryConfig
from .executor import DanaTestExecutor
from .reporter import DanaTestReporter

# Configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version="0.1.0", prog_name="natest")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output and debug logging")
@click.option(
    "--pattern", "-p", multiple=True, help="Test file patterns (default: test_*.na, *_test.na)"
)
@click.option("--discover-only", is_flag=True, help="Only discover test files, don't execute them")
@click.argument("test_paths", nargs=-1, type=click.Path(exists=True))
def main(
    verbose: bool, pattern: tuple[str, ...], discover_only: bool, test_paths: tuple[str, ...]
) -> None:
    """
    Natest: Testing framework for Dana language files.

    Discovers and runs tests in .na (Dana) files.

    Examples:
        natest tests/                    # Run all tests in tests/ directory
        natest test_example.na           # Run specific test file
        natest --discover-only tests/    # Only show discovered files
        natest -v tests/                 # Verbose output
    """
    # Configure logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("natest").setLevel(logging.DEBUG)

    # Initialize components
    reporter = DanaTestReporter(use_color=True, verbose=verbose)

    # Show header
    click.echo("🧪 Natest - Testing framework for Dana language")
    if verbose:
        click.echo("Debug logging enabled")

    # Determine test paths
    if not test_paths:
        # Default to tests directory if it exists, otherwise current directory
        default_path = Path("tests")
        paths = [default_path] if default_path.exists() else [Path(".")]
    else:
        paths = [Path(p) for p in test_paths]

    # Configure discovery
    config = DiscoveryConfig()
    if pattern:
        config.patterns = list(pattern)

    discovery = DanaTestDiscovery(config)

    try:
        # Discover test files
        discovered_files = discovery.discover(paths)

        if not discovered_files:
            reporter.print_warning("No Dana test files found")
            click.echo("\nTip: Ensure test files match patterns like 'test_*.na' or '*_test.na'")
            sys.exit(1)

        # Show discovered files
        if verbose or discover_only:
            file_paths = [str(f) for f in discovered_files]
            reporter.print_discovery_results(file_paths)

        if discover_only:
            click.echo(f"Discovery complete: {len(discovered_files)} test file(s) found")
            sys.exit(0)

        # Execute tests
        executor = DanaTestExecutor()

        # Check if Dana is available
        if not executor.is_dana_available():
            reporter.print_warning(
                "Dana command not available. Test files will be discovered but not executed."
            )
            reporter.print_warning("Install Dana or ensure 'dana' command is in PATH to run tests.")
            # Still show discovery results
            file_paths = [str(f) for f in discovered_files]
            reporter.print_discovery_results(file_paths)
            sys.exit(2)

        # Run the tests
        results = executor.run_multiple_files(discovered_files)

        # Generate report
        reporter.generate_report(results)

        # Exit with appropriate code
        failed_count = sum(1 for r in results if not r.success)
        if failed_count > 0:
            sys.exit(1)  # Test failures
        else:
            sys.exit(0)  # Success

    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        reporter.print_error(str(e))
        if verbose:
            logger.exception("Unexpected error in natest")
        sys.exit(2)


if __name__ == "__main__":
    main()
