#!/usr/bin/env python3
"""
Command-line interface for Datest.

Copyright © 2025 Aitomatic, Inc. Licensed under the MIT License.
"""

import logging
import sys
from pathlib import Path

import click

from .config import DatestConfig
from .discovery import DanaTestDiscovery, DiscoveryConfig
from .executor import DanaTestExecutor
from .reporter import DanaTestReporter

# Configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version="0.1.0", prog_name="datest")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output and debug logging")
@click.option(
    "--pattern", "-p", multiple=True, help="Test file patterns (default: test_*.na, *_test.na)"
)
@click.option("--discover-only", is_flag=True, help="Only discover test files, don't execute them")
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to configuration file")
@click.option("--json", is_flag=True, help="Use JSON output format for Dana tests")
@click.option("--timeout", "-t", type=float, help="Timeout for test execution in seconds")
@click.option("--no-color", is_flag=True, help="Disable colored output")
@click.argument("test_paths", nargs=-1, type=click.Path(exists=True))
def main(
    verbose: bool,
    pattern: tuple[str, ...],
    discover_only: bool,
    config: str | None,
    json: bool,
    timeout: float | None,
    no_color: bool,
    test_paths: tuple[str, ...],
) -> None:
    """
    Datest: Testing framework for Dana language files.

    Discovers and runs tests in .na (Dana) files.

    Examples:
        datest tests/                    # Run all tests in tests/ directory
        datest test_example.na           # Run specific test file
        datest --discover-only tests/    # Only show discovered files
        datest -v tests/                 # Verbose output
    """
    # Load configuration
    if config:
        config_path = Path(config)
        datest_config = DatestConfig.load_from_file(config_path)
    else:
        datest_config = DatestConfig.find_and_load()

    # Apply command line overrides
    if verbose:
        datest_config.verbose = True
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("datest").setLevel(logging.DEBUG)

    if json:
        datest_config.use_json_output = True

    if timeout is not None:
        datest_config.timeout = timeout

    if no_color:
        datest_config.use_color = False

    # Initialize components
    reporter = DanaTestReporter(use_color=datest_config.use_color, verbose=datest_config.verbose)

    # Show header
    click.echo("🧪 Datest - Testing framework for Dana language")
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
    discovery_config = DiscoveryConfig(
        patterns=datest_config.test_patterns if not pattern else list(pattern),
        exclude_patterns=datest_config.exclude_patterns,
        recursive=datest_config.recursive,
        max_depth=datest_config.max_depth,
    )

    discovery = DanaTestDiscovery(discovery_config)

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
        executor_config = {
            "dana_command": datest_config.dana_command,
            "timeout": datest_config.timeout,
            "use_json_output": datest_config.use_json_output,
        }
        executor = DanaTestExecutor(executor_config)

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
            logger.exception("Unexpected error in datest")
        sys.exit(2)


if __name__ == "__main__":
    main()
