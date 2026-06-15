#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Templating System - CLI Interface
Windows-Compatible Version with Number Selection
"""

import sys
import io
import os

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Set environment variable for Python
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

# Try to import rich, fallback to simple print if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better UI: pip install rich")

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.prompt_manager import PromptManager

# Simple console for Windows if rich not available
if RICH_AVAILABLE:
    console = Console()
else:
    class SimpleConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = SimpleConsole()

class PromptCLI:
    def __init__(self):
        self.manager = PromptManager()
        self.current_session = None
        self.persona_list = []
        self.template_list = []
        self._load_lists()
    
    def _load_lists(self):
        """Load persona and template lists"""
        self.persona_list = self._get_persona_ids()
        self.template_list = self._get_template_ids()
    
    def _get_choice_from_list(self, prompt_text: str, items: List[str], allow_none: bool = False) -> Union[str, None]:
        """Get user choice with number selection"""
        if not items:
            print("⚠️ No items available!")
            return None
        
        # Display numbered list
        print(f"\n{prompt_text}")
        print("-" * 40)
        for idx, item in enumerate(items, 1):
            print(f"  {idx}. {item}")
        print("-" * 40)
        
        while True:
            choice = input(f"Enter number or ID (1-{len(items)}): ").strip()
            
            if not choice and allow_none:
                return None
            
            # Try as number
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(items):
                    return items[num - 1]
            
            # Try as direct ID
            if choice in items:
                return choice
            
            print(f"❌ Invalid choice. Please enter a number between 1 and {len(items)} or a valid ID.")
    
    def run(self):
        """Main CLI loop"""
        self.print_header()
        
        while True:
            self.show_menu()
            
            if RICH_AVAILABLE:
                choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5", "6", "7", "q"], default="1")
            else:
                print("\nSelect option (1-7 or q): ", end='')
                choice = input().strip()
            
            if choice == "1":
                self.generate_prompt()
            elif choice == "2":
                self.list_personas()
            elif choice == "3":
                self.list_templates()
            elif choice == "4":
                self.view_history()
            elif choice == "5":
                self.batch_generate()
            elif choice == "6":
                self.export_prompts()
            elif choice == "7":
                self.compare_personas()
            elif choice.lower() == "q":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("❌ Invalid option. Please try again.")
    
    def print_header(self):
        """Print application header"""
        header = """
