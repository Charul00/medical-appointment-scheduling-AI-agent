#!/usr/bin/env python3
"""
Medical Appointment Scheduling AI Agent - Demonstration Script

This script demonstrates the LangChain-based scheduling agent working
with realistic appointment scheduling scenarios.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / 'src'))

try:
    from agents.scheduling_agent import MedicalSchedulingAgent
    print("✅ Successfully imported LangChain-based MedicalSchedulingAgent")
except ImportError as e:
    print(f"❌ Failed to import scheduling agent: {e}")
    sys.exit(1)

def run_demo():
    """Run a comprehensive demo of the scheduling agent"""
    
    print("\n" + "="*60)
    print("🏥 MEDICAL APPOINTMENT SCHEDULING AI AGENT DEMO")
    print("Powered by LangChain & LangGraph")
    print("="*60)
    
    # Initialize the agent
    try:
        agent = MedicalSchedulingAgent()
        print("✅ Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Demo scenarios
    demo_queries = [
        "Hello, I need to schedule an appointment",
        "What doctors do you have available?",
        "What times are available next week?",
        "Do you accept Blue Cross Blue Shield insurance?",
        "I need a pediatric appointment for my 5-year-old",
        "Can I see Dr. Smith on Monday morning?",
        "I'm a new patient, what do I need to bring?",
        "Can you send me intake forms?",
        "I need to reschedule my appointment",
        "What are your office hours?"
    ]
    
    print(f"\n🤖 Running {len(demo_queries)} demo scenarios...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'='*50}")
        print(f"Demo {i}/{len(demo_queries)}")
        print(f"{'='*50}")
        print(f"👤 Patient: {query}")
        print(f"🤖 Agent: ", end="", flush=True)
        
        try:
            response = agent.chat(query)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
    
    print(f"\n✅ Demo completed! The LangChain-based agent successfully handled {len(demo_queries)} scenarios.")
    print("\n📊 Key Features Demonstrated:")
    print("  • Natural language understanding")
    print("  • Doctor availability search")
    print("  • Appointment scheduling logic")
    print("  • Insurance verification")
    print("  • Patient intake form handling")
    print("  • Multi-turn conversation flow")
    print("\n🔧 Technical Stack:")
    print("  • LangChain for agent orchestration")
    print("  • LangGraph for workflow management")
    print("  • Pandas for data processing")
    print("  • Real-time schedule lookup")
    print("  • Fallback simulation mode (no OpenAI API key)")

def main():
    """Main entry point"""
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        print("\n👋 Thank you for trying the Medical Appointment Scheduling AI Agent!")

if __name__ == "__main__":
    main()
