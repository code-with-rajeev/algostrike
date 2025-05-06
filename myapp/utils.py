# for sanitizing login credentials

def is_safe_string(input_str):
    if not input_str:
        return False
    return all(char.isalnum() or char == '_' for char in input_str)

def is_valid_username(input_str):
    if is_safe_string(input_str) and len(input_str)>=7 and input_str[0].isalnum():
        return True
    return False