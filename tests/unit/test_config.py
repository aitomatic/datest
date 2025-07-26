"""
Unit tests for datest configuration management.
"""

from pathlib import Path
import tempfile
import textwrap
from unittest.mock import patch, mock_open

from datest.config import DatestConfig


class TestDatestConfig:
    """Test DatestConfig class"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = DatestConfig()
        
        # Test discovery defaults
        assert config.test_patterns == ["test_*.na", "*_test.na"]
        assert config.exclude_patterns == [".*", "__pycache__", "*.egg-info"]
        assert config.recursive is True
        assert config.max_depth == 10
        
        # Test execution defaults
        assert config.dana_command == "dana"
        assert config.timeout == 30.0
        assert config.use_json_output is False
        
        # Test output defaults
        assert config.verbose is False
        assert config.use_color is True
        assert config.show_timings is True
        
        # Test pytest defaults
        assert config.enable_pytest_plugin is True
    
    def test_from_dict(self):
        """Test creating config from dictionary"""
        data = {
            "discovery": {
                "patterns": ["spec_*.na"],
                "exclude": ["temp", "build"],
                "recursive": False,
                "max_depth": 5
            },
            "execution": {
                "command": "/usr/bin/dana",
                "timeout": 60.0,
                "json_output": True
            },
            "output": {
                "verbose": True,
                "color": False,
                "timings": False
            },
            "pytest": {
                "enable": False
            }
        }
        
        config = DatestConfig.from_dict(data)
        
        # Test discovery settings
        assert config.test_patterns == ["spec_*.na"]
        assert config.exclude_patterns == ["temp", "build"]
        assert config.recursive is False
        assert config.max_depth == 5
        
        # Test execution settings
        assert config.dana_command == "/usr/bin/dana"
        assert config.timeout == 60.0
        assert config.use_json_output is True
        
        # Test output settings
        assert config.verbose is True
        assert config.use_color is False
        assert config.show_timings is False
        
        # Test pytest settings
        assert config.enable_pytest_plugin is False
    
    def test_partial_dict(self):
        """Test creating config from partial dictionary"""
        data = {
            "discovery": {
                "patterns": ["custom_*.na"]
            },
            "execution": {
                "timeout": 45.0
            }
        }
        
        config = DatestConfig.from_dict(data)
        
        # Changed values
        assert config.test_patterns == ["custom_*.na"]
        assert config.timeout == 45.0
        
        # Defaults should remain
        assert config.recursive is True
        assert config.dana_command == "dana"
        assert config.use_color is True
    
    def test_to_dict(self):
        """Test converting config to dictionary"""
        config = DatestConfig()
        config.test_patterns = ["spec_*.na"]
        config.timeout = 45.0
        config.verbose = True
        
        data = config.to_dict()
        
        assert data["discovery"]["patterns"] == ["spec_*.na"]
        assert data["execution"]["timeout"] == 45.0
        assert data["output"]["verbose"] is True
    
    def test_load_from_file(self):
        """Test loading config from TOML file"""
        toml_content = '''
[discovery]
patterns = ["spec_*.na", "test_*.dana"]
exclude = ["vendor", "node_modules"]

[execution]
command = "dana-test"
timeout = 120.0

[output]
verbose = true
color = false
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(toml_content)
            f.flush()
            
            config = DatestConfig.load_from_file(Path(f.name))
            
            assert config.test_patterns == ["spec_*.na", "test_*.dana"]
            assert config.exclude_patterns == ["vendor", "node_modules"]
            assert config.dana_command == "dana-test"
            assert config.timeout == 120.0
            assert config.verbose is True
            assert config.use_color is False
        
        # Clean up
        Path(f.name).unlink()
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file returns defaults"""
        config = DatestConfig.load_from_file(Path("nonexistent.toml"))
        
        # Should return default config
        assert config.test_patterns == ["test_*.na", "*_test.na"]
        assert config.dana_command == "dana"
    
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_find_and_load_from_cwd(self, mock_file, mock_exists):
        """Test finding and loading config from current directory"""
        # Mock datest.toml exists in current directory
        def exists_side_effect(self):
            return str(self).endswith("datest.toml") and "parent" not in str(self)
        
        mock_exists.side_effect = exists_side_effect
        
        toml_content = '''
[discovery]
patterns = ["found_*.na"]
        '''
        mock_file.return_value.read.return_value = toml_content.encode()
        
        with patch("datest.config.tomllib.load") as mock_load:
            mock_load.return_value = {"discovery": {"patterns": ["found_*.na"]}}
            
            config = DatestConfig.find_and_load()
            
            assert config.test_patterns == ["found_*.na"]
    
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_from_pyproject_toml(self, mock_file, mock_exists):
        """Test loading from pyproject.toml [tool.datest] section"""
        # Mock pyproject.toml exists
        def exists_side_effect(self):
            return str(self).endswith("pyproject.toml")
        
        mock_exists.side_effect = exists_side_effect
        
        pyproject_content = '''
[tool.datest]
[tool.datest.discovery]
patterns = ["pyproject_*.na"]

[tool.datest.execution]
timeout = 90.0
        '''
        
        with patch("datest.config.tomllib.load") as mock_load:
            mock_load.return_value = {
                "tool": {
                    "datest": {
                        "discovery": {"patterns": ["pyproject_*.na"]},
                        "execution": {"timeout": 90.0}
                    }
                }
            }
            
            config = DatestConfig.find_and_load()
            
            assert config.test_patterns == ["pyproject_*.na"]
            assert config.timeout == 90.0
    
    def test_empty_dict_uses_defaults(self):
        """Test that empty dict results in default config"""
        config = DatestConfig.from_dict({})
        
        assert config.test_patterns == ["test_*.na", "*_test.na"]
        assert config.dana_command == "dana"
        assert config.timeout == 30.0