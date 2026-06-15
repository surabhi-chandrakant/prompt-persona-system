from datetime import datetime
from typing import List, Optional, Dict

class ContextEnhancer:
    """Adds contextual enhancements to prompts"""
    
    @staticmethod
    def add_timestamp(prompt: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Add timestamp to prompt"""
        timestamp = datetime.now().strftime(format_string)
        return f"[Generated at: {timestamp}]\n\n{prompt}"
    
    @staticmethod
    def add_urgency(prompt: str, level: str = "normal") -> str:
        """Add urgency level to prompt"""
        urgency_levels = {
            "low": "⏰ This task has flexible timing. Take time to be thorough.",
            "normal": "📅 Please complete this in a timely manner.",
            "high": "⚠️ URGENT: This requires immediate attention.",
            "critical": "🚨 CRITICAL: Immediate action required!"
        }
        return f"{urgency_levels.get(level, urgency_levels['normal'])}\n\n{prompt}"
    
    @staticmethod
    def add_quality_requirements(prompt: str, requirements: List[str]) -> str:
        """Add quality requirements to prompt"""
        if not requirements:
            return prompt
        
        req_text = "📋 Quality Requirements:\n" + "\n".join(f"  • {req}" for req in requirements)
        return f"{req_text}\n\n{prompt}"
    
    @staticmethod
    def add_audience_context(prompt: str, audience: str, expertise_level: str = "mixed") -> str:
        """Add audience context"""
        audience_text = f"🎯 Target Audience: {audience} (Expertise: {expertise_level})"
        return f"{audience_text}\n\n{prompt}"
    
    @staticmethod
    def add_constraints(prompt: str, constraints: Dict[str, str]) -> str:
        """Add constraints to prompt"""
        if not constraints:
            return prompt
        
        constraints_text = "🔒 Constraints:\n" + "\n".join(f"  • {k}: {v}" for k, v in constraints.items())
        return f"{constraints_text}\n\n{prompt}"
    
    def apply_enhancements(self, prompt: str, enhancements: Dict) -> str:
        """Apply multiple enhancements"""
        enhanced_prompt = prompt
        
        if enhancements.get('timestamp'):
            enhanced_prompt = self.add_timestamp(enhanced_prompt)
        
        if enhancements.get('urgency'):
            enhanced_prompt = self.add_urgency(enhanced_prompt, enhancements['urgency'])
        
        if enhancements.get('quality_requirements'):
            enhanced_prompt = self.add_quality_requirements(
                enhanced_prompt, 
                enhancements['quality_requirements']
            )
        
        if enhancements.get('audience'):
            enhanced_prompt = self.add_audience_context(
                enhanced_prompt,
                enhancements['audience'],
                enhancements.get('expertise_level', 'mixed')
            )
        
        if enhancements.get('constraints'):
            enhanced_prompt = self.add_constraints(enhanced_prompt, enhancements['constraints'])
        
        return enhanced_prompt