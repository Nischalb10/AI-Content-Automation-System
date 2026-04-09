# Example Usage Script - Content Automation System
"""
This script demonstrates various use cases of the Content Automation System.
Run this to see the system in action with different scenarios.
"""

import sys
from main import ContentAutomationSystem


def example_1_basic_content_generation():
    """Example 1: Basic content generation for a topic"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Content Generation")
    print("="*80)
    
    system = ContentAutomationSystem()
    
    topic = "Machine Learning in Finance"
    output = system.process_topic(topic, verbose=False)
    
    print("\n✅ Generated final content:")
    system.display_content("final")


def example_2_multi_topic_processing():
    """Example 2: Processing multiple topics sequentially"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Multi-Topic Processing")
    print("="*80)
    
    system = ContentAutomationSystem()
    
    topics = [
        "Quantum Computing",
        "Renewable Energy",
        "Blockchain Technology"
    ]
    
    for topic in topics:
        print(f"\nProcessing: {topic}")
        system.process_topic(topic, verbose=False)
        print(f"✅ Completed: {topic}")
    
    # Display memory summary
    memory_summary = system.get_memory_summary()
    print(f"\n📊 Total interactions processed: {memory_summary['total_interactions']}")


def example_3_follow_up_modification():
    """Example 3: Follow-up instructions and content modification"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Follow-up Modifications with Memory")
    print("="*80)
    
    system = ContentAutomationSystem()
    
    # Process initial topic
    topic = "Cybersecurity Threats"
    print(f"\n1. Initial processing: {topic}")
    system.process_topic(topic, verbose=False)
    system.display_content("final")
    
    # Follow-up: Make it more technical
    print("\n2. First follow-up: Make it more technical")
    follow_up = system.follow_up("Make this content more technical with specific terms and concepts")
    print(follow_up)
    
    # Memory now has context for next operations
    memory_summary = system.get_memory_summary()
    print(f"\n📊 Memory maintained {memory_summary['current_session_interactions']} interactions")


def example_4_conversation_memory():
    """Example 4: Demonstrate conversation memory and context awareness"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Conversation Memory and Context")
    print("="*80)
    
    system = ContentAutomationSystem()
    
    # First request
    print("\n1. User: 'Create content about AI careers'")
    system.process_topic("AI Career Opportunities", verbose=False)
    
    # Second request - system remembers
    print("\n2. User: 'Now make it suitable for low-cost online learning'")
    system.follow_up("Adapt the content to be suitable for low-cost online learning platforms")
    
    # Show memory
    print("\n📚 System Memory Snapshot:")
    all_memory = system.memory.get_all_memory()
    print(f"Total stored interactions: {len(all_memory)}")
    for i, interaction in enumerate(all_memory[-2:], 1):
        print(f"\nInteraction {i}:")
        print(f"  Topic: {interaction.get('topic', 'N/A')}")
        print(f"  Time: {interaction['timestamp']}")


def interactive_mode():
    """Interactive mode where user can input topics and follow-ups"""
    print("\n" + "="*80)
    print("🎯 INTERACTIVE MODE - Content Automation System")
    print("="*80)
    
    system = ContentAutomationSystem()
    
    while True:
        print("\n" + "-"*80)
        print("Options:")
        print("1. Process a new topic")
        print("2. Follow-up on previous content")
        print("3. Display content")
        print("4. View memory summary")
        print("5. Clear session")
        print("6. Exit")
        print("-"*80)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            topic = input("Enter the topic: ").strip()
            if topic:
                system.process_topic(topic, verbose=False)
                print("\n✅ Topic processed successfully!")
            else:
                print("❌ Please enter a valid topic")
        
        elif choice == "2":
            instruction = input("Enter your follow-up instruction: ").strip()
            if instruction:
                result = system.follow_up(instruction)
                if "error" not in result:
                    print("\n✅ Follow-up processed successfully!")
                    print(result.get("modified_content", "N/A"))
                else:
                    print(f"❌ Error: {result['error']}")
            else:
                print("❌ Please enter a valid instruction")
        
        elif choice == "3":
            step = input("Enter step (final/news/summary/written) or press Enter for all: ").strip().lower() or None
            system.display_content(step)
        
        elif choice == "4":
            summary = system.get_memory_summary()
            print("\n📊 Memory Summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")
        
        elif choice == "5":
            confirm = input("Clear current session? (y/n): ").lower()
            if confirm == 'y':
                system.clear_session()
                print("✅ Session cleared!")
        
        elif choice == "6":
            print("\nGoodbye! 👋")
            break
        
        else:
            print("❌ Invalid option. Please select 1-6")


def demo_all_examples():
    """Run all examples in sequence"""
    print("\n" + "="*80)
    print("RUNNING ALL EXAMPLES")
    print("="*80)
    
    print("\n[1/4] Running Example 1: Basic Content Generation...")
    try:
        example_1_basic_content_generation()
    except Exception as e:
        print(f"⚠️  Example 1 skipped: {str(e)}")
    
    print("\n[2/4] Running Example 2: Multi-Topic Processing...")
    try:
        example_2_multi_topic_processing()
    except Exception as e:
        print(f"⚠️  Example 2 skipped: {str(e)}")
    
    print("\n[3/4] Running Example 3: Follow-up Modifications...")
    try:
        example_3_follow_up_modification()
    except Exception as e:
        print(f"⚠️  Example 3 skipped: {str(e)}")
    
    print("\n[4/4] Running Example 4: Conversation Memory...")
    try:
        example_4_conversation_memory()
    except Exception as e:
        print(f"⚠️  Example 4 skipped: {str(e)}")
    
    print("\n" + "="*80)
    print("✅ ALL EXAMPLES COMPLETED")
    print("="*80)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        # Run interactive mode
        interactive_mode()
    elif len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Run all examples
        demo_all_examples()
    else:
        # Run default example
        print("\nRunning default example...")
        example_1_basic_content_generation()
        print("\nTip: Use '-i' flag for interactive mode, '--all' for all examples")
