from django import template

register = template.Library()

@register.filter
def split_and_strip(value, delimiter=","):
    """
    Splits the input string by a specified delimiter and strips whitespace from each resulting item.
    
    Args:
        value (str): The string to be split.
        delimiter (str, optional): The delimiter on which to split the string. Defaults to ",".
    
    Returns:
        list[str]: A list of strings obtained by splitting and stripping the input string.
    """
    return [item.strip() for item in value.split(delimiter)]

@register.filter
def to_int(value):
    """
    Converts a given input to an integer if possible; returns None if conversion is not possible.
    
    Args:
        value (str): The value to convert to an integer.
    
    Returns:
        int or None: The integer representation of the input if convertible, otherwise None.
    """
    try:
        return int(value) if value else None
    except (ValueError, TypeError):
        return None

@register.filter
def map_to_int(value):
    """
    Converts a list of string numbers to integers, ignoring non-digit strings.
    
    Args:
        value (list[str]): A list of strings to be converted to integers.
    
    Returns:
        list[int]: A list of integers converted from strings that contain digit characters only.
    """
    return [int(item) for item in value if item.isdigit()]