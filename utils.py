import re
from typing import Optional

def extract_entity_name(user_input: str) -> Optional[str]:
    """
    Extract the entity name (company, product, or service) from the user's input.
    
    This function attempts to identify the entity name from various question formats:
    - "What are the terms and conditions for [entity]?"
    - "Show me the T&C for [entity]"
    - "I need the terms for [entity]"
    - "Find the terms and conditions of [entity]"
    - "Get me the TOS for [entity]"
    
    Args:
        user_input: The user's input text
        
    Returns:
        The extracted entity name or None if no entity could be identified
    """
    # Common patterns for terms and conditions requests
    patterns = [
        r"(?:terms and conditions|terms & conditions|t&c|tos|terms of service|terms of use|terms) (?:for|of) ([^?.,]+)",
        r"(?:what are|show me|i need|find|get me) (?:the )?(?:terms and conditions|t&c|tos|terms) (?:for|of) ([^?.,]+)",
        r"(?:what are|show me|i need|find|get me) (?:the )?(?:terms and conditions|t&c|tos|terms) (?:for|of) ([^?.,]+)\?",
    ]
    
    # Try each pattern
    for pattern in patterns:
        match = re.search(pattern, user_input.lower())
        if match:
            entity_name = match.group(1).strip()
            return entity_name
    
    # If no pattern matches, try to extract the entity name after common phrases
    fallback_patterns = [
        r"(?:for|about|regarding) ([^?.,]+)",
        r"(?:what are|show me|i need|find|get me) (?:the )?([^?.,]+) (?:terms and conditions|t&c|tos|terms)",
    ]
    
    for pattern in fallback_patterns:
        match = re.search(pattern, user_input.lower())
        if match:
            entity_name = match.group(1).strip()
            return entity_name
    
    # If still no match, return None
    return None

def format_config_with_entity(config: dict, entity_name: str) -> dict:
    """
    Replace the {entity_name} placeholder in the configuration with the actual entity name.
    
    Args:
        config: The configuration dictionary
        entity_name: The entity name to insert
        
    Returns:
        A new configuration dictionary with the entity name inserted
    """
    import copy
    import json
    
    # Create a deep copy of the config
    new_config = copy.deepcopy(config)
    
    # Convert to JSON string, replace the placeholder, and convert back to dict
    config_str = json.dumps(new_config)
    config_str = config_str.replace("{entity_name}", entity_name)
    new_config = json.loads(config_str)
    
    return new_config 