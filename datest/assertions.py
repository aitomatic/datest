"""
Dana assertion parsing and pattern matching.

Parses Dana output to extract assertions, log statements, and test results.
"""

import json
import logging
import re
from typing import List, Optional, Tuple

from .models import DanaAssertion

logger = logging.getLogger(__name__)


class DanaAssertionParser:
    """Parses Dana test output to extract assertions and results"""
    
    # Pattern to match Dana assert statements in output
    ASSERT_PATTERN = re.compile(
        r'(?:Line\s+(\d+):\s*)?'  # Optional line number
        r'(assert(?:ion)?)\s+'     # assert/assertion keyword
        r'(.+?)\s*'                # assertion expression
        r'(?:failed|passed|==|!=)'  # Result indicator
    )
    
    # Pattern to match Dana log statements
    LOG_PATTERN = re.compile(
        r'(?:Line\s+(\d+):\s*)?'   # Optional line number
        r'log\s*\(\s*["\']?'       # log( with optional quote
        r'(.+?)'                   # log message
        r'["\']?\s*\)'            # closing quote and paren
    )
    
    # Pattern to match error messages
    ERROR_PATTERN = re.compile(
        r'(?:Line\s+(\d+):\s*)?'   # Optional line number
        r'(Error|Exception):\s*'   # Error type
        r'(.+)'                   # Error message
    )
    
    # Patterns for test status indicators
    PASS_INDICATORS = ["✅", "passed", "success", "ok", "PASS"]
    FAIL_INDICATORS = ["❌", "failed", "failure", "error", "FAIL", "AssertionError"]
    
    def parse_output(self, output: str, error_output: str = "") -> List[DanaAssertion]:
        """
        Parse Dana test output to extract assertions
        
        Args:
            output: Standard output from Dana execution
            error_output: Standard error output from Dana execution
            
        Returns:
            List of DanaAssertion objects
        """
        assertions = []
        
        # First try to parse as JSON (if Dana was run with --output-json)
        json_assertions = self._parse_json_output(output)
        if json_assertions:
            return json_assertions
        
        # Otherwise parse text output
        assertions.extend(self._parse_text_output(output))
        
        # Parse error output
        if error_output:
            assertions.extend(self._parse_error_output(error_output))
        
        # If no specific assertions found, check for general pass/fail
        if not assertions:
            assertions.extend(self._parse_generic_results(output))
        
        return assertions
    
    def _parse_json_output(self, output: str) -> Optional[List[DanaAssertion]]:
        """Try to parse JSON-formatted Dana output"""
        try:
            # Look for JSON in the output
            json_start = output.find('{')
            if json_start == -1:
                return None
                
            json_str = output[json_start:]
            data = json.loads(json_str)
            
            assertions = []
            
            # Parse test results from JSON
            if "tests" in data:
                for test in data["tests"]:
                    assertion = DanaAssertion(
                        line_number=test.get("line", 0),
                        assertion_type="assert",
                        message=test.get("message", ""),
                        passed=test.get("passed", False),
                        source_line=test.get("source", "")
                    )
                    assertions.append(assertion)
            
            # Parse logs from JSON
            if "logs" in data:
                for log in data["logs"]:
                    assertion = DanaAssertion(
                        line_number=log.get("line", 0),
                        assertion_type="log",
                        message=log.get("message", ""),
                        passed=True,  # Logs are informational
                        source_line=log.get("source", "")
                    )
                    assertions.append(assertion)
            
            return assertions
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.debug(f"Could not parse JSON output: {e}")
            return None
    
    def _parse_text_output(self, output: str) -> List[DanaAssertion]:
        """Parse text-based Dana output"""
        assertions = []
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for assertion patterns
            assertion = self._parse_assertion_line(line, i + 1)
            if assertion:
                assertions.append(assertion)
                continue
            
            # Check for log patterns
            log = self._parse_log_line(line, i + 1)
            if log:
                assertions.append(log)
                continue
        
        return assertions
    
    def _parse_assertion_line(self, line: str, default_line_num: int) -> Optional[DanaAssertion]:
        """Parse a single assertion line"""
        # Check for pass/fail indicators
        passed = any(indicator in line for indicator in self.PASS_INDICATORS)
        failed = any(indicator in line for indicator in self.FAIL_INDICATORS)
        
        if not (passed or failed):
            return None
        
        # Extract line number if present
        line_match = re.search(r'Line\s+(\d+)', line)
        line_number = int(line_match.group(1)) if line_match else default_line_num
        
        # Extract assertion details
        assert_match = self.ASSERT_PATTERN.search(line)
        if assert_match:
            return DanaAssertion(
                line_number=int(assert_match.group(1) or line_number),
                assertion_type="assert",
                message=assert_match.group(3).strip(),
                passed=passed and not failed
            )
        
        # Generic assertion based on indicators
        return DanaAssertion(
            line_number=line_number,
            assertion_type="assert",
            message=line.strip(),
            passed=passed and not failed
        )
    
    def _parse_log_line(self, line: str, default_line_num: int) -> Optional[DanaAssertion]:
        """Parse a log statement line"""
        # Look for log patterns
        if "log(" in line or "log " in line:
            # Extract message from log statement
            message = line
            if "log(" in line:
                start = line.find("log(") + 4
                end = line.rfind(")")
                if end > start:
                    message = line[start:end].strip().strip('"\'')
            
            return DanaAssertion(
                line_number=default_line_num,
                assertion_type="log",
                message=message,
                passed=True  # Logs are informational
            )
        
        return None
    
    def _parse_error_output(self, error_output: str) -> List[DanaAssertion]:
        """Parse error output for failures"""
        assertions = []
        lines = error_output.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for error patterns
            error_match = self.ERROR_PATTERN.search(line)
            if error_match:
                line_number = int(error_match.group(1)) if error_match.group(1) else 0
                error_type = error_match.group(2)
                message = error_match.group(3).strip()
                
                assertions.append(DanaAssertion(
                    line_number=line_number,
                    assertion_type="error",
                    message=f"{error_type}: {message}",
                    passed=False
                ))
            elif "Error" in line or "Exception" in line:
                # Generic error
                assertions.append(DanaAssertion(
                    line_number=0,
                    assertion_type="error",
                    message=line,
                    passed=False
                ))
        
        return assertions
    
    def _parse_generic_results(self, output: str) -> List[DanaAssertion]:
        """Parse generic test results when specific assertions not found"""
        assertions = []
        
        # Look for overall pass/fail indicators
        if any(indicator in output for indicator in self.PASS_INDICATORS):
            assertions.append(DanaAssertion(
                line_number=0,
                assertion_type="result",
                message="Test passed",
                passed=True
            ))
        elif any(indicator in output for indicator in self.FAIL_INDICATORS):
            assertions.append(DanaAssertion(
                line_number=0,
                assertion_type="result", 
                message="Test failed",
                passed=False
            ))
        
        return assertions
    
    def extract_test_summary(self, assertions: List[DanaAssertion]) -> Tuple[int, int]:
        """
        Extract test summary from assertions
        
        Returns:
            Tuple of (passed_count, failed_count)
        """
        passed = sum(1 for a in assertions if a.passed and a.assertion_type == "assert")
        failed = sum(1 for a in assertions if not a.passed and a.assertion_type == "assert")
        
        return passed, failed