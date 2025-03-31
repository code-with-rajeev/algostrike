# for sanitizing login credentials

def is_safe_string(input_str):
    if not input_str:
        return False
    return all(char.isalnum() or char == '_' for char in input_str)

def username_checker(input_str):
    pass