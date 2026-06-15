import json
from typing import Dict, Any, Optional
from pathlib import Path

class PersonaAdapter:
    """Adapts prompts based on user persona configurations"""
    
    def __init__(self, persona_id: str, custom_config: Optional[Dict] = None):
        self.persona_id = persona_id
        self.config = self._load_persona_config(persona_id)
        if custom_config:
            self.config.update(custom_config)
    
    def _load_persona_config(self, persona_id: str) -> Dict:
        """Load persona configuration from JSON file"""
        config_path = Path(__file__).parent.parent / "config" / "personas.json"
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        if persona_id not in data['personas']:
            raise ValueError(f"Unknown persona: {persona_id}")
        
        return data['personas'][persona_id]
    
    def get_icon(self) -> str:
        """Get persona icon"""
        return self.config.get('icon', '👤')
    
    def get_name(self) -> str:
        """Get persona display name"""
        return self.config['name']
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get specific configuration value"""
        return self.config.get(key, default)
    
    def get_include_examples_text(self) -> str:
        """Get text for include examples flag"""
        return "Include concrete" if self.config.get('include_examples', True) else "Exclude"
    
    def get_all_config(self) -> Dict:
        """Get complete persona configuration"""
        config_copy = self.config.copy()
        config_copy['include_examples_text'] = self.get_include_examples_text()
        return config_copy