# Main Application - Content Automation System Orchestrator
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from crewai import Crew
from agents import (
    create_news_collector_agent,
    create_summarizer_agent,
    create_content_writer_agent,
    create_editor_agent,
    create_task_collect_news,
    create_task_summarize,
    create_task_write_content,
    create_task_edit_content,
    conversation_memory
)
from memory import ConversationMemory
import json
from datetime import datetime

# Load environment variables
load_dotenv()


class ContentAutomationSystem:
    """
    AI-powered Content Automation System using CrewAI
    Orchestrates multiple agents to collect, summarize, write, and edit content
    """

    def __init__(self):
        """Initialize the content automation system"""
        self.memory = conversation_memory
        self.last_output = {}
        self.process_output = []

    def _get_context_prompt(self) -> str:
        """Generate context from previous interactions"""
        return self.memory.get_context(num_interactions=3)

    def process_topic(self, topic: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Process a topic through the entire content automation pipeline

        Args:
            topic: The topic to process
            verbose: Whether to print detailed output

        Returns:
            Dictionary containing outputs from all agents
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"Starting Content Automation for Topic: {topic}")
            print(f"{'='*80}\n")

        results = {}
        context = self._get_context_prompt()

        try:
            # Step 1: Collect News
            if verbose:
                print("📰 STEP 1: Collecting News...")
                print("-" * 80)

            news_collector = create_news_collector_agent()
            
            # Augment task description with context
            augmented_description = (
                f"Topic: {topic}\n"
                f"Previous Context:\n{context}\n\n"
                f"Search and collect recent news articles on {topic} from the last 24 hours. "
                f"Build upon any previous context if relevant."
            )
            
            collect_task = create_task_collect_news(news_collector, topic)
            collect_task.description = augmented_description
            
            crew = Crew(agents=[news_collector], tasks=[collect_task], verbose=verbose)
            collected_news = crew.kickoff()
            results["collected_news"] = str(collected_news)
            
            if verbose:
                print(f"\n✅ News Collection Complete")
                print(f"Output Preview: {str(collected_news)[:200]}...\n")

            # Step 2: Summarize Content
            if verbose:
                print("📝 STEP 2: Summarizing Content...")
                print("-" * 80)

            summarizer = create_summarizer_agent()
            summarize_task = create_task_summarize(summarizer, results["collected_news"])
            
            crew = Crew(agents=[summarizer], tasks=[summarize_task], verbose=verbose)
            summary = crew.kickoff()
            results["summary"] = str(summary)
            
            if verbose:
                print(f"\n✅ Summarization Complete")
                print(f"Output Preview: {str(summary)[:200]}...\n")

            # Step 3: Write Content
            if verbose:
                print("✍️  STEP 3: Writing Content...")
                print("-" * 80)

            writer = create_content_writer_agent()
            write_task = create_task_write_content(writer, results["summary"])
            
            crew = Crew(agents=[writer], tasks=[write_task], verbose=verbose)
            written_content = crew.kickoff()
            results["written_content"] = str(written_content)
            
            if verbose:
                print(f"\n✅ Content Writing Complete")
                print(f"Output Preview: {str(written_content)[:200]}...\n")

            # Step 4: Edit Content
            if verbose:
                print("🔍 STEP 4: Editing Content...")
                print("-" * 80)

            editor = create_editor_agent()
            edit_task = create_task_edit_content(editor, results["written_content"])
            
            crew = Crew(agents=[editor], tasks=[edit_task], verbose=verbose)
            final_content = crew.kickoff()
            results["final_content"] = str(final_content)
            
            if verbose:
                print(f"\n✅ Content Editing Complete")
                print(f"Output Preview: {str(final_content)[:200]}...\n")

            # Store results in memory
            agent_responses = {
                "news_collector": results.get("collected_news", ""),
                "summarizer": results.get("summary", ""),
                "writer": results.get("written_content", ""),
                "editor": results.get("final_content", "")
            }
            
            self.memory.add_interaction(
                user_input=f"Process topic: {topic}",
                agent_responses=agent_responses,
                topic=topic,
                metadata={"status": "success"}
            )

            self.last_output = results

            if verbose:
                print(f"{'='*80}")
                print("✨ Content Automation Pipeline Complete!")
                print(f"{'='*80}\n")

            return results

        except Exception as e:
            print(f"❌ Error in processing: {str(e)}")
            self.memory.add_interaction(
                user_input=f"Process topic: {topic}",
                agent_responses={"error": str(e)},
                topic=topic,
                metadata={"status": "failed", "error": str(e)}
            )
            return {"error": str(e)}

    def follow_up(self, instruction: str) -> Dict[str, Any]:
        """
        Process follow-up instructions based on previous context

        Args:
            instruction: The follow-up instruction

        Returns:
            Dictionary with follow-up results
        """
        print(f"\n{'='*80}")
        print(f"Processing Follow-up: {instruction}")
        print(f"{'='*80}\n")

        if not self.last_output:
            print("⚠️  No previous output available. Please process a topic first.")
            return {"error": "No previous context"}

        try:
            # Get previous final content
            previous_content = self.last_output.get("final_content", "")
            
            # Create writer for modifications
            writer = create_content_writer_agent()
            
            modify_description = f"""
            Previous content:
            {previous_content}
            
            User's follow-up instruction:
            {instruction}
            
            Modify the content according to the user's instruction while maintaining quality and coherence.
            """
            
            from crewai import Task
            
            modify_task = Task(
                description=modify_description,
                expected_output="Modified content that incorporates the user's feedback and instructions",
                agent=writer,
            )
            
            crew = Crew(agents=[writer], tasks=[modify_task], verbose=True)
            modified_content = crew.kickoff()
            
            result = {"modified_content": str(modified_content)}
            
            # Store follow-up in memory
            self.memory.add_interaction(
                user_input=instruction,
                agent_responses={"modification": str(modified_content)},
                metadata={"type": "follow_up"}
            )
            
            return result

        except Exception as e:
            print(f"❌ Error in follow-up: {str(e)}")
            return {"error": str(e)}

    def display_content(self, step: Optional[str] = None) -> None:
        """
        Display the output content

        Args:
            step: Specific step to display (news, summary, written, final)
        """
        if not self.last_output:
            print("No content to display. Please process a topic first.")
            return

        if step == "news":
            print("\n📰 COLLECTED NEWS:")
            print(self.last_output.get("collected_news", "No content"))
        elif step == "summary":
            print("\n📝 SUMMARY:")
            print(self.last_output.get("summary", "No content"))
        elif step == "written":
            print("\n✍️  WRITTEN CONTENT:")
            print(self.last_output.get("written_content", "No content"))
        elif step == "final":
            print("\n✨ FINAL CONTENT:")
            print(self.last_output.get("final_content", "No content"))
        else:
            print("\n" + "="*80)
            print("COMPLETE PIPELINE OUTPUT")
            print("="*80)
            for key, value in self.last_output.items():
                print(f"\n{key.upper()}:")
                print("-" * 80)
                print(value)
                print()

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation memory"""
        return self.memory.get_summary()

    def clear_session(self) -> None:
        """Clear the current session from memory"""
        self.memory.clear_session()
        self.last_output = {}


def main():
    """Main entry point for the application"""
    # Initialize system
    system = ContentAutomationSystem()

    print("\n" + "="*80)
    print("🚀 AI CONTENT AUTOMATION SYSTEM - CrewAI")
    print("="*80)

    # Example: Process a topic
    topic = "Artificial Intelligence in Healthcare"
    
    print(f"\nProcessing topic: '{topic}'")
    
    output = system.process_topic(topic, verbose=False)  # Set to False for faster execution in testing
    
    # Display results
    system.display_content("final")

    # Show memory summary
    print("\n📊 Memory Summary:")
    print(json.dumps(system.get_memory_summary(), indent=2))

    print("\n" + "="*80)
    print("✅ Execution Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
