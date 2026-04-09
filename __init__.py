"""
AI Content Automation System - CrewAI Implementation

A sophisticated multi-agent AI system for automated content generation,
summarization, writing, and editing using CrewAI.

Main Components:
- main.py: Core orchestration logic
- agents.py: Agent definitions and task creation  
- memory.py: Conversation memory management
- config.py: System configuration
- examples.py: Usage examples and interactive mode

License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Content Automation Team"
__description__ = "AI Multi-Agent Content Automation System using CrewAI"

from main import ContentAutomationSystem
from memory import ConversationMemory
from config import AGENTS_CONFIG, TASKS_CONFIG, MEMORY_CONFIG, SYSTEM_CONFIG

__all__ = [
    "ContentAutomationSystem",
    "ConversationMemory",
    "AGENTS_CONFIG",
    "TASKS_CONFIG",
    "MEMORY_CONFIG",
    "SYSTEM_CONFIG",
]
