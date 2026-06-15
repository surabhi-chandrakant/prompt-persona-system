import json
from pathlib import Path
from typing import Dict, Any, List

class FileHandler:
    """Handles file operations for the prompt system"""
    
    @staticmethod
    def save_json(data: Any, filepath: str):
        """Save data to JSON file"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_json(filepath: str) -> Any:
        """Load data from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_text(text: str, filepath: str):
        """Save text to file"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(text)
    
    @staticmethod
    def load_text(filepath: str) -> str:
        """Load text from file"""
        with open(filepath, 'r') as f:
            return f.read()
    
    @staticmethod
    def batch_export(prompts: List[Dict], output_dir: str):
        """Export multiple prompts to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, prompt_data in enumerate(prompts):
            filename = f"prompt_{i+1}_{prompt_data['timestamp'][:19].replace(':', '-')}.txt"
            filepath = output_path / filename
            FileHandler.save_text(prompt_data['prompt'], str(filepath))
        
        # Save index file
        index_data = [
            {
                'file': f"prompt_{i+1}_{p['timestamp'][:19].replace(':', '-')}.txt",
                'persona': p['persona'],
                'template': p['template'],
                'timestamp': p['timestamp']
            }
            for i, p in enumerate(prompts)
        ]
        FileHandler.save_json(index_data, str(output_path / "index.json"))