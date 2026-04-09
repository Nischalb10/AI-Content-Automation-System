# Configuration for AI Content Automation System
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Agent Configuration
AGENTS_CONFIG = {
    "news_collector": {
        "role": "News Collector",
        "goal": "Find and collect relevant news stories and articles from various sources",
        "backstory": "An expert journalist with deep knowledge of current events and excellent research skills.",
        "max_iter": 5,
        "verbose": True,
    },
    "summarizer": {
        "role": "Content Summarizer",
        "goal": "Create concise and accurate summaries of news articles while preserving key information",
        "backstory": "A skilled content strategist with expertise in summarizing complex information.",
        "max_iter": 5,
        "verbose": True,
    },
    "content_writer": {
        "role": "Content Writer",
        "goal": "Transform news summaries into engaging, well-structured content pieces",
        "backstory": "A creative writer with expertise in crafting compelling narratives and engaging content.",
        "max_iter": 5,
        "verbose": True,
    },
    "editor": {
        "role": "Content Editor",
        "goal": "Review, refine, and ensure quality of all content before publishing",
        "backstory": "An experienced editor with keen eye for detail and commitment to content excellence.",
        "max_iter": 5,
        "verbose": True,
    },
}

# Tasks Configuration
TASKS_CONFIG = {
    "collect_news": {
        "description": "Search and collect recent news articles on {topic} from the last 24 hours",
        "expected_output": "A list of 5-10 relevant news articles with titles, sources, and brief descriptions",
    },
    "summarize_content": {
        "description": "Create a comprehensive summary of the provided news articles",
        "expected_output": "A concise summary (200-300 words) capturing the main points from the articles",
    },
    "write_content": {
        "description": "Transform the summary into an engaging content piece suitable for publishing",
        "expected_output": "A well-structured article (500-800 words) with introduction, body, and conclusion",
    },
    "edit_content": {
        "description": "Review and refine the content for quality, clarity, and engagement",
        "expected_output": "Final polished content with improvements for clarity, style, and impact",
    },
}

# Memory Configuration
MEMORY_CONFIG = {
    "memory_file": "conversation_history.json",
    "max_history": 50,
}

# System Configuration
SYSTEM_CONFIG = {
    "verbose": True,
    "max_rpm": 100,  # Max requests per minute
    "timeout": 300,  # Task timeout in seconds
}
