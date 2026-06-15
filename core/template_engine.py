import json
from typing import Dict, Any, List
from pathlib import Path

class TemplateEngine:
    """Handles prompt template loading and rendering"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load templates from JSON file"""
        template_path = Path(__file__).parent.parent / "templates" / "prompt_templates.json"
        with open(template_path, 'r') as f:
            data = json.load(f)
        return data['templates']
    
    def get_template(self, template_id: str) -> Dict:
        """Get template by ID"""
        if template_id not in self.templates:
            raise ValueError(f"Unknown template: {template_id}")
        return self.templates[template_id]
    
    def get_all_templates(self) -> Dict:
        """Get all available templates"""
        return self.templates
    
    def render(self, template_id: str, variables: Dict[str, Any], persona_config: Dict) -> str:
        """Render a template with variables and persona configuration"""
        template = self.get_template(template_id)
        template_str = template['template']
        
        # Merge persona config with variables
        all_vars = {**persona_config, **variables}
        
        # Replace placeholders
        for key, value in all_vars.items():
            placeholder = "{" + key + "}"
            if placeholder in template_str:
                template_str = template_str.replace(placeholder, str(value))
        
        return template_str.strip()
    
    def validate_template_variables(self, template_id: str, variables: Dict) -> List[str]:
        """Validate that all required variables are provided"""
        template = self.get_template(template_id)
        required = template.get('required', [])
        missing = [req for req in required if req not in variables or not variables[req]]
        return missing