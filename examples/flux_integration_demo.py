#!/usr/bin/env python3
"""
Demo: Test Flux Integration with DataAnalyst Agent

This demo:
1. Creates a DataAnalyst agent
2. Executes a sample task
3. Shows the earning recorded in Flux dashboard
4. Displays updated stats
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.specialized import DataAnalystAgent
from integrations.flux_integration import get_agent_dashboard_stats


async def main():
    """Run the demo."""
    print("\n" + "=" * 70)
    print(" FLUX INTEGRATION DEMO - Data Analyst Agent")
    print("=" * 70)
    
    # Sample dataset
    sample_data = {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "sales": [12000, 15000, 13000, 18000, 22000, 25000],
        "expenses": [8000, 9000, 8500, 10000, 12000, 13000],
        "profit": [4000, 6000, 4500, 8000, 10000, 12000]
    }
    
    # Initialize agent (auto-registers in Flux)
    print("\n📊 Initializing Data Analyst Agent...")
    analyst = DataAnalystAgent(
        agent_id="data-analyst-001",
        hourly_rate=25.0,
        register_in_flux=True
    )
    
    # Get initial stats
    print("\n📈 Initial Stats from Flux Dashboard:")
    initial_stats = get_agent_dashboard_stats("data-analyst-001")
    if initial_stats:
        print(f"   Balance: ${initial_stats['balance']/100:.2f}")
        print(f"   Total Earned: ${initial_stats['total_earned']/100:.2f}")
        print(f"   Transactions: {initial_stats['transaction_count']}")
    
    # Execute task
    print("\n🔄 Executing analysis task...")
    print("   Task: Analyze sales and expense trends")
    print("   Client: marketing-team-001")
    
    result = await analyst.execute_task(
        task_description="Analyze the sales and expense data. Calculate profit margins and identify trends. Provide a summary report.",
        client_id="marketing-team-001",
        data=sample_data,
        auto_charge=True
    )
    
    print(f"\n✅ Task completed!")
    print(f"   Status: {result['status']}")
    print(f"   Time spent: {result['time_spent_hours']} hours")
    print(f"   Earnings: {result['earnings']}")
    
    # Get updated stats
    print("\n📈 Updated Stats from Flux Dashboard:")
    updated_stats = get_agent_dashboard_stats("data-analyst-001")
    if updated_stats:
        print(f"   Balance: ${updated_stats['balance']/100:.2f}")
        print(f"   Total Earned: ${updated_stats['total_earned']/100:.2f}")
        print(f"   Transactions: {updated_stats['transaction_count']}")
        
        # Calculate difference
        earnings_diff = updated_stats['total_earned'] - initial_stats['total_earned']
        print(f"\n   💰 New earnings: ${earnings_diff/100:.2f}")
    
    print("\n" + "=" * 70)
    print(" 🎉 DEMO COMPLETE!")
    print("=" * 70)
    print("\nCheck the Flux dashboard at http://localhost:3000 to see:")
    print("  - Data Analyst Agent in the 'Top Earners' list")
    print("  - New transaction in recent activity")
    print("  - Updated agent stats")
    print()


if __name__ == "__main__":
    asyncio.run(main())
