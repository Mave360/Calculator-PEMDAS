import pytest
import project
from project import shunting_yard, is_valid_expression, tokenize

# Test cases for shunting_yard function
def test_shunting_yard():
    pass
    #Basic arithmetic operations
    assert shunting_yard(["3", "+", "2"]) == ["3", "2", "+"]
    assert shunting_yard(["5", "*", "4"]) == ["5", "4", "*"]

    # Test with negative numbers
    assert shunting_yard(["-3", "+", "2"]) == ['-3', '2', '+']
    assert shunting_yard(["5", "*", "-4"]) == ['5', '-4', '*']
    assert shunting_yard(["-5", "*", "-4"]) == ["-5", "-4", "*"]

# Test cases for tokenize function
def test_tokenize():
    # Basic arithmetic operations
    assert tokenize("3 + 2") == ["3", "+", "2"]
    assert tokenize("5 * 4") == ["5", "*", "4"]
    # Test with negative numbers
    assert tokenize("-3 + 2") == ["-", "3", "+", "2"]
    assert tokenize("5 * -4") == ["5", "*", "-", "4"]
    assert tokenize("-5 * -4") == ["-", "5", "*", "-", "4"]
    # Test with percentage
    assert tokenize("10%") == ["10", "%"]
    assert tokenize("-10%") == ["-", "10", "%"]
    assert tokenize("10.5%") == ["10.5", "%"]

# Test cases for is_valid_expression function
def test_is_valid_expression():
    # Basic valid expressions
    assert is_valid_expression("3 + 2") == "3+2"
    assert is_valid_expression("5 * 4") == "5*4"

    # Test with negative numbers and percentage
    assert is_valid_expression("-3 + 2") == "-3+2"
    assert is_valid_expression("5 * -4") == "5*-4"
    assert is_valid_expression("-5 * -4") == "-5*-4"
    assert is_valid_expression("10%") == "10%"
    assert is_valid_expression("-10%") == "-10%"
    assert is_valid_expression("10.5%") == "10.5%"
    # Invalid expressions
    assert is_valid_expression("abc") == None
    assert is_valid_expression("a^2+b^2") == None
    assert is_valid_expression("cat+dog") == None