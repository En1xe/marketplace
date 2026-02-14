from typing import Any


def get_text_by_condition(
    main_text: str,
    optional_text: str,
    value_condition: Any
):
    """Adds optional text to the main text if the condition is true"""
    
    return f'{main_text} {optional_text if value_condition else ''}'.strip()
