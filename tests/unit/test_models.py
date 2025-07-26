"""
Unit tests for Dana test data models.
"""

from pathlib import Path

from datest.models import DanaAssertion, DanaTestFile, DanaTestResult


class TestDanaTestFile:
    """Test DanaTestFile dataclass"""
    
    def test_basic_creation(self):
        """Test creating a DanaTestFile"""
        path = Path("test_example.na")
        test_file = DanaTestFile(path=path, name="test_example.na")
        
        assert test_file.path == path
        assert test_file.name == "test_example.na"
    
    def test_auto_name_from_path(self):
        """Test automatic name extraction from path"""
        path = Path("/some/path/test_example.na")
        test_file = DanaTestFile(path=path, name="")
        
        # Post-init should set name from path
        assert test_file.name == "test_example.na"


class TestDanaAssertion:
    """Test DanaAssertion dataclass"""
    
    def test_basic_creation(self):
        """Test creating a DanaAssertion"""
        assertion = DanaAssertion(
            line_number=10,
            assertion_type="assert",
            message="x == 5",
            passed=True
        )
        
        assert assertion.line_number == 10
        assert assertion.assertion_type == "assert"
        assert assertion.message == "x == 5"
        assert assertion.passed is True
        assert assertion.source_line is None
    
    def test_string_representation(self):
        """Test string representation of assertions"""
        # Passing assertion
        assertion_pass = DanaAssertion(
            line_number=10,
            assertion_type="assert",
            message="x == 5",
            passed=True
        )
        assert str(assertion_pass) == "✅ Line 10: x == 5"
        
        # Failing assertion
        assertion_fail = DanaAssertion(
            line_number=20,
            assertion_type="assert",
            message="y != 10",
            passed=False
        )
        assert str(assertion_fail) == "❌ Line 20: y != 10"


class TestDanaTestResult:
    """Test DanaTestResult dataclass"""
    
    def test_basic_creation(self):
        """Test creating a DanaTestResult"""
        path = Path("test_example.na")
        result = DanaTestResult(
            file_path=path,
            success=True,
            duration=1.5
        )
        
        assert result.file_path == path
        assert result.success is True
        assert result.duration == 1.5
        assert result.output == ""
        assert result.errors == ""
        assert result.exit_code == 0
        assert result.assertions == []
    
    def test_with_assertions(self):
        """Test result with assertions"""
        path = Path("test_example.na")
        assertions = [
            DanaAssertion(line_number=10, assertion_type="assert", message="x == 5", passed=True),
            DanaAssertion(line_number=20, assertion_type="assert", message="y != 10", passed=False),
            DanaAssertion(line_number=30, assertion_type="log", message="Test log", passed=True),
        ]
        
        result = DanaTestResult(
            file_path=path,
            success=False,
            duration=2.0,
            assertions=assertions
        )
        
        assert len(result.assertions) == 3
        assert len(result.passed_assertions) == 2
        assert len(result.failed_assertions) == 1
    
    def test_test_name(self):
        """Test extracting test name from path"""
        path = Path("/path/to/test_example.na")
        result = DanaTestResult(
            file_path=path,
            success=True,
            duration=1.0
        )
        
        assert result.test_name == "test_example"
    
    def test_has_errors(self):
        """Test error detection"""
        path = Path("test.na")
        
        # No errors
        result1 = DanaTestResult(
            file_path=path,
            success=True,
            duration=1.0
        )
        assert result1.has_errors() is False
        
        # With error text
        result2 = DanaTestResult(
            file_path=path,
            success=False,
            duration=1.0,
            errors="Some error occurred"
        )
        assert result2.has_errors() is True
        
        # With non-zero exit code
        result3 = DanaTestResult(
            file_path=path,
            success=False,
            duration=1.0,
            exit_code=1
        )
        assert result3.has_errors() is True
    
    def test_summary(self):
        """Test summary generation"""
        path = Path("test_math.na")
        assertions = [
            DanaAssertion(line_number=10, assertion_type="assert", message="2+2==4", passed=True),
            DanaAssertion(line_number=20, assertion_type="assert", message="3*3==9", passed=True),
            DanaAssertion(line_number=30, assertion_type="assert", message="10/0", passed=False),
        ]
        
        result = DanaTestResult(
            file_path=path,
            success=False,
            duration=1.5,
            assertions=assertions
        )
        
        summary = result.summary()
        assert "test_math" in summary
        assert "FAILED" in summary
        assert "2/3" in summary  # 2 passed out of 3 assertions
        assert "1.50s" in summary