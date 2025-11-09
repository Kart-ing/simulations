#!/usr/bin/env python3
"""
Interactive Simulation - Talk to the Orchestrator

This script provides an interactive CLI where you can chat with the
Orchestrator (Generalized Agent) and watch it coordinate specialized
agents to complete your tasks.

The Orchestrator will:
1. Understand your request
2. Break it down into subtasks
3. Hire the appropriate specialized agents
4. Coordinate their work
5. Return comprehensive results

All agents (Orchestrator + specialists) will update in Flux dashboard!
"""

import sys
import asyncio
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / '.env')

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.orchestrator import OrchestratorAgent


async def interactive_mode():
    """Run interactive CLI for the orchestrator."""
    
    print("\n" + "="*70)
    print("🎭 AI ORCHESTRATOR - Interactive Mode")
    print("="*70)
    print("\nWelcome! I'm the Orchestrator, a generalized AI agent that can")
    print("coordinate multiple specialized agents to complete complex tasks.")
    print("\nI can help you with:")
    print("  • Data analysis and visualization")
    print("  • Content writing and marketing")
    print("  • Research and fact-checking")
    print("  • Code review and optimization")
    print("  • Marketing strategy and campaigns")
    print("\nI have a $1000 budget and will hire the right specialists for your task.")
    print("="*70)
    
    # Initialize orchestrator
    print("\n🔄 Initializing Orchestrator...")
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator-001",
        budget=1000.0,
        register_in_flux=True
    )
    
    print("\n✅ Orchestrator ready!")
    print(f"   Budget: ${orchestrator.budget_cents/100:.2f}")
    print(f"   Registered as SPENDER in Flux\n")
    
    # Interactive loop
    conversation_count = 0
    
    while True:
        try:
            # Get user input
            print("="*70)
            user_input = input("\n💬 Your request (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                print("⚠️  Please enter a request.")
                continue
            
            if user_input.lower() == 'status':
                # Show status
                status = await orchestrator.get_status()
                print("\n📊 ORCHESTRATOR STATUS:")
                print(f"   Budget Total: {status['budget_total']}")
                print(f"   Spent: {status['spent']}")
                print(f"   Remaining: {status['remaining']}")
                print(f"   Workflows Completed: {status['workflows_completed']}")
                continue
            
            conversation_count += 1
            
            # Execute the prompt
            print(f"\n🎭 Orchestrator is working on your request...")
            print("   (This may take a moment as I coordinate with specialists)\n")
            
            result = await orchestrator.execute_prompt(user_input)
            
            # Display result
            print("\n" + "="*70)
            print("✅ COMPLETED!")
            print("="*70)
            
            if result['status'] == 'success':
                print(f"\n📋 Result:")
                print(f"{result['result']}\n")
                print(f"💰 Cost: {result['total_spent']}")
                print(f"💵 Budget Remaining: {result['budget_remaining']}")
                print(f"⏱️  Duration: {result['duration_seconds']:.2f}s")
            else:
                print(f"\n❌ Error: {result.get('error')}")
            
            print(f"\n💡 Tip: Check http://localhost:3000 to see all transactions in the Flux dashboard!")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Final summary
    print("\n" + "="*70)
    print("📊 SESSION SUMMARY")
    print("="*70)
    print(f"Requests processed: {conversation_count}")
    print(f"Total spent: ${orchestrator.spent_cents/100:.2f}")
    print(f"Budget remaining: ${(orchestrator.budget_cents - orchestrator.spent_cents)/100:.2f}")
    print(f"Workflows completed: {len(orchestrator.workflows)}")
    print("="*70 + "\n")


async def demo_mode():
    """Run a quick demo with preset prompts."""
    
    print("\n" + "="*70)
    print("🎭 ORCHESTRATOR DEMO MODE")
    print("="*70)
    
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator-demo-001",
        budget=500.0,
        register_in_flux=True
    )
    
    demo_prompts = [
        "Analyze sales data and create a visualization showing trends",
        "Write a 500-word blog post about AI agents in business"
    ]
    
    for i, prompt in enumerate(demo_prompts, 1):
        print(f"\n{'='*70}")
        print(f"Demo {i}/{len(demo_prompts)}")
        print(f"{'='*70}")
        print(f"Prompt: {prompt}\n")
        
        result = await orchestrator.execute_prompt(prompt)
        
        print(f"\nResult: {result['status']}")
        if result['status'] == 'success':
            print(f"Cost: {result['total_spent']}")
            print(f"Remaining: {result['budget_remaining']}")
        
        if i < len(demo_prompts):
            print("\n⏳ Waiting 3 seconds...")
            await asyncio.sleep(3)
    
    print("\n✅ Demo complete!")


def main():
    """Main entry point."""
    import sys
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'interactive'
    
    if mode == 'demo':
        asyncio.run(demo_mode())
    else:
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
