"""
Unit tests for Dana test discovery functionality.
"""

from pathlib import Path
from unittest.mock import patch

from natest.discovery import DanaTestDiscovery, DiscoveryConfig


class TestDiscoveryConfig:
    """Test DiscoveryConfig dataclass"""

    def test_default_config(self):
        """Test default configuration values"""
        config = DiscoveryConfig()

        assert config.patterns == ["test_*.na", "*_test.na"]
        assert config.recursive is True
        assert config.max_depth == 10
        assert ".*" in config.exclude_patterns
        assert "__pycache__" in config.exclude_patterns


class TestDanaTestDiscovery:
    """Test DanaTestDiscovery class"""

    def test_init_default_config(self):
        """Test initialization with default config"""
        discovery = DanaTestDiscovery()

        assert discovery.config is not None
        assert discovery.config.patterns == ["test_*.na", "*_test.na"]

    def test_init_custom_config(self):
        """Test initialization with custom config"""
        config = DiscoveryConfig(patterns=["custom_*.na"])
        discovery = DanaTestDiscovery(config)

        assert discovery.config.patterns == ["custom_*.na"]

    def test_is_test_file_valid_patterns(self):
        """Test _is_test_file with valid test file patterns"""
        discovery = DanaTestDiscovery()

        # Test default patterns
        assert discovery._is_test_file(Path("test_example.na")) is True
        assert discovery._is_test_file(Path("example_test.na")) is True
        assert discovery._is_test_file(Path("test_basic_math.na")) is True
        assert discovery._is_test_file(Path("complex_test.na")) is True

    def test_is_test_file_invalid_patterns(self):
        """Test _is_test_file with invalid patterns"""
        discovery = DanaTestDiscovery()

        # Wrong extension
        assert discovery._is_test_file(Path("test_example.py")) is False

        # Wrong naming pattern
        assert discovery._is_test_file(Path("example.na")) is False
        assert discovery._is_test_file(Path("random_file.na")) is False

        # No extension
        assert discovery._is_test_file(Path("test_example")) is False

    def test_is_test_file_custom_patterns(self):
        """Test _is_test_file with custom patterns"""
        config = DiscoveryConfig(patterns=["spec_*.na", "*.spec.na"])
        discovery = DanaTestDiscovery(config)

        assert discovery._is_test_file(Path("spec_example.na")) is True
        assert discovery._is_test_file(Path("example.spec.na")) is True
        assert discovery._is_test_file(Path("test_example.na")) is False

    def test_is_excluded(self):
        """Test _is_excluded method"""
        discovery = DanaTestDiscovery()

        # Test default exclude patterns
        assert discovery._is_excluded(Path(".hidden_file")) is True
        assert discovery._is_excluded(Path("__pycache__")) is True
        assert discovery._is_excluded(Path("test.egg-info")) is True

        # Should not be excluded
        assert discovery._is_excluded(Path("test_example.na")) is False
        assert discovery._is_excluded(Path("normal_file.txt")) is False

    def test_remove_duplicates(self):
        """Test _remove_duplicates method"""
        discovery = DanaTestDiscovery()

        # Create some paths (using strings since we don't need real files)
        path1 = Path("test1.na")
        path2 = Path("test2.na")
        path1_dup = Path("test1.na")

        files = [path1, path2, path1_dup, path2]
        unique_files = discovery._remove_duplicates(files)

        # Should remove duplicates while preserving order
        assert len(unique_files) == 2
        assert unique_files[0] == path1
        assert unique_files[1] == path2

    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.is_file")
    def test_walk_directory(self, mock_is_file, mock_is_dir, mock_iterdir):
        """Test _walk_directory method"""
        discovery = DanaTestDiscovery()

        # Mock directory structure
        test_file = Path("test_example.na")
        regular_file = Path("example.py")

        mock_iterdir.return_value = [test_file, regular_file]
        mock_is_file.side_effect = lambda: True
        mock_is_dir.side_effect = lambda: False

        # Mock the _is_test_file method to return True for .na files
        with patch.object(discovery, "_is_test_file") as mock_is_test:
            mock_is_test.side_effect = lambda p: p.suffix == ".na" and "test_" in p.name

            result = discovery._walk_directory(Path("test_dir"))

            assert len(result) == 1
            assert result[0] == test_file

    def test_discover_single_file(self):
        """Test discover method with single file"""
        discovery = DanaTestDiscovery()

        # Create a temporary test file path
        test_file = Path("test_example.na")

        with (
            patch.object(Path, "is_file", return_value=True),
            patch.object(Path, "is_dir", return_value=False),
            patch.object(discovery, "_is_test_file", return_value=True),
        ):
            result = discovery.discover([test_file])

            assert len(result) == 1
            assert result[0] == test_file

    def test_discover_directory(self):
        """Test discover method with directory"""
        discovery = DanaTestDiscovery()

        test_dir = Path("tests")

        with (
            patch.object(Path, "is_file", return_value=False),
            patch.object(Path, "is_dir", return_value=True),
            patch.object(discovery, "_walk_directory") as mock_walk,
        ):
            mock_walk.return_value = [Path("test1.na"), Path("test2.na")]

            result = discovery.discover([test_dir])

            assert len(result) == 2
            mock_walk.assert_called_once_with(test_dir)

    def test_discover_nonexistent_path(self):
        """Test discover method with nonexistent path"""
        discovery = DanaTestDiscovery()

        nonexistent_path = Path("nonexistent")

        with (
            patch.object(Path, "is_file", return_value=False),
            patch.object(Path, "is_dir", return_value=False),
        ):
            # Should handle gracefully and return empty list
            result = discovery.discover([nonexistent_path])

            assert result == []

    def test_discover_empty_result(self):
        """Test discover method when no files found"""
        discovery = DanaTestDiscovery()

        test_dir = Path("tests")

        with (
            patch.object(Path, "is_file", return_value=False),
            patch.object(Path, "is_dir", return_value=True),
            patch.object(discovery, "_walk_directory", return_value=[]),
        ):
            result = discovery.discover([test_dir])

            assert result == []
