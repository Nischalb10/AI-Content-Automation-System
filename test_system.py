# Test Suite - Content Automation System
"""
Comprehensive test runner for the Content Automation System.
Tests configuration, imports, and basic functionality.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported successfully"""
    print("\n" + "="*80)
    print("TEST 1: Module Imports")
    print("="*80)
    
    try:
        import config
        print("✓ config module imported successfully")
    except Exception as e:
        print(f"✗ config import failed: {e}")
        return False
    
    try:
        import memory
        print("✓ memory module imported successfully")
    except Exception as e:
        print(f"✗ memory import failed: {e}")
        return False
    
    try:
        import agents
        print("✓ agents module imported successfully")
    except Exception as e:
        print(f"✗ agents import failed: {e}")
        return False
    
    try:
        import main
        print("✓ main module imported successfully")
    except Exception as e:
        print(f"✗ main import failed: {e}")
        return False
    
    return True


def test_configuration():
    """Test that configuration is loaded correctly"""
    print("\n" + "="*80)
    print("TEST 2: Configuration Loading")
    print("="*80)
    
    try:
        from config import (
            AGENTS_CONFIG, 
            TASKS_CONFIG, 
            MEMORY_CONFIG, 
            SYSTEM_CONFIG
        )
        
        # Check agents
        assert "news_collector" in AGENTS_CONFIG
        assert "summarizer" in AGENTS_CONFIG
        assert "content_writer" in AGENTS_CONFIG
        assert "editor" in AGENTS_CONFIG
        print("✓ All required agents configured")
        
        # Check tasks
        assert "collect_news" in TASKS_CONFIG
        assert "summarize_content" in TASKS_CONFIG
        assert "write_content" in TASKS_CONFIG
        assert "edit_content" in TASKS_CONFIG
        print("✓ All required tasks configured")
        
        # Check memory config
        assert "memory_file" in MEMORY_CONFIG
        assert "max_history" in MEMORY_CONFIG
        print("✓ Memory configuration complete")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_memory_system():
    """Test conversation memory system"""
    print("\n" + "="*80)
    print("TEST 3: Memory System")
    print("="*80)
    
    try:
        from memory import ConversationMemory
        import tempfile
        import json
        
        # Create temporary memory file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        memory = ConversationMemory(memory_file=temp_file, max_history=5)
        print("✓ Memory initialized successfully")
        
        # Test add interaction
        memory.add_interaction(
            user_input="Test input",
            agent_responses={"agent": "response"},
            topic="Test Topic",
            metadata={"test": True}
        )
        print("✓ Interaction added successfully")
        
        # Test get context
        context = memory.get_context(num_interactions=1)
        assert "Test Topic" in context
        print("✓ Context retrieval working")
        
        # Test memory summary
        summary = memory.get_summary()
        assert summary["total_interactions"] == 1
        print("✓ Memory summary correct")
        
        # Cleanup
        os.remove(temp_file)
        return True
        
    except Exception as e:
        print(f"✗ Memory system test failed: {e}")
        return False


def test_agent_creation():
    """Test that agents can be created"""
    print("\n" + "="*80)
    print("TEST 4: Agent Creation")
    print("="*80)
    
    try:
        from agents import (
            create_news_collector_agent,
            create_summarizer_agent,
            create_content_writer_agent,
            create_editor_agent,
        )
        
        # Test news collector
        agent = create_news_collector_agent()
        assert agent.role == "News Collector"
        print("✓ News Collector created successfully")
        
        # Test summarizer
        agent = create_summarizer_agent()
        assert agent.role == "Content Summarizer"
        print("✓ Summarizer created successfully")
        
        # Test writer
        agent = create_content_writer_agent()
        assert agent.role == "Content Writer"
        print("✓ Content Writer created successfully")
        
        # Test editor
        agent = create_editor_agent()
        assert agent.role == "Content Editor"
        print("✓ Content Editor created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent creation test failed: {e}")
        return False


def test_system_initialization():
    """Test that the main system can be initialized"""
    print("\n" + "="*80)
    print("TEST 5: System Initialization")
    print("="*80)
    
    try:
        from main import ContentAutomationSystem
        
        system = ContentAutomationSystem()
        print("✓ ContentAutomationSystem initialized successfully")
        
        # Check system has required attributes
        assert hasattr(system, 'memory')
        print("✓ System has memory component")
        
        assert hasattr(system, 'last_output')
        print("✓ System has output tracking")
        
        assert hasattr(system, 'process_topic')
        print("✓ System has process_topic method")
        
        assert hasattr(system, 'follow_up')
        print("✓ System has follow_up method")
        
        return True
        
    except Exception as e:
        print(f"✗ System initialization test failed: {e}")
        return False


def test_file_structure():
    """Test that all required files exist"""
    print("\n" + "="*80)
    print("TEST 6: File Structure")
    print("="*80)
    
    required_files = [
        'main.py',
        'agents.py',
        'memory.py',
        'config.py',
        'examples.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        '__init__.py',
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist


def test_dependencies():
    """Test that required dependencies are installed"""
    print("\n" + "="*80)
    print("TEST 7: Dependencies")
    print("="*80)
    
    dependencies = [
        'crewai',
        'python-dotenv',
        'requests',
        'pydantic',
        'langchain',
    ]
    
    all_installed = True
    for package in dependencies:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
    
    return all_installed


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*80)
    print("🧪 CONTENT AUTOMATION SYSTEM - TEST SUITE")
    print("="*80)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Memory System", test_memory_system),
        ("Agent Creation", test_agent_creation),
        ("System Initialization", test_system_initialization),
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n✗ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*80)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*80 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
