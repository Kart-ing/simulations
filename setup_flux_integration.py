#!/usr/bin/env python3
"""
Setup Script: Register all specialized agents in Flux Dashboard

This script:
1. Registers all specialized agents as earners in the Flux economy database
2. Verifies the registration
3. Displays agent stats

Run this ONCE before using the agents for the first time.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from integrations.flux_integration import FluxDashboardIntegration


def main():
    """Register all specialized agents."""
    print("\n" + "=" * 70)
    print(" FLUX DASHBOARD INTEGRATION SETUP")
    print("=" * 70)
    print("\nThis will register all specialized agents in the Flux Economy dashboard.")
    print("Agents will appear as 'earners' and their payments will be tracked.\n")
    
    # Initialize integration
    flux = FluxDashboardIntegration()
    
    # Register all agents
    flux.register_all_specialized_agents()
    
    # Display stats
    print("\n" + "=" * 70)
    print(" CURRENT AGENT STATUS")
    print("=" * 70)
    
    agent_ids = [
        'data-analyst-001',
        'content-writer-001',
        'researcher-001',
        'coding-specialist-001',
        'marketing-specialist-001'
    ]
    
    for agent_id in agent_ids:
        stats = flux.get_agent_stats(agent_id)
        if stats:
            print(f"\n{stats['display_name']} ({agent_id})")
            print(f"  Type: {stats['type']}")
            print(f"  Status: {stats['status']}")
            print(f"  Balance: ${stats['balance']/100:.2f}")
            print(f"  Total Earned: ${stats['total_earned']/100:.2f}")
            print(f"  Transactions: {stats['transaction_count']}")
            print(f"  Rating: {stats['rating']}/5.0")
    
    print("\n" + "=" * 70)
    print(" ✅ SETUP COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Start the Flux backend: cd ../flux/flux-economy && ./start-backend.sh")
    print("2. Start the Flux frontend: cd ../flux/flux-economy && ./start-frontend.sh")
    print("3. Visit http://localhost:3000 to see your agents in the dashboard")
    print("4. Run a scenario to see agents earn money in real-time!")
    print()


if __name__ == "__main__":
    main()
