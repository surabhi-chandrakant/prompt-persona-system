from typing import Dict, Any, List

class Validators:
    """Validation utilities for inputs"""
    
    @staticmethod
    def validate_persona(persona_id: str, available_personas: List[str]) -> bool:
        """Validate persona ID"""
        return persona_id in available_personas
    
    @staticmethod
    def validate_template(template_id: str, available_templates: List[str]) -> bool:
        """Validate template ID"""
        return template_id in available_templates
    
    @staticmethod
    def validate_variables(variables: Dict, required: List[str]) -> List[str]:
        """Validate required variables"""
        missing = []
        for req in required:
            if req not in variables or not str(variables[req]).strip():
                missing.append(req)
        return missing
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        # Remove potential dangerous characters
        dangerous_chars = ['<', '>', '&', '{', '}']
        for char in dangerous_chars:
            text = text.replace(char, '')
        return text.strip()