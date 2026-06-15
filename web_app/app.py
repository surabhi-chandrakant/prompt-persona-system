from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/personas', methods=['GET'])
def get_personas():
    """Get all available personas"""
    config_path = Path(__file__).parent.parent / "config" / "personas.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    personas = []
    for pid, pdata in data['personas'].items():
        personas.append({
            'id': pid,
            'name': pdata['name'],
            'icon': pdata.get('icon', '👤'),
            'description': f"Expertise: {pdata['technical_depth']}, Tone: {pdata['tone']}"
        })
    
    return jsonify(personas)

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get all available templates with their required variables"""
    templates_path = Path(__file__).parent.parent / "templates" / "prompt_templates.json"
    with open(templates_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    template_list = []
    for tid, tdata in data['templates'].items():
        template_list.append({
            'id': tid,
            'name': tdata['name'],
            'required_variables': tdata.get('required', []),
            'all_variables': tdata.get('variables', []),
            'description': f"Use for: {', '.join(tdata.get('variables', [])[:3])}"
        })
    
    return jsonify(template_list)

@app.route('/api/generate', methods=['POST'])
def generate_prompt():
    """Generate a prompt"""
    data = request.json
    
    try:
        # Get persona configuration
        config_path = Path(__file__).parent.parent / "config" / "personas.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            persona_data = json.load(f)
        
        persona_id = data['persona']
        if persona_id not in persona_data['personas']:
            return jsonify({'success': False, 'error': 'Invalid persona'}), 400
        
        persona_config = persona_data['personas'][persona_id].copy()
        
        # Get template
        templates_path = Path(__file__).parent.parent / "templates" / "prompt_templates.json"
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates_data = json.load(f)
        
        template_id = data['template']
        if template_id not in templates_data['templates']:
            return jsonify({'success': False, 'error': 'Invalid template'}), 400
        
        template = templates_data['templates'][template_id]
        template_string = template['template']
        
        # Get user variables
        user_variables = data.get('variables', {}).copy()
        
        # Check for missing required variables
        required_vars = template.get('required', [])
        missing_vars = [var for var in required_vars if var not in user_variables or not user_variables[var]]
        
        if missing_vars:
            return jsonify({
                'success': False, 
                'error': f'Missing required variables: {", ".join(missing_vars)}'
            }), 400
        
        # Prepare all variables (persona config + user variables)
        all_variables = {
            # Persona config values
            'persona_name': persona_config['name'],
            'language_level': persona_config['language_level'],
            'technical_depth': persona_config['technical_depth'],
            'tone': persona_config['tone'],
            'detail_level': persona_config['detail_level'],
            'jargon_level': persona_config['jargon_level'],
            'structure': persona_config['structure'],
            'include_examples_text': "Include concrete" if persona_config.get('include_examples', True) else "Exclude",
            
            # User variables
            **user_variables
        }
        
        # Also add persona_name_lower for templates that need it
        all_variables['persona_name_lower'] = persona_config['name'].lower()
        
        # Replace all placeholders in template
        prompt = template_string
        for key, value in all_variables.items():
            placeholder = "{" + key + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        # Handle any remaining placeholders
        import re
        remaining_placeholders = re.findall(r'\{([^}]+)\}', prompt)
        for placeholder in remaining_placeholders:
            if placeholder in all_variables:
                prompt = prompt.replace(f"{{{placeholder}}}", str(all_variables[placeholder]))
            else:
                prompt = prompt.replace(f"{{{placeholder}}}", f"[{placeholder} not provided]")
        
        # Apply enhancements
        enhancements = data.get('enhancements', {})
        
        # Quality requirements (add at the beginning)
        if enhancements.get('quality_requirements'):
            reqs = enhancements['quality_requirements']
            if reqs and any(reqs):
                req_text = "📋 Quality Requirements:\n" + "\n".join(f"  • {req}" for req in reqs if req)
                prompt = f"{req_text}\n\n{prompt}"
        
        # Timestamp
        if enhancements.get('timestamp'):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prompt = f"[Generated at: {timestamp}]\n\n{prompt}"
        
        # Urgency (add at the very beginning)
        if enhancements.get('urgency'):
            urgency_levels = {
                "low": "⏰ This task has flexible timing. Take time to be thorough.",
                "normal": "📅 Please complete this in a timely manner.",
                "high": "⚠️ URGENT: This requires immediate attention.",
                "critical": "🚨 CRITICAL: Immediate action required!"
            }
            urgency_text = urgency_levels.get(enhancements['urgency'], "")
            if urgency_text:
                prompt = f"{urgency_text}\n\n{prompt}"
        
        # Save to history
        result = {
            'prompt': prompt,
            'persona': persona_id,
            'persona_name': persona_config['name'],
            'persona_icon': persona_config.get('icon', '👤'),
            'template': template_id,
            'template_name': template['name'],
            'variables': user_variables,
            'enhancements': enhancements,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history file
        history_dir = Path(__file__).parent.parent / "history"
        history_dir.mkdir(exist_ok=True)
        history_file = history_dir / "web_history.json"
        
        history = []
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        history.append(result)
        
        # Keep last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, default=str)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'metadata': {
                'persona': result['persona_name'],
                'persona_icon': result['persona_icon'],
                'template': result['template_name'],
                'timestamp': result['timestamp']
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get prompt history"""
    history_dir = Path(__file__).parent.parent / "history"
    history_file = history_dir / "web_history.json"
    
    if not history_file.exists():
        return jsonify({'success': True, 'history': [], 'count': 0})
    
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    limit = request.args.get('limit', type=int)
    if limit:
        history = history[-limit:]
    
    return jsonify({
        'success': True,
        'history': history,
        'count': len(history)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)