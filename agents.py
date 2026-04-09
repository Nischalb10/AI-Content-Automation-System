# Agent Definitions for Content Automation System
from crewai import Agent, Task, Crew, LLM
from crewai_tools import tool
from config import AGENTS_CONFIG, TASKS_CONFIG, OPENAI_API_KEY, OPENAI_MODEL
from memory import ConversationMemory
import requests
from bs4 import BeautifulSoup
from typing import Optional
import os

# Initialize Conversation Memory
conversation_memory = ConversationMemory()

# Configure LLM
llm = LLM(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    max_tokens=2048,
    temperature=0.7
) if OPENAI_API_KEY else None


# Tool Functions for Agents
@tool
def search_news(topic: str, max_results: int = 5) -> str:
    """
    Search for news articles on a specific topic
    
    Args:
        topic: The news topic to search for
        max_results: Maximum number of results to return
    
    Returns:
        String containing news article summaries
    """
    try:
        # Simulate news search - in production, use NewsAPI or similar
        news_items = []
        
        # Example mock data structure
        mock_articles = [
            {
                "title": f"Breaking: {topic} developments in 2024",
                "source": "TechNews Daily",
                "url": "https://example.com/news1",
                "summary": f"Latest updates on {topic}"
            },
            {
                "title": f"{topic}: Industry insights and trends",
                "source": "Industry Weekly",
                "url": "https://example.com/news2",
                "summary": f"Expert analysis of {topic}"
            },
            {
                "title": f"How {topic} is changing the landscape",
                "source": "Future Focus",
                "url": "https://example.com/news3",
                "summary": f"Impact analysis of {topic}"
            }
        ]
        
        for article in mock_articles[:max_results]:
            news_items.append(
                f"Title: {article['title']}\n"
                f"Source: {article['source']}\n"
                f"Summary: {article['summary']}\n"
            )
        
        return "\n---\n".join(news_items)
    except Exception as e:
        return f"Error searching news: {str(e)}"


@tool
def analyze_content(content: str) -> str:
    """
    Analyze content structure and quality
    
    Args:
        content: The content to analyze
    
    Returns:
        Analysis results
    """
    analysis = {
        "word_count": len(content.split()),
        "readability": "Good" if len(content.split()) > 100 else "Short",
        "structure": "Well-organized" if "\n" in content else "Linear",
    }
    return str(analysis)


@tool
def validate_content(content: str) -> str:
    """
    Validate content for quality and completeness
    
    Args:
        content: The content to validate
    
    Returns:
        Validation results
    """
    issues = []
    
    if len(content) < 100:
        issues.append("Content is too short")
    
    if not any(char in content for char in [".", "!", "?"]):
        issues.append("Missing proper punctuation")
    
    if len([line for line in content.split("\n") if line.strip()]) < 2:
        issues.append("Structure needs improvement")
    
    return "Issues found: " + ", ".join(issues) if issues else "Content passes validation"


# Agent Definitions
def create_news_collector_agent() -> Agent:
    """Create the News Collector agent"""
    return Agent(
        role=AGENTS_CONFIG["news_collector"]["role"],
        goal=AGENTS_CONFIG["news_collector"]["goal"],
        backstory=AGENTS_CONFIG["news_collector"]["backstory"],
        tools=[search_news],
        verbose=True,
        llm=llm,
    )


def create_summarizer_agent() -> Agent:
    """Create the Content Summarizer agent"""
    return Agent(
        role=AGENTS_CONFIG["summarizer"]["role"],
        goal=AGENTS_CONFIG["summarizer"]["goal"],
        backstory=AGENTS_CONFIG["summarizer"]["backstory"],
        verbose=True,
        llm=llm,
    )


def create_content_writer_agent() -> Agent:
    """Create the Content Writer agent"""
    return Agent(
        role=AGENTS_CONFIG["content_writer"]["role"],
        goal=AGENTS_CONFIG["content_writer"]["goal"],
        backstory=AGENTS_CONFIG["content_writer"]["backstory"],
        verbose=True,
        llm=llm,
    )


def create_editor_agent() -> Agent:
    """Create the Content Editor agent"""
    return Agent(
        role=AGENTS_CONFIG["editor"]["role"],
        goal=AGENTS_CONFIG["editor"]["goal"],
        backstory=AGENTS_CONFIG["editor"]["backstory"],
        tools=[analyze_content, validate_content],
        verbose=True,
        llm=llm,
    )


# Task Definitions
def create_task_collect_news(agent: Agent, topic: str) -> Task:
    """Create news collection task"""
    return Task(
        description=TASKS_CONFIG["collect_news"]["description"].format(topic=topic),
        expected_output=TASKS_CONFIG["collect_news"]["expected_output"],
        agent=agent,
        tools=[search_news],
    )


def create_task_summarize(agent: Agent, collected_news: str) -> Task:
    """Create summarization task"""
    return Task(
        description=f"{TASKS_CONFIG['summarize_content']['description']}\n\nContent to summarize:\n{collected_news}",
        expected_output=TASKS_CONFIG["summarize_content"]["expected_output"],
        agent=agent,
    )


def create_task_write_content(agent: Agent, summary: str) -> Task:
    """Create content writing task"""
    return Task(
        description=f"{TASKS_CONFIG['write_content']['description']}\n\nBased on this summary:\n{summary}",
        expected_output=TASKS_CONFIG["write_content"]["expected_output"],
        agent=agent,
    )


def create_task_edit_content(agent: Agent, written_content: str) -> Task:
    """Create content editing task"""
    return Task(
        description=f"{TASKS_CONFIG['edit_content']['description']}\n\nContent to edit:\n{written_content}",
        expected_output=TASKS_CONFIG["edit_content"]["expected_output"],
        agent=agent,
        tools=[analyze_content, validate_content],
    )
