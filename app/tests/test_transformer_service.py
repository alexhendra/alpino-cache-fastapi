import pytest
from services.transformer import transformer_function, interleave_lists, generate_hash

def test_transformer_function():
    assert transformer_function("test") == "TEST"
    assert transformer_function("Test Case") == "TEST CASE"

def test_interleave_lists():
    list1 = ["a", "b", "c"]
    list2 = ["1", "2", "3"]
    result = interleave_lists(list1, list2)
    assert result == ["a", "1", "b", "2", "c", "3"]

def test_generate_hash():
    list1 = ["a", "b", "c"]
    list2 = ["1", "2", "3"]
    hash_value = generate_hash(list1, list2)
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64  # SHA256 hash length
