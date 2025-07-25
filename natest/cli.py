#!/usr/bin/env python3
"""
Command-line interface for Natest.

Copyright © 2025 Aitomatic, Inc. Licensed under the MIT License.
"""

import sys
from typing import Optional

import click


@click.command()
@click.version_option(version="0.1.0", prog_name="natest")
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.argument("test_files", nargs=-1, type=click.Path(exists=True))
def main(verbose: bool, test_files: tuple[str, ...]) -> None:
    """
    Natest: Pytest-inspired testing framework for Dana language files.
    
    Run tests on .na (Dana) files or Python test files.
    """
    click.echo("🧪 Natest - Testing framework for Dana language")
    
    if verbose:
        click.echo("Verbose mode enabled")
    
    if not test_files:
        click.echo("No test files specified. Looking for test files...")
        # TODO: Implement automatic test discovery
        click.echo("⚠️  No test files found. Please specify test files to run.")
        return
    
    click.echo(f"Running tests on {len(test_files)} file(s):")
    for test_file in test_files:
        click.echo(f"  • {test_file}")
    
    # TODO: Implement actual test execution logic
    click.echo("✅ Test framework initialized successfully!")
    click.echo("⚠️  Test execution not yet implemented.")


if __name__ == "__main__":
    main() 