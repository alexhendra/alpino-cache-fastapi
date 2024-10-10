import hashlib

def transformer_function(input_string: str) -> str:
    """Simulate an external service by converting string to uppercase."""
    return input_string.upper()

def interleave_lists(list1, list2):
    """Interleave two lists of strings."""
    return [elem for pair in zip(list1, list2) for elem in pair]

def generate_hash(list1, list2):
    """Generate a hash of the two lists to be used as a cache key."""
    combined = ''.join(list1 + list2)
    return hashlib.sha256(combined.encode()).hexdigest()