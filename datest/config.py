"""
Configuration management for datest.

Handles loading and parsing configuration from datest.toml files.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import tomllib
except ImportError:
    # Python < 3.11
    import tomli as tomllib

logger = logging.getLogger(__name__)


@dataclass
class DatestConfig:
    """Configuration for datest framework"""

    # Test discovery settings
    test_patterns: list[str] = field(default_factory=lambda: ["test_*.na", "*_test.na"])
    exclude_patterns: list[str] = field(default_factory=lambda: [".*", "__pycache__", "*.egg-info"])
    recursive: bool = True
    max_depth: int = 10

    # Dana execution settings
    dana_command: str = "dana"
    timeout: float = 30.0
    use_json_output: bool = False

    # Output settings
    verbose: bool = False
    use_color: bool = True
    show_timings: bool = True

    # pytest integration
    enable_pytest_plugin: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DatestConfig":
        print(f"DEBUG from_dict data: {data}")  # DEBUG
        config = cls()

        # Test discovery settings
        if "discovery" in data:
            discovery = data["discovery"]
            config.test_patterns = discovery.get("patterns", config.test_patterns)
            config.exclude_patterns = discovery.get("exclude", config.exclude_patterns)
            config.recursive = discovery.get("recursive", config.recursive)
            config.max_depth = discovery.get("max_depth", config.max_depth)

        # Dana execution settings
        if "execution" in data:
            execution = data["execution"]
            config.dana_command = execution.get("command", config.dana_command)
            config.timeout = execution.get("timeout", config.timeout)
            config.use_json_output = execution.get("json_output", config.use_json_output)

        # Output settings
        if "output" in data:
            output = data["output"]
            config.verbose = output.get("verbose", config.verbose)
            config.use_color = output.get("color", config.use_color)
            config.show_timings = output.get("timings", config.show_timings)

        # pytest settings
        if "pytest" in data:
            pytest_config = data["pytest"]
            config.enable_pytest_plugin = pytest_config.get("enable", config.enable_pytest_plugin)

        return config

    @classmethod
    def load_from_file(cls, path: Path) -> "DatestConfig":
        """Load configuration from TOML file"""
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)

            logger.debug(f"Loaded configuration from {path}")
            return cls.from_dict(data)

        except FileNotFoundError:
            logger.debug(f"Config file not found: {path}")
            return cls()
        except Exception as e:
            logger.warning(f"Error loading config from {path}: {e}")
            return cls()

    @classmethod
    def find_and_load(cls, start_path: Path | None = None) -> "DatestConfig":
        """Find and load configuration file"""
        if start_path is None:
            start_path = Path.cwd()

        # Look for config file in current and parent directories
        current = start_path.resolve()

        while current != current.parent:
            config_path = current / "datest.toml"
            if config_path.exists():
                return cls.load_from_file(config_path)

            # Also check for pyproject.toml with [tool.datest] section
            pyproject_path = current / "pyproject.toml"
            if pyproject_path.exists():
                config = cls._load_from_pyproject(pyproject_path)
                if config:
                    return config

            current = current.parent

        # No config file found, use defaults
        logger.debug("No configuration file found, using defaults")
        return cls()

    @classmethod
    def _load_from_pyproject(cls, path: Path) -> Optional["DatestConfig"]:
        """Load configuration from pyproject.toml [tool.datest] section"""
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)

            if "tool" in data and "datest" in data["tool"]:
                logger.debug(f"Loaded datest config from {path}")
                return cls.from_dict(data["tool"]["datest"])

        except Exception as e:
            logger.debug(f"Error loading from pyproject.toml: {e}")

        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for serialization"""
        return {
            "discovery": {
                "patterns": self.test_patterns,
                "exclude": self.exclude_patterns,
                "recursive": self.recursive,
                "max_depth": self.max_depth,
            },
            "execution": {
                "command": self.dana_command,
                "timeout": self.timeout,
                "json_output": self.use_json_output,
            },
            "output": {
                "verbose": self.verbose,
                "color": self.use_color,
                "timings": self.show_timings,
            },
            "pytest": {
                "enable": self.enable_pytest_plugin,
            },
        }


# Example configuration file content
EXAMPLE_CONFIG = """# datest.toml - Configuration for Dana test framework

[discovery]
# Patterns for test file discovery
patterns = ["test_*.na", "*_test.na"]
# Patterns to exclude from discovery
exclude = [".*", "__pycache__", "*.egg-info"]
# Recursively search directories
recursive = true
# Maximum directory depth for recursive search
max_depth = 10

[execution]
# Path to Dana command
command = "dana"
# Timeout for test execution (seconds)
timeout = 30.0
# Use JSON output format
json_output = false

[output]
# Verbose output
verbose = false
# Use colored output
color = true
# Show test execution timings
timings = true

[pytest]
# Enable pytest plugin for .na files
enable = true
"""
