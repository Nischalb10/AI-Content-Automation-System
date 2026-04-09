# AI Content Automation System - CrewAI

A sophisticated multi-agent AI system for automated content generation, summarization, writing, and editing using **CrewAI**. This system demonstrates advanced agent collaboration, conversation memory, and structured content workflows.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agents Overview](#agents-overview)
- [Memory Management](#memory-management)
- [Examples](#examples)
- [Demo](#demo)

---

## Features

### Core Features
- **Multi-Agent Collaboration**: 4 specialized agents working together seamlessly
- **News Collection**: Intelligent news gathering and curation
- **Content Summarization**: Concise summaries preserving key information
- **Content Writing**: Engaging, well-structured article generation
- **Quality Editing**: Professional content refinement and validation
- **Conversation Memory**: Maintains context across interactions
- **Follow-up Instructions**: Support for iterative content modifications
- **Structured Output**: JSON-based results for easy integration

### Advanced Capabilities
- **Context Awareness**: Agents leverage previous interactions
- **Tool Integration**: Specialized tools for analysis and validation
- **Error Handling**: Robust error management and logging
- **Session Management**: Track multiple conversations independently
- **Extensible Design**: Easy to add new agents or modify workflows

---

##  System Architecture

```
┌─────────────────────────────────────────────────────────┐
│          User Input (Topic/Instructions)                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Conversation Memory   │
        │  (Context Management)  │
        └──────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
    ┌─────────────┐   ┌────────────────┐
    │   Pipeline  │   │   Memory Store │
    │  Execution  │   │  (JSON File)   │
    └─────────────┘   └────────────────┘
        │
        ├─► Agent 1: News Collector
        │   └─► Task: Search & Collection
        │
        ├─► Agent 2: Summarizer
        │   └─► Task: Summarization
        │
        ├─► Agent 3: Content Writer
        │   └─► Task: Writing
        │
        ├─► Agent 4: Editor
        │   └─► Task: Refinement & Validation
        │
        └─► Final Output
```

---

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API Key (for LLM functionality)

### Setup Steps

1. **Clone or create the project directory**
   ```bash
   cd "Content Automation System"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   ```

---

## ⚙️ Configuration

### config.py

The system is configured through `config.py`:

```python
# API Configuration
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-4"

# Agents Configuration
AGENTS_CONFIG = {
    "news_collector": { ... },
    "summarizer": { ... },
    "content_writer": { ... },
    "editor": { ... }
}

# Tasks Configuration
TASKS_CONFIG = {
    "collect_news": { ... },
    "summarize_content": { ... },
    "write_content": { ... },
    "edit_content": { ... }
}

# Memory Configuration
MEMORY_CONFIG = {
    "memory_file": "conversation_history.json",
    "max_history": 50
}
```

**Key Configuration Options:**
- `OPENAI_MODEL`: LLM model to use (gpt-4, gpt-3.5-turbo, etc.)
- `max_history`: Number of interactions to keep in memory
- `verbose`: Enable detailed logging
- `max_rpm`: Rate limiting (requests per minute)
- `timeout`: Task execution timeout in seconds

---

##  Usage

### Basic Usage

#### 1. Simple Topic Processing
```python
from main import ContentAutomationSystem

system = ContentAutomationSystem()
output = system.process_topic("Artificial Intelligence in Healthcare")
system.display_content("final")
```

#### 2. Follow-up Instructions
```python
# After processing a topic
system.follow_up("Make this content more technical")
system.follow_up("Add more examples and case studies")
```

#### 3. Access Memory
```python
# Get memory summary
summary = system.get_memory_summary()

# Get all interactions
all_interactions = system.memory.get_all_memory()

# Get context from previous interactions
context = system.memory.get_context(num_interactions=5)
```

### Command-Line Usage

#### Run Default Example
```bash
python examples.py
```

#### Run Interactive Mode
```bash
python examples.py -i
```

#### Run All Examples
```bash
python examples.py --all
```

---

##  Project Structure

```
Content Automation System/
├── main.py                      # Main application orchestrator
├── config.py                    # System configuration
├── agents.py                    # Agent definitions and tasks
├── memory.py                    # Conversation memory management
├── examples.py                  # Usage examples and demos
├── requirements.txt             # Project dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── conversation_history.json   # Memory storage (generated)
└── README.md                   # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Core orchestration logic, pipeline execution |
| `config.py` | Configuration and constants |
| `agents.py` | Agent creation, tasks definition, tools |
| `memory.py` | Conversation memory system |
| `examples.py` | Usage examples and interactive mode |
| `requirements.txt` | Python dependencies |

---

## 🤖 Agents Overview

### Agent 1: News Collector
**Role**: News Collector  
**Goal**: Find and collect relevant news stories from various sources  
**Backstory**: Expert journalist with deep knowledge of current events

**Capabilities:**
- News searching and curation
- Source verification
- Article collection
- Information gathering

---

### Agent 2: Summarizer (Content Summarizer)
**Role**: Content Summarizer  
**Goal**: Create concise and accurate summaries preserving key information  
**Backstory**: Skilled content strategist with summarization expertise

**Capabilities:**
- Extract key information
- Create concise summaries
- Preserve context and relevance
- Maintain information hierarchy

---

### Agent 3: Writer (Content Writer)
**Role**: Content Writer  
**Goal**: Transform summaries into engaging, well-structured content  
**Backstory**: Creative writer with expertise in compelling narratives

**Capabilities:**
- Engaging writing
- Structure organization
- Style adaptation
- Narrative development

---

### Agent 4: Editor (Content Editor)
**Role**: Content Editor  
**Goal**: Review and ensure quality of all content  
**Backstory**: Experienced editor with commitment to excellence

**Capabilities:**
- Content analysis
- Quality validation
- Error correction
- Enhancement recommendations

---

##  Memory Management

### ConversationMemory Class

The `ConversationMemory` class manages conversation history:

```python
from memory import ConversationMemory

# Initialize memory
memory = ConversationMemory(
    memory_file="conversation_history.json",
    max_history=50
)

# Add interaction
memory.add_interaction(
    user_input="Create content about AI",
    agent_responses={"collect": "...", "write": "..."},
    topic="AI",
    metadata={"status": "success"}
)

# Get context
context = memory.get_context(num_interactions=5)

# Get summary
summary = memory.get_summary()
```

### Features

- **Persistent Storage**: Conversations saved to JSON
- **Session Tracking**: Separate sessions with unique IDs
- **Context Retrieval**: Smart context extraction for agent awareness
- **Bounded History**: Automatically maintains size limits
- **Metadata Support**: Store additional interaction data

### Memory File Structure

```json
[
  {
    "session_id": "a1b2c3d4",
    "timestamp": "2024-01-15T10:30:00",
    "user_input": "Create content about AI",
    "topic": "Artificial Intelligence",
    "agent_responses": {
      "news_collector": "...",
      "summarizer": "...",
      "writer": "...",
      "editor": "..."
    },
    "metadata": {
      "status": "success"
    }
  }
]
```

---

##  Examples

### Example 1: Basic Content Generation
```python
from main import ContentAutomationSystem

system = ContentAutomationSystem()
output = system.process_topic("Machine Learning in Finance", verbose=False)
system.display_content("final")
```

### Example 2: Multi-Topic Processing
```python
topics = ["Quantum Computing", "Renewable Energy", "Blockchain"]
for topic in topics:
    system.process_topic(topic)
```

### Example 3: Follow-up with Memory
```python
# First request
system.process_topic("AI Career Opportunities")

# Follow-up - system remembers context
system.follow_up("Make it suitable for low-cost online learning")
```

### Example 4: Interactive Mode
```bash
python examples.py -i
# Then follow the interactive menu
```

---

##  Demo

### Running the Demo

1. **Ensure dependencies are installed**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```

3. **Run the demo**
   ```bash
   python examples.py --all
   ```
   
---
