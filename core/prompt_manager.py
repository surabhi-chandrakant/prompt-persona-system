import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from .persona_adapter import PersonaAdapter
from .template_engine import TemplateEngine
from .context_enhancer import ContextEnhancer

class PromptManager:
    """Main manager for prompt generation and history tracking"""
    
    def __init__(self, history_dir: str = "history"):
        self.template_engine = TemplateEngine()
        self.context_enhancer = ContextEnhancer()
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_prompt(self, 
                       persona_id: str,
                       template_id: str,
                       variables: Dict[str, Any],
                       enhancements: Optional[Dict] = None,
                       save_to_history: bool = True) -> Dict:
        """Generate a prompt with persona adaptation"""
        
        # Create persona adapter
        adapter = PersonaAdapter(persona_id)
        persona_config = adapter.get_all_config()
        
        # Validate template variables
        missing_vars = self.template_engine.validate_template_variables(template_id, variables)
        if missing_vars:
            raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")
        
        # Render base prompt
        base_prompt = self.template_engine.render(template_id, variables, persona_config)
        
        # Apply enhancements
        if enhancements:
            final_prompt = self.context_enhancer.apply_enhancements(base_prompt, enhancements)
        else:
            final_prompt = base_prompt
        
        # Create result object
        result = {
            'prompt': final_prompt,
            'persona': persona_id,
            'persona_name': adapter.get_name(),
            'persona_icon': adapter.get_icon(),
            'template': template_id,
            'template_name': self.template_engine.get_template(template_id)['name'],
            'variables': variables,
            'enhancements': enhancements or {},
            'timestamp': datetime.now().isoformat(),
            'session_id': self.current_session
        }
        
        # Save to history
        if save_to_history:
            self._save_to_history(result)
        
        return result
    
    def _save_to_history(self, result: Dict):
        """Save generated prompt to history"""
        history_file = self.history_dir / f"history_{self.current_session}.json"
        
        # Load existing history
        history = []
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        # Add new entry
        history.append(result)
        
        # Save back
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_history(self, session_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve generation history"""
        if session_id:
            history_file = self.history_dir / f"history_{session_id}.json"
        else:
            history_file = self.history_dir / f"history_{self.current_session}.json"
        
        if not history_file.exists():
            return []
        
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        if limit:
            return history[-limit:]
        return history
    
    def list_sessions(self) -> List[str]:
        """List all available history sessions"""
        sessions = []
        for file in self.history_dir.glob("history_*.json"):
            session_id = file.stem.replace("history_", "")
            sessions.append(session_id)
        return sorted(sessions)
    
    def export_prompt(self, result: Dict, filepath: str):
        """Export a single prompt to file"""
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(result['prompt'])
        
        # Also save metadata
        meta_path = output_path.with_suffix('.meta.json')
        with open(meta_path, 'w') as f:
            json.dump({k: v for k, v in result.items() if k != 'prompt'}, f, indent=2)