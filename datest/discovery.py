"""
Test file discovery for Dana test files.

Finds .na files matching test patterns in directories.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DiscoveryConfig:
    """Configuration for test discovery"""

    patterns: list[str] = field(default_factory=lambda: ["test_*.na", "*_test.na"])
    recursive: bool = True
    max_depth: int = 10
    exclude_patterns: list[str] = field(default_factory=lambda: [".*", "__pycache__", "*.egg-info"])


class DanaTestDiscovery:
    """Discovers Dana test files in file system"""

    def __init__(self, config: DiscoveryConfig | None = None):
        self.config = config or DiscoveryConfig()
        logger.debug(f"Initialized discovery with patterns: {self.config.patterns}")

    def discover(self, paths: list[Path]) -> list[Path]:
        """
        Discover test files in given paths

        Args:
            paths: List of file/directory paths to search

        Returns:
            List of discovered test file paths sorted by name
        """
        discovered_files: list[Path] = []

        for path in paths:
            try:
                if path.is_file():
                    # Single file case
                    if self._is_test_file(path):
                        discovered_files.append(path)
                        logger.debug(f"Discovered test file: {path}")
                elif path.is_dir():
                    # Directory case - recursive walk
                    found_files = self._walk_directory(path)
                    discovered_files.extend(found_files)
                    logger.debug(f"Discovered {len(found_files)} files in {path}")
                else:
                    logger.warning(f"Path does not exist: {path}")
            except Exception as e:
                logger.error(f"Error discovering tests in {path}: {e}")

        # Remove duplicates while preserving order
        unique_files = self._remove_duplicates(discovered_files)

        # Sort for consistent output
        unique_files.sort()

        logger.info(f"Discovery completed: {len(unique_files)} test files found")
        return unique_files

    def _walk_directory(self, directory: Path, depth: int = 0) -> list[Path]:
        """Recursively walk directory to find test files"""
        if depth > self.config.max_depth:
            logger.debug(f"Max depth {self.config.max_depth} reached for {directory}")
            return []

        found_files: list[Path] = []

        try:
            for item in directory.iterdir():
                if self._is_excluded(item):
                    continue

                if item.is_file() and self._is_test_file(item):
                    found_files.append(item)
                elif item.is_dir() and self.config.recursive:
                    sub_files = self._walk_directory(item, depth + 1)
                    found_files.extend(sub_files)
        except PermissionError:
            logger.warning(f"Permission denied accessing {directory}")
        except Exception as e:
            logger.error(f"Error walking directory {directory}: {e}")

        return found_files

    def _is_test_file(self, path: Path) -> bool:
        """Check if file matches test patterns"""
        if path.suffix != ".na":
            return False

        filename = path.name
        for pattern in self.config.patterns:
            # Use simple glob-like matching
            if self._matches_glob_pattern(filename, pattern):
                return True

        return False

    def _matches_glob_pattern(self, filename: str, pattern: str) -> bool:
        """Simple glob pattern matching for test file names"""
        # Handle simple wildcard patterns
        if "*" not in pattern:
            # Exact match
            return filename == pattern

        # Split pattern on '*' and check each part
        parts = pattern.split("*")

        if len(parts) == 2:
            # Single wildcard: either prefix* or *suffix or prefix*suffix
            prefix, suffix = parts

            if prefix and suffix:
                # prefix*suffix pattern (e.g., "test_*.na")
                return filename.startswith(prefix) and filename.endswith(suffix)
            elif prefix:
                # prefix* pattern (e.g., "test_*")
                return filename.startswith(prefix)
            elif suffix:
                # *suffix pattern (e.g., "*_test.na")
                return filename.endswith(suffix)
            else:
                # Just "*" matches everything
                return True

        # Multiple wildcards - more complex pattern
        # For now, just check if all non-wildcard parts are in the filename
        non_wildcard_parts = [part for part in parts if part]
        return all(part in filename for part in non_wildcard_parts)

    def _is_excluded(self, path: Path) -> bool:
        """Check if path should be excluded"""
        name = path.name
        for exclude_pattern in self.config.exclude_patterns:
            if exclude_pattern.startswith(".") and name.startswith("."):
                return True
            elif "*" in exclude_pattern:
                # Handle wildcard patterns like "*.egg-info"
                if self._matches_glob_pattern(name, exclude_pattern):
                    return True
            elif exclude_pattern in name:
                return True
        return False

    def _remove_duplicates(self, files: list[Path]) -> list[Path]:
        """Remove duplicate paths while preserving order"""
        seen = set()
        unique_files = []
        for file_path in files:
            # Use resolved path to handle symlinks and relative paths
            resolved_path = file_path.resolve()
            if resolved_path not in seen:
                seen.add(resolved_path)
                unique_files.append(file_path)
        return unique_files