╔══════════════════════════════════════════════════════════════╗
║                    🎭 Prompt Templating System                ║
║              Adaptive Prompts for Different Personas          ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(header)
    
    def show_menu(self):
        """Display main menu"""
        if RICH_AVAILABLE:
            table = Table(title="📋 Main Menu", style="cyan")
            table.add_column("Option", style="bold yellow")
            table.add_column("Action", style="white")
            
            table.add_row("1", "Generate a prompt")
            table.add_row("2", "List all personas")
            table.add_row("3", "List all templates")
            table.add_row("4", "View generation history")
            table.add_row("5", "Batch generate prompts")
            table.add_row("6", "Export prompts to files")
            table.add_row("7", "Compare personas")
            table.add_row("q", "Quit")
            
            console.print(table)
        else:
            menu = """
┌─────────────────────────────────────────────────────────────┐
│                        📋 MAIN MENU                         │
├─────────────────────────────────────────────────────────────┤
│  1. Generate a prompt                                       │
│  2. List all personas                                       │
│  3. List all templates                                      │
│  4. View generation history                                 │
│  5. Batch generate prompts                                  │
│  6. Export prompts to files                                 │
│  7. Compare personas                                        │
│  q. Quit                                                    │
└─────────────────────────────────────────────────────────────┘
            """
            print(menu)
    
    def list_personas(self):
        """Display all available personas"""
        config_path = Path(__file__).parent / "config" / "personas.json"
        
        if not config_path.exists():
            print("❌ Config file not found!")
            return
            
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if RICH_AVAILABLE:
            table = Table(title="🎭 Available Personas", style="green")
            table.add_column("#", style="bold cyan")
            table.add_column("ID", style="bold yellow")
            table.add_column("Name", style="white")
            table.add_column("Icon", style="yellow")
            table.add_column("Tone", style="blue")
            table.add_column("Tech Depth", style="magenta")
            
            for idx, (pid, pdata) in enumerate(data['personas'].items(), 1):
                table.add_row(
                    str(idx),
                    pid,
                    pdata['name'],
                    pdata.get('icon', '👤'),
                    pdata['tone'],
                    str(pdata['technical_depth'])
                )
            
            console.print(table)
        else:
            print("\n" + "="*60)
            print("🎭 AVAILABLE PERSONAS")
            print("="*60)
            
            for idx, (pid, pdata) in enumerate(data['personas'].items(), 1):
                print(f"\n{idx}. [{pid}] {pdata.get('icon', '👤')} {pdata['name']}")
                print(f"   Tone: {pdata['tone']}")
                print(f"   Tech Depth: {pdata['technical_depth']}")
                print(f"   Language: {pdata['language_level']}")
            
            print("\n" + "="*60)
    
    def list_templates(self):
        """Display all available templates"""
        templates = self.manager.template_engine.get_all_templates()
        
        if RICH_AVAILABLE:
            table = Table(title="📝 Available Templates", style="green")
            table.add_column("#", style="bold cyan")
            table.add_column("ID", style="bold yellow")
            table.add_column("Name", style="white")
            table.add_column("Required Variables", style="blue")
            
            for idx, (tid, tdata) in enumerate(templates.items(), 1):
                required = ", ".join(tdata.get('required', []))
                table.add_row(str(idx), tid, tdata['name'], required if required else "None")
            
            console.print(table)
        else:
            print("\n" + "="*60)
            print("📝 AVAILABLE TEMPLATES")
            print("="*60)
            
            for idx, (tid, tdata) in enumerate(templates.items(), 1):
                print(f"\n{idx}. [{tid}] {tdata['name']}")
                required = ", ".join(tdata.get('required', []))
                print(f"   Required: {required if required else 'None'}")
            
            print("\n" + "="*60)
    
    def generate_prompt(self):
        """Interactive prompt generation"""
        print("\n" + "="*60)
        print("🔧 GENERATE A PROMPT")
        print("="*60)
        
        # Select persona with number selection
        if not self.persona_list:
            print("❌ No personas found!")
            return
        
        persona_id = self._get_choice_from_list("Select a persona:", self.persona_list)
        if not persona_id:
            return
        
        # Select template with number selection
        if not self.template_list:
            print("❌ No templates found!")
            return
        
        template_id = self._get_choice_from_list("Select a template:", self.template_list)
        if not template_id:
            return
        
        # Get template info
        try:
            template = self.manager.template_engine.get_template(template_id)
        except ValueError:
            print(f"❌ Template '{template_id}' not found")
            return
            
        required_vars = template.get('required', [])
        
        # Collect variables
        print("\n📝 Enter variables:")
        variables = {}
        for var in required_vars:
            if RICH_AVAILABLE:
                value = Prompt.ask(f"  {var.replace('_', ' ').title()}")
            else:
                value = input(f"  {var.replace('_', ' ').title()}: ")
            variables[var] = value
        
        # Ask for enhancements
        if RICH_AVAILABLE:
            use_enhancements = Confirm.ask("\nAdd context enhancements?", default=False)
        else:
            use_enhancements = input("\nAdd context enhancements? (y/n): ").lower() == 'y'
        
        enhancements = None
        
        if use_enhancements:
            enhancements = {}
            
            if RICH_AVAILABLE:
                enhancements['timestamp'] = Confirm.ask("  Add timestamp?", default=True)
            else:
                enhancements['timestamp'] = input("  Add timestamp? (y/n): ").lower() == 'y'
            
            if RICH_AVAILABLE:
                urgency = Prompt.ask(
                    "  Urgency level",
                    choices=["low", "normal", "high", "critical"],
                    default="normal"
                )
            else:
                print("  Urgency level (low/normal/high/critical): ", end='')
                urgency = input().strip()
                if urgency not in ["low", "normal", "high", "critical"]:
                    urgency = "normal"
            
            if urgency:
                enhancements['urgency'] = urgency
            
            if RICH_AVAILABLE:
                quality_reqs = Prompt.ask("  Quality requirements (comma-separated)", default="")
            else:
                quality_reqs = input("  Quality requirements (comma-separated): ")
            
            if quality_reqs:
                enhancements['quality_requirements'] = [q.strip() for q in quality_reqs.split(',')]
        
        # Generate prompt
        print("\n⏳ Generating prompt...")
        try:
            result = self.manager.generate_prompt(
                persona_id=persona_id,
                template_id=template_id,
                variables=variables,
                enhancements=enhancements if enhancements else None
            )
            
            print("\n✅ PROMPT GENERATED!\n")
            
            if RICH_AVAILABLE:
                console.print(Panel(
                    result['prompt'],
                    title=f"{result['persona_icon']} {result['persona_name']} - {result['template_name']}",
                    border_style="cyan"
                ))
            else:
                print("="*60)
                print(result['prompt'])
                print("="*60)
            
            print(f"\n📊 Metadata:")
            print(f"   Persona: {result['persona_icon']} {result['persona_name']}")
            print(f"   Template: {result['template_name']}")
            print(f"   Time: {result['timestamp']}")
            
            # Save option
            if RICH_AVAILABLE:
                save = Confirm.ask("\nSave this prompt to a file?", default=False)
            else:
                save = input("\nSave this prompt to a file? (y/n): ").lower() == 'y'
            
            if save:
                if RICH_AVAILABLE:
                    filename = Prompt.ask("Filename", default=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                else:
                    filename = input(f"Filename (default: prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt): ")
                    if not filename:
                        filename = f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['prompt'])
                print(f"✓ Saved to {filename}")
                
        except Exception as e:
            print(f"❌ Error generating prompt: {str(e)}")
    
    def view_history(self):
        """View generation history"""
        sessions = self.manager.list_sessions()
        
        if not sessions:
            print("\n📭 No history found.")
            return
        
        print("\n📚 AVAILABLE SESSIONS:")
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")
        
        try:
            if RICH_AVAILABLE:
                session_input = Prompt.ask("Select session number", default="1")
            else:
                session_input = input("Select session number: ")
            
            session_idx = int(session_input) - 1
            if session_idx < 0 or session_idx >= len(sessions):
                print("❌ Invalid selection!")
                return
                
            session_id = sessions[session_idx]
            history = self.manager.get_history(session_id)
            
            if not history:
                print(f"📭 No prompts in session {session_id}")
                return
            
            print(f"\n📖 Session: {session_id}")
            print(f"Total prompts: {len(history)}\n")
            
            for i, entry in enumerate(history, 1):
                print(f"{i}. {entry.get('persona_icon', '👤')} {entry.get('persona_name', 'Unknown')} - {entry.get('template_name', 'Unknown')}")
                print(f"   Time: {entry.get('timestamp', 'Unknown')}")
                preview = entry.get('prompt', '')[:100]
                print(f"   Preview: {preview}...\n")
            
            if RICH_AVAILABLE:
                view = Confirm.ask("View full prompt?", default=False)
            else:
                view = input("View full prompt? (y/n): ").lower() == 'y'
            
            if view:
                if RICH_AVAILABLE:
                    idx_input = Prompt.ask("Enter prompt number")
                else:
                    idx_input = input("Enter prompt number: ")
                
                idx = int(idx_input) - 1
                if 0 <= idx < len(history):
                    print("\n" + "="*60)
                    print(history[idx]['prompt'])
                    print("="*60)
                else:
                    print("❌ Invalid prompt number!")
                    
        except (IndexError, ValueError):
            print("❌ Invalid selection!")
    
    def batch_generate(self):
        """Generate multiple prompts at once"""
        print("\n" + "="*60)
        print("📦 BATCH GENERATION")
        print("="*60)
        
        if RICH_AVAILABLE:
            config_file = Prompt.ask("Path to batch config JSON file", default="batch_config.json")
        else:
            config_file = input("Path to batch config JSON file (default: batch_config.json): ").strip()
            if not config_file:
                config_file = "batch_config.json"
        
        config_path = Path(config_file)
        
        if not config_path.exists():
            print(f"⚠️ Config file not found! Creating template...")
            
            # Create template config
            template_config = {
                "prompts": [
                    {
                        "persona": "beginner",
                        "template": "explanation",
                        "variables": {
                            "concept": "Python programming",
                            "context": "First-time learner",
                            "additional_instructions": "Start with basics"
                        },
                        "enhancements": {
                            "timestamp": True,
                            "urgency": "normal"
                        }
                    },
                    {
                        "persona": "expert",
                        "template": "explanation",
                        "variables": {
                            "concept": "Python programming",
                            "context": "Advanced developer",
                            "additional_instructions": "Focus on optimization"
                        },
                        "enhancements": {
                            "timestamp": True,
                            "urgency": "normal"
                        }
                    }
                ]
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(template_config, f, indent=2)
            
            print(f"✓ Created template at {config_file}")
            print("  Please edit this file and run again.")
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Error reading config file: {e}")
            return
        
        prompts = []
        total = len(config.get('prompts', []))
        
        for i, prompt_config in enumerate(config.get('prompts', []), 1):
            print(f"⏳ Generating prompt {i}/{total}...")
            try:
                result = self.manager.generate_prompt(
                    persona_id=prompt_config.get('persona'),
                    template_id=prompt_config.get('template'),
                    variables=prompt_config.get('variables', {}),
                    enhancements=prompt_config.get('enhancements'),
                    save_to_history=True
                )
                prompts.append(result)
                print(f"   ✓ Generated")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n✅ Generated {len(prompts)}/{total} prompts successfully!")
        
        if prompts:
            if RICH_AVAILABLE:
                save = Confirm.ask("Save batch results to file?", default=True)
            else:
                save = input("Save batch results to file? (y/n): ").lower() == 'y'
            
            if save:
                if RICH_AVAILABLE:
                    output_file = Prompt.ask("Output filename", default=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                else:
                    output_file = input(f"Output filename (default: batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json): ")
                    if not output_file:
                        output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(prompts, f, indent=2, default=str)
                print(f"✓ Saved to {output_file}")
    
    def export_prompts(self):
        """Export prompts to files"""
        if RICH_AVAILABLE:
            session_id = Prompt.ask("Session ID to export", default=self.manager.current_session)
        else:
            session_id = input(f"Session ID to export (default: {self.manager.current_session}): ").strip()
            if not session_id:
                session_id = self.manager.current_session
        
        history = self.manager.get_history(session_id)
        
        if not history:
            print(f"📭 No prompts found in session {session_id}")
            return
        
        if RICH_AVAILABLE:
            output_dir = Prompt.ask("Output directory", default="exports")
        else:
            output_dir = input("Output directory (default: exports): ").strip()
            if not output_dir:
                output_dir = "exports"
        
        try:
            from utils.file_handler import FileHandler
            FileHandler.batch_export(history, output_dir)
            print(f"✓ Exported {len(history)} prompts to {output_dir}/")
        except ImportError:
            # Manual export if file_handler not available
            Path(output_dir).mkdir(exist_ok=True)
            for i, prompt_data in enumerate(history, 1):
                filename = f"{output_dir}/prompt_{i}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(prompt_data['prompt'])
            print(f"✓ Exported {len(history)} prompts to {output_dir}/")
    
    def compare_personas(self):
        """Compare how different personas handle the same prompt"""
        print("\n" + "="*60)
        print("🔄 COMPARE PERSONAS")
        print("="*60)
        
        # Select template with number selection
        if not self.template_list:
            print("❌ No templates found!")
            return
        
        template_id = self._get_choice_from_list("Select a template to compare:", self.template_list)
        if not template_id:
            return
        
        try:
            template = self.manager.template_engine.get_template(template_id)
        except ValueError:
            print(f"❌ Template '{template_id}' not found")
            return
        
        # Collect variables once
        variables = {}
        print("\n📝 Enter variables (will be used for all personas):")
        for var in template.get('required', []):
            if RICH_AVAILABLE:
                value = Prompt.ask(f"  {var.replace('_', ' ').title()}")
            else:
                value = input(f"  {var.replace('_', ' ').title()}: ")
            variables[var] = value
        
        # Select personas to compare (allow multiple)
        print("\n👥 Select personas to compare (you can select multiple)")
        print("Enter numbers separated by commas (e.g., 1,2,3) or 'all' for all personas")
        
        # Show persona list with numbers
        for idx, pid in enumerate(self.persona_list, 1):
            print(f"  {idx}. {pid}")
        
        selection = input("\nYour selection: ").strip().lower()
        
        if selection == 'all':
            selected_personas = self.persona_list
        else:
            selected_indices = []
            for part in selection.split(','):
                part = part.strip()
                if part.isdigit():
                    selected_indices.append(int(part))
            selected_personas = [self.persona_list[i-1] for i in selected_indices if 1 <= i <= len(self.persona_list)]
        
        if not selected_personas:
            print("❌ No valid personas selected!")
            return
        
        # Generate prompts
        results = {}
        print("\n⏳ Generating prompts for comparison...")
        
        for persona_id in selected_personas:
            print(f"  Generating for {persona_id}...")
            try:
                result = self.manager.generate_prompt(
                    persona_id=persona_id,
                    template_id=template_id,
                    variables=variables,
                    save_to_history=False
                )
                results[persona_id] = result
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        # Display comparison
        print("\n" + "="*60)
        print("📊 PERSONA COMPARISON")
        print("="*60)
        
        for persona_id, result in results.items():
            print(f"\n{'='*60}")
            print(f"{result['persona_icon']} {result['persona_name']}")
            print(f"{'='*60}")
            
            # Show first 500 characters
            prompt_text = result['prompt']
            if len(prompt_text) > 500:
                print(prompt_text[:500])
                print("\n... (truncated, full prompt saved if you choose to save)")
            else:
                print(prompt_text)
        
        # Option to save comparison
        if RICH_AVAILABLE:
            save = Confirm.ask("\nSave comparison to file?", default=True)
        else:
            save = input("\nSave comparison to file? (y/n): ").lower() == 'y'
        
        if save:
            if RICH_AVAILABLE:
                filename = Prompt.ask("Filename", default=f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            else:
                filename = input(f"Filename (default: comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json): ")
                if not filename:
                    filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Convert to serializable format
                serializable_results = {}
                for pid, res in results.items():
                    serializable_results[pid] = {
                        'persona': res['persona'],
                        'persona_name': res['persona_name'],
                        'template': res['template'],
                        'prompt': res['prompt'],
                        'timestamp': res['timestamp']
                    }
                json.dump(serializable_results, f, indent=2, default=str)
            print(f"✓ Saved to {filename}")
    
    def _get_persona_ids(self) -> List[str]:
        """Get list of persona IDs"""
        config_path = Path(__file__).parent / "config" / "personas.json"
        if not config_path.exists():
            return []
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return list(data.get('personas', {}).keys())
        except:
            return []
    
    def _get_template_ids(self) -> List[str]:
        """Get list of template IDs"""
        try:
            return list(self.manager.template_engine.get_all_templates().keys())
        except:
            return []

def main():
    """Main entry point"""
    try:
        cli = PromptCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all files are in the correct directory structure")
        print("2. Run: pip install -r requirements.txt")
        print("3. Make sure config/personas.json and templates/prompt_templates.json exist")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()