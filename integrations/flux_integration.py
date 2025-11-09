"""
Flux Dashboard Integration for AgentPay Specialized Agents

This module integrates the Dedalus-powered agents with the Flux Economy dashboard,
ensuring all agents are registered and their earnings are tracked in real-time.

Uses the Flux backend API to register agents in Supabase.
"""

import os
import sys
import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://rvprysqboidvnxqfbtjt.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2cHJ5c3Fib2lkdm54cWZidGp0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MjM5OTYsImV4cCI6MjA3ODE5OTk5Nn0.c1iCpeN4WODCA1j-_37wQ4OGQocEJFHjL8Zr4YzCB2U')


class FluxDashboardIntegration:
    """
    Integration layer between specialized agents and Flux dashboard (Supabase).
    
    Handles:
    - Agent registration in Supabase via Flux
    - Real-time earnings updates
    - Transaction recording
    """
    
    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None
    ):
        """
        Initialize Flux integration.
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon/service key
        """
        # Set Supabase credentials
        self.supabase_url = supabase_url or SUPABASE_URL
        self.supabase_key = supabase_key or SUPABASE_KEY
        
        # Initialize Supabase client
        try:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            print(f"✅ Connected to Supabase at {self.supabase_url}")
        except Exception as e:
            print(f"⚠️  Could not connect to Supabase: {e}")
            self.supabase = None
    
    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        display_name: Optional[str] = None,
        categories: Optional[List[str]] = None,
        hourly_rate: Optional[float] = None
    ) -> bool:
        """
        Register a specialized agent in the Flux dashboard (Supabase).
        
        Args:
            agent_id: Unique agent identifier (will be used as 'name', UUID generated for 'id')
            agent_name: Agent name (e.g., "data-analyst-001")
            agent_type: Agent type (e.g., "DataAnalyst", "ContentWriter")
            display_name: Human-readable name
            categories: List of categories/skills
            hourly_rate: Agent's hourly rate
            
        Returns:
            True if registered successfully
        """
        if not self.supabase:
            print(f"❌ Supabase not connected. Cannot register agent {agent_id}")
            return False
        
        try:
            # Check if agent already exists (by name, not UUID id)
            result = self.supabase.table('agents').select('id').eq('name', agent_name).execute()
            
            if result.data:
                print(f"   ℹ️  Agent {agent_name} already registered")
                return True
            
            # Generate UUID for the id field
            import uuid
            agent_uuid = str(uuid.uuid4())
            
            # Prepare agent data
            display = display_name or agent_type.replace('Agent', ' Agent')
            now = datetime.now().isoformat() + 'Z'
            
            agent_data = {
                'id': agent_uuid,  # UUID for Supabase
                'name': agent_name,  # Readable name like "data-analyst-001"
                'display_name': display,
                'type': 'earner',  # All specialized agents are earners
                'balance': 0,
                'hold': 0,
                'total_spent': 0,
                'total_earned': 0,
                'transaction_count': 0,
                'avg_transaction_size': 0,
                'status': 'active',
                'rating': 5.0,
                'completion_rate': 100.0,
                'approval_rate': 100.0,
                'categories': categories or [agent_type],  # Supabase handles JSON
                'created_at': now,
                'updated_at': now
            }
            
            # Insert agent into Supabase
            result = self.supabase.table('agents').insert(agent_data).execute()
            
            if result.data:
                print(f"✅ Registered agent in Supabase: {agent_name} ({display}) [UUID: {agent_uuid}]")
                return True
            else:
                print(f"⚠️  Agent registration returned no data: {agent_name}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to register agent {agent_name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def record_earning(
        self,
        agent_id: str,
        client_id: str,
        amount_cents: int,
        service_description: str,
        task_details: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Record an earning transaction for an agent in Supabase.
        
        Args:
            agent_id: Agent name (e.g., "data-analyst-001")
            client_id: Client who paid
            amount_cents: Amount in cents
            service_description: Description of service provided
            task_details: Optional details about the task
            
        Returns:
            Transaction ID if successful, None otherwise
        """
        if not self.supabase:
            print(f"❌ Supabase not connected. Cannot record earning for {agent_id}")
            return None
        
        try:
            # Find agent by name to get UUID
            agent_result = self.supabase.table('agents').select('id, total_earned, total_spent, transaction_count').eq('name', agent_id).execute()
            
            if not agent_result.data:
                print(f"⚠️  Agent {agent_id} not found in Supabase")
                return None
            
            agent = agent_result.data[0]
            agent_uuid = agent['id']
            
            # Generate transaction ID
            import uuid
            tx_id = str(uuid.uuid4())
            now = datetime.now().isoformat() + 'Z'
            
            # Insert transaction
            transaction_data = {
                'id': tx_id,
                'type': 'payment',
                'from_agent_id': None,  # Client (no ID in system yet)
                'from_agent_name': client_id,
                'to_agent_id': agent_uuid,  # Use UUID from Supabase
                'to_agent_name': agent_id,
                'amount': amount_cents,
                'purpose': service_description,
                'memo': json.dumps(task_details) if task_details else None,
                'status': 'completed',
                'consensus_required': False,
                'consensus_result': None,
                'timestamp': now
            }
            
            result = self.supabase.table('transactions').insert(transaction_data).execute()
            
            if not result.data:
                print(f"⚠️  Transaction insert returned no data")
            
            # Calculate new stats
            new_total_earned = agent['total_earned'] + amount_cents
            new_transaction_count = agent['transaction_count'] + 1
            new_avg = (new_total_earned + agent['total_spent']) // new_transaction_count if new_transaction_count > 0 else 0
            
            # Update agent stats
            update_data = {
                'total_earned': new_total_earned,
                'balance': new_total_earned - agent['total_spent'],  # Balance = earned - spent
                'transaction_count': new_transaction_count,
                'avg_transaction_size': new_avg,
                'updated_at': now
            }
            
            self.supabase.table('agents').update(update_data).eq('id', agent_uuid).execute()
            
            print(f"   💰 {agent_id} earned ${amount_cents/100:.2f} (total: ${new_total_earned/100:.2f})")
            
            return tx_id
            
        except Exception as e:
            print(f"❌ Failed to record earning for {agent_id}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_agent_stats(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current stats for an agent from Supabase.
        
        Args:
            agent_id: Agent name (e.g., "data-analyst-001")
            
        Returns:
            Dictionary with agent stats
        """
        if not self.supabase:
            print(f"❌ Supabase not connected. Cannot get stats for {agent_id}")
            return None
        
        try:
            # Query by name, not UUID
            result = self.supabase.table('agents').select('*').eq('name', agent_id).execute()
            
            if not result.data:
                return None
            
            agent = result.data[0]
            
            return {
                'id': agent['id'],
                'name': agent['name'],
                'display_name': agent['display_name'],
                'type': agent['type'],
                'balance': agent['balance'],
                'total_earned': agent['total_earned'],
                'total_spent': agent['total_spent'],
                'transaction_count': agent['transaction_count'],
                'avg_transaction_size': agent['avg_transaction_size'],
                'status': agent['status'],
                'rating': agent.get('rating'),
                'completion_rate': agent.get('completion_rate'),
                'approval_rate': agent.get('approval_rate')
            }
            
        except Exception as e:
            print(f"❌ Failed to get stats for {agent_id}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def register_all_specialized_agents(self):
        """
        Register all specialized agents in the Flux dashboard.
        
        This should be called once during setup.
        """
        agents = [
            {
                'agent_id': 'data-analyst-001',
                'agent_name': 'data-analyst-001',
                'agent_type': 'DataAnalyst',
                'display_name': 'Data Analyst AI',
                'categories': ['Data Analysis', 'Statistics', 'Visualization'],
                'hourly_rate': 25.0
            },
            {
                'agent_id': 'content-writer-001',
                'agent_name': 'content-writer-001',
                'agent_type': 'ContentWriter',
                'display_name': 'Content Writer AI',
                'categories': ['Content Writing', 'Copywriting', 'Blogging'],
                'hourly_rate': None  # Per-word pricing
            },
            {
                'agent_id': 'researcher-001',
                'agent_name': 'researcher-001',
                'agent_type': 'Researcher',
                'display_name': 'Research Specialist AI',
                'categories': ['Research', 'Fact-Checking', 'Analysis'],
                'hourly_rate': 35.0
            },
            {
                'agent_id': 'coding-specialist-001',
                'agent_name': 'coding-specialist-001',
                'agent_type': 'CodingSpecialist',
                'display_name': 'Coding Specialist AI',
                'categories': ['Code Review', 'Debugging', 'Optimization'],
                'hourly_rate': 50.0
            },
            {
                'agent_id': 'marketing-specialist-001',
                'agent_name': 'marketing-specialist-001',
                'agent_type': 'MarketingSpecialist',
                'display_name': 'Marketing Specialist AI',
                'categories': ['Marketing Strategy', 'Campaigns', 'Analytics'],
                'hourly_rate': 40.0
            }
        ]
        
        print("=" * 60)
        print("Registering Specialized Agents in Flux Dashboard")
        print("=" * 60)
        
        for agent in agents:
            self.register_agent(**agent)
        
        print("=" * 60)
        print("✅ All agents registered successfully!")
        print("=" * 60)


# Singleton instance
_flux_integration = None

def get_flux_integration() -> FluxDashboardIntegration:
    """Get or create the Flux integration singleton."""
    global _flux_integration
    if _flux_integration is None:
        _flux_integration = FluxDashboardIntegration()
    return _flux_integration


# Convenience functions for agents to use
def register_agent_in_flux(
    agent_id: str,
    agent_name: str,
    agent_type: str,
    **kwargs
) -> bool:
    """Register an agent in Flux dashboard."""
    flux = get_flux_integration()
    return flux.register_agent(agent_id, agent_name, agent_type, **kwargs)


def record_agent_earning(
    agent_id: str,
    client_id: str,
    amount_cents: int,
    service_description: str,
    task_details: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """Record an earning for an agent in Flux dashboard."""
    flux = get_flux_integration()
    return flux.record_earning(
        agent_id, client_id, amount_cents, 
        service_description, task_details
    )


def record_agent_spending(
    agent_id: str,
    recipient_id: str,
    amount_cents: int,
    service_description: str,
    task_details: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """
    Record a spending transaction for an agent (like orchestrator paying other agents).
    
    Args:
        agent_id: Agent making the payment (spender)
        recipient_id: Agent receiving the payment (earner)
        amount_cents: Amount in cents
        service_description: Description of service paid for
        task_details: Optional details about the task
        
    Returns:
        Transaction ID if successful, None otherwise
    """
    flux = get_flux_integration()
    
    if not flux.supabase:
        print(f"❌ Supabase not connected. Cannot record spending for {agent_id}")
        return None
    
    try:
        # Find spender agent by name to get UUID
        spender_result = flux.supabase.table('agents').select('id, total_earned, total_spent, transaction_count, balance').eq('name', agent_id).execute()
        
        if not spender_result.data:
            print(f"⚠️  Spender agent {agent_id} not found in Supabase")
            return None
        
        spender = spender_result.data[0]
        spender_uuid = spender['id']
        
        # Find recipient agent by name to get UUID
        recipient_result = flux.supabase.table('agents').select('id').eq('name', recipient_id).execute()
        recipient_uuid = recipient_result.data[0]['id'] if recipient_result.data else None
        
        # Generate transaction ID
        import uuid
        tx_id = str(uuid.uuid4())
        now = datetime.now().isoformat() + 'Z'
        
        # Insert transaction
        transaction_data = {
            'id': tx_id,
            'type': 'payment',
            'from_agent_id': spender_uuid,  # Orchestrator UUID
            'from_agent_name': agent_id,
            'to_agent_id': recipient_uuid,  # Specialist UUID
            'to_agent_name': recipient_id,
            'amount': amount_cents,
            'purpose': service_description,
            'memo': json.dumps(task_details) if task_details else None,
            'status': 'completed',
            'consensus_required': False,
            'consensus_result': None,
            'timestamp': now
        }
        
        result = flux.supabase.table('transactions').insert(transaction_data).execute()
        
        if not result.data:
            print(f"⚠️  Transaction insert returned no data")
        
        # Calculate new stats for spender
        new_total_spent = spender['total_spent'] + amount_cents
        new_balance = spender['total_earned'] - new_total_spent
        new_transaction_count = spender['transaction_count'] + 1
        new_avg = (spender['total_earned'] + new_total_spent) // new_transaction_count if new_transaction_count > 0 else 0
        
        # Update spender agent stats
        update_data = {
            'total_spent': new_total_spent,
            'balance': new_balance,
            'transaction_count': new_transaction_count,
            'avg_transaction_size': new_avg,
            'updated_at': now
        }
        
        flux.supabase.table('agents').update(update_data).eq('id', spender_uuid).execute()
        
        print(f"   💸 {agent_id} spent ${amount_cents/100:.2f} → {recipient_id} (balance: ${new_balance/100:.2f})")
        
        return tx_id
        
    except Exception as e:
        print(f"❌ Failed to record spending for {agent_id}: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_agent_dashboard_stats(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get agent stats from Flux dashboard."""
    flux = get_flux_integration()
    return flux.get_agent_stats(agent_id)


# Setup script
if __name__ == "__main__":
    """Run this to register all agents in Flux dashboard."""
    flux = FluxDashboardIntegration()
    flux.register_all_specialized_agents()
    
    # Display current stats
    print("\n" + "=" * 60)
    print("Current Agent Stats")
    print("=" * 60)
    
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
            print(f"\n{stats['display_name']}:")
            print(f"  Balance: ${stats['balance']/100:.2f}")
            print(f"  Total Earned: ${stats['total_earned']/100:.2f}")
            print(f"  Transactions: {stats['transaction_count']}")
            print(f"  Status: {stats['status']}")
