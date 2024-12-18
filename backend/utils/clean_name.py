import re

def clean_disease_name(name):
    """
    Clean disease name while preserving valid characters including numbers and hyphens.
    
    Args:
        name (str): Raw disease name
        
    Returns:
        str: Cleaned disease name
    """
    # Remove parentheses
    name = name.replace('(', '').replace(')', '')
    
    # Remove ellipsis
    name = name.replace('...', '')
    name = name.replace('..', '')
    name = name.replace('.', '')
    
    # Preserve hyphens and numbers but remove other special characters
    cleaned = ''.join(char for char in name if char.isalnum() or char in '-')
    
    return cleaned.strip()