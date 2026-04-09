# Memory Management System for Conversation History
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import hashlib


class ConversationMemory:
    """Manages conversation history and context for the content automation system"""

    def __init__(self, memory_file: str = "conversation_history.json", max_history: int = 50):
        """
        Initialize the conversation memory manager

        Args:
            memory_file: Path to the JSON file storing conversation history
            max_history: Maximum number of conversations to keep
        """
        self.memory_file = memory_file
        self.max_history = max_history
        self.memory: List[Dict[str, Any]] = []
        self.current_session_id = self._generate_session_id()
        self._load_memory()

    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]

    def _load_memory(self) -> None:
        """Load conversation history from file if it exists"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.memory = []
        else:
            self.memory = []

    def _save_memory(self) -> None:
        """Save conversation history to file"""
        os.makedirs(os.path.dirname(self.memory_file) or ".", exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def add_interaction(
        self, 
        user_input: str, 
        agent_responses: Dict[str, str],
        topic: str = "",
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Add a new interaction to memory

        Args:
            user_input: The user's input/request
            agent_responses: Dictionary of agent outputs
            topic: The topic being discussed
            metadata: Additional metadata
        """
        interaction = {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "topic": topic,
            "agent_responses": agent_responses,
            "metadata": metadata or {}
        }
        
        self.memory.append(interaction)
        
        # Keep only recent interactions
        if len(self.memory) > self.max_history:
            self.memory = self.memory[-self.max_history:]
        
        self._save_memory()

    def get_context(self, num_interactions: int = 5) -> str:
        """
        Get recent conversation context for agent awareness

        Args:
            num_interactions: Number of recent interactions to retrieve

        Returns:
            Formatted context string
        """
        recent = self.memory[-num_interactions:] if self.memory else []
        
        if not recent:
            return "No previous context available."
        
        context_lines = ["### Previous Conversation Context ###\n"]
        for interaction in recent:
            context_lines.append(f"Topic: {interaction.get('topic', 'General')}")
            context_lines.append(f"User: {interaction['user_input'][:100]}...")
            context_lines.append("---")
        
        return "\n".join(context_lines)

    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get all interactions from the current session"""
        return [m for m in self.memory if m["session_id"] == self.current_session_id]

    def get_all_memory(self) -> List[Dict[str, Any]]:
        """Get all stored interactions"""
        return self.memory.copy()

    def clear_session(self) -> None:
        """Clear current session memory"""
        self.memory = [m for m in self.memory if m["session_id"] != self.current_session_id]
        self._save_memory()

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the memory"""
        return {
            "total_interactions": len(self.memory),
            "current_session_interactions": len(self.get_session_history()),
            "sessions": len(set(m["session_id"] for m in self.memory)),
            "last_update": self.memory[-1]["timestamp"] if self.memory else None
        }
