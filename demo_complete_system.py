"""
Complete Multi-Agent Simulation Demo

This demonstrates the full simulation system:
1. Orchestrator (Generalized Agent) - Registered as SPENDER
2. Specialized Agents - Registered as EARNERS
3. All transactions recorded in Flux/Supabase dashboard
4. Real-time updates visible at http://localhost:3000

Run this to see the entire system in action!
"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from agents.orchestrator import OrchestratorAgent


async def main():
    print("\n" + "="*80)
    print("🎭 COMPLETE MULTI-AGENT SIMULATION SYSTEM")
    print("="*80)
    print("\nThis demo showcases:")
    print("  1. Orchestrator (Generalized Agent) - Takes user prompts, coordinates specialists")
    print("  2. Data Analyst - Analyzes data, creates visualizations")
    print("  3. Content Writer - Creates blog posts and marketing copy")
    print("  4. Researcher - Conducts research and synthesizes information")
    print("  5. Coding Specialist - Reviews code and provides optimization")
    print("  6. Marketing Specialist - Develops marketing strategies")
    print("\n🎯 All agents register in Flux/Supabase:")
    print("  • Orchestrator → SPENDER (has budget, pays specialists)")
    print("  • Specialists → EARNERS (get paid for completed work)")
    print("\n📊 View dashboard: http://localhost:3000")
    print("="*80)
    
    # Initialize the Orchestrator
    print("\n🔄 Initializing Orchestrator (Generalized Agent)...")
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator-demo-001",
        budget=500.0,  # $500 budget
        register_in_flux=True
    )
    
    print("\n✅ Orchestrator initialized and registered as SPENDER in Flux")
    print(f"   Budget: $500.00")
    print(f"   Will hire specialists as needed\n")
    
    # Example user prompts that require multi-agent coordination
    prompts = [
        {
            "number": 1,
            "prompt": "I need a comprehensive analysis of our Q4 sales data with visualizations and insights.",
            "description": "Requires Data Analyst"
        },
        {
            "number": 2,
            "prompt": "Write a 500-word blog post about the benefits of AI agents in modern business.",
            "description": "Requires Content Writer"
        },
        {
            "number": 3,
            "prompt": "Create a complete marketing campaign for a new AI product including market research, content strategy, and campaign plan.",
            "description": "Requires Researcher + Content Writer + Marketing Specialist"
        }
    ]
    
    print("="*80)
    print("📝 DEMO SCENARIOS")
    print("="*80)
    
    # Run the first scenario
    scenario = prompts[0]
    print(f"\n🎯 Scenario {scenario['number']}: {scenario['description']}")
    print(f"   User Request: \"{scenario['prompt']}\"")
    print("\n" + "-"*80)
    
    result = await orchestrator.execute_prompt(scenario['prompt'])
    
    print("\n" + "="*80)
    print("📊 EXECUTION RESULTS")
    print("="*80)
    
    if result['status'] == 'success':
        print(f"\n✅ Task completed successfully!")
        print(f"\n📄 Result:")
        print(f"   {result['result'][:500]}...")  # Show first 500 chars
        print(f"\n💰 Financial Summary:")
        print(f"   Total Spent: {result['total_spent']}")
        print(f"   Budget Remaining: {result['budget_remaining']}")
        print(f"\n⏱️  Performance:")
        print(f"   Duration: {result['duration_seconds']:.2f} seconds")
        print(f"   Workflows Completed: {result['workflows_completed']}")
    else:
        print(f"\n❌ Error: {result.get('error')}")
    
    # Show orchestrator status
    print("\n" + "="*80)
    print("📈 ORCHESTRATOR STATUS")
    print("="*80)
    
    status = await orchestrator.get_status()
    print(f"\nAgent ID: {status['agent_id']}")
    print(f"Type: {status['agent_type']}")
    print(f"Budget Total: {status['budget_total']}")
    print(f"Spent: {status['spent']}")
    print(f"Remaining: {status['remaining']}")
    print(f"Workflows Completed: {status['workflows_completed']}")
    
    # Instructions for interactive mode
    print("\n" + "="*80)
    print("🚀 NEXT STEPS")
    print("="*80)
    print("\n1. Check Flux Dashboard:")
    print("   → http://localhost:3000")
    print("   → See all agents (Orchestrator + Specialists)")
    print("   → View all transactions in real-time")
    print("\n2. Run Interactive Mode:")
    print("   → python run_orchestrator.py")
    print("   → Chat with the Orchestrator")
    print("   → Give it any task and watch it coordinate specialists")
    print("\n3. Run More Demos:")
    print("   → python examples/flux_integration_demo.py")
    print("   → Test individual specialist agents")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
