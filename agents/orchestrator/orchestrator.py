"""
Orchestrator Agent - The Generalized Agent

This is the main coordinator agent that:
- Takes natural language prompts from users
- Breaks down complex tasks into subtasks
- Hires specialized agents to complete work
- Manages workflows and payments
- Registers itself as a "spender" in Flux

The Orchestrator is registered as a "spender" type agent in Supabase.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

from dedalus_labs import AsyncDedalus, DedalusRunner

# Import integrations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from tools.payment_tools import pay_for_service, check_balance, get_quote
from integrations.flux_integration import (
    register_agent_in_flux,
    record_agent_earning,
    record_agent_spending,
    get_agent_dashboard_stats
)


class OrchestratorAgent:
    """
    The Orchestrator (Generalized Agent) - Coordinates specialized agents.
    
    This agent:
    - Takes user prompts
    - Plans multi-agent workflows
    - Hires and manages specialized agents
    - Handles all payments (registered as SPENDER in Flux)
    """
    
    def __init__(
        self,
        agent_id: str = "orchestrator-001",
        budget: float = 1000.0,  # Default budget if not in DB
        model: str = "openai/gpt-4.1",
        register_in_flux: bool = True
    ):
        """
        Initialize the Orchestrator agent.
        
        Args:
            agent_id: Unique identifier
            budget: Default budget in dollars (used only if agent not in DB)
            model: LLM model to use
            register_in_flux: Whether to register in Flux dashboard
        """
        self.agent_id = agent_id
        self.model = model
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Available specialized agents (lazy loaded)
        self.available_agents = {
            'data_analyst': {
                'class': None,  # Lazy loaded
                'module': 'agents.specialized.data_analyst',
                'class_name': 'DataAnalystAgent',
                'instance': None,
                'rate': 2500,  # $25/hour in cents
                'description': 'Data analysis, statistics, visualization'
            },
            'content_writer': {
                'class': None,
                'module': 'agents.specialized.content_writer',
                'class_name': 'ContentWriterAgent',
                'instance': None,
                'rate': 10,  # $0.10/word in cents
                'description': 'Blog posts, marketing copy, content creation'
            },
            'researcher': {
                'class': None,
                'module': 'agents.specialized.researcher',
                'class_name': 'ResearcherAgent',
                'instance': None,
                'rate': 3500,  # $35/hour in cents
                'description': 'Research, fact-checking, information synthesis'
            },
            'coding_specialist': {
                'class': None,
                'module': 'agents.specialized.coding_specialist',
                'class_name': 'CodingSpecialistAgent',
                'instance': None,
                'rate': 5000,  # $50/hour in cents
                'description': 'Code review, debugging, optimization'
            },
            'marketing_specialist': {
                'class': None,
                'module': 'agents.specialized.marketing_specialist',
                'class_name': 'MarketingSpecialistAgent',
                'instance': None,
                'rate': 4000,  # $40/hour in cents
                'description': 'Marketing strategy, campaigns, analytics'
            }
        }
        
        # Workflow history
        self.workflows: List[Dict[str, Any]] = []
        
        # Register in Flux as SPENDER and get/set budget
        if register_in_flux:
            try:
                # First check if agent already exists to get current balance
                from integrations.flux_integration import get_flux_integration
                flux = get_flux_integration()
                existing_stats = get_agent_dashboard_stats(self.agent_id)
                
                if existing_stats and 'balance' in existing_stats:
                    # Agent exists - use balance from database
                    self.budget_cents = existing_stats['balance']
                    self.spent_cents = existing_stats.get('total_spent', 0)
                    print(f"✅ Loaded orchestrator from DB - Balance: ${self.budget_cents/100:.2f}")
                else:
                    # New agent - register with default budget
                    self.budget_cents = int(budget * 100)
                    self.spent_cents = 0
                    
                    register_agent_in_flux(
                        agent_id=self.agent_id,
                        agent_name=self.agent_id,
                        agent_type="Orchestrator",
                        display_name="AI Orchestrator (Generalized Agent)",
                        categories=["Orchestration", "Coordination", "Management"],
                        hourly_rate=None  # Orchestrator doesn't charge, it pays
                    )
                    
                    # Update agent type to "spender" after registration
                    if flux.supabase:
                        # Find agent and update to spender type
                        result = flux.supabase.table('agents').select('id').eq('name', self.agent_id).execute()
                        if result.data:
                            agent_uuid = result.data[0]['id']
                            flux.supabase.table('agents').update({
                                'type': 'spender',  # Change to spender
                                'balance': self.budget_cents,  # Set initial budget
                                'updated_at': datetime.now().isoformat() + 'Z'
                            }).eq('id', agent_uuid).execute()
                            print(f"✅ Registered orchestrator as SPENDER with ${budget:.2f} budget")
                
            except Exception as e:
                print(f"⚠️  Could not register orchestrator in Flux: {e}")
                # Fallback to default budget
                self.budget_cents = int(budget * 100)
                self.spent_cents = 0
        else:
            # Not registering in Flux - use default budget
            self.budget_cents = int(budget * 100)
            self.spent_cents = 0
    
    # ==================== ORCHESTRATION TOOLS ====================
    
    def analyze_task(self, user_prompt: str) -> str:
        """
        Analyze user prompt and determine which agents are needed.
        
        Args:
            user_prompt: Natural language task description
            
        Returns:
            JSON string with task breakdown
        """
        try:
            # This will be done by Dedalus reasoning
            return json.dumps({
                "status": "ready_to_analyze",
                "prompt": user_prompt,
                "available_agents": {
                    name: info['description'] 
                    for name, info in self.available_agents.items()
                },
                "message": "Dedalus will analyze and create execution plan"
            }, indent=2)
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def check_budget(self) -> str:
        """
        Check current budget status (pulls latest from database).
        
        Returns:
            JSON string with budget information
        """
        try:
            # Get latest stats from database
            stats = get_agent_dashboard_stats(self.agent_id)
            if stats and 'balance' in stats:
                self.budget_cents = stats['balance'] + stats.get('total_spent', 0)
                self.spent_cents = stats.get('total_spent', 0)
                remaining = stats['balance']
            else:
                # Fallback to local tracking
                remaining = self.budget_cents - self.spent_cents
            
            return json.dumps({
                "total_budget": f"${self.budget_cents/100:.2f}",
                "spent": f"${self.spent_cents/100:.2f}",
                "remaining": f"${remaining/100:.2f}",
                "remaining_cents": remaining,
                "can_spend": remaining > 0
            }, indent=2)
        except Exception as e:
            # Fallback to local tracking on error
            remaining = self.budget_cents - self.spent_cents
            return json.dumps({
                "total_budget": f"${self.budget_cents/100:.2f}",
                "spent": f"${self.spent_cents/100:.2f}",
                "remaining": f"${remaining/100:.2f}",
                "remaining_cents": remaining,
                "can_spend": remaining > 0,
                "note": f"Using local tracking (DB error: {str(e)})"
            }, indent=2)
    
    async def hire_agent(
        self,
        agent_type: str,
        task_description: str,
        estimated_cost_cents: int
    ) -> str:
        """
        Hire a specialized agent to complete a task.
        
        Args:
            agent_type: Type of agent (data_analyst, content_writer, etc.)
            task_description: Task for the agent
            estimated_cost_cents: Estimated cost in cents
            
        Returns:
            JSON string with task result
        """
        try:
            if agent_type not in self.available_agents:
                return json.dumps({
                    "status": "error",
                    "error": f"Unknown agent type: {agent_type}"
                })
            
            # Check budget
            remaining = self.budget_cents - self.spent_cents
            if estimated_cost_cents > remaining:
                return json.dumps({
                    "status": "error",
                    "error": f"Insufficient budget. Need ${estimated_cost_cents/100:.2f}, have ${remaining/100:.2f}"
                })
            
            # Get or create agent instance
            agent_info = self.available_agents[agent_type]
            if agent_info['instance'] is None:
                # Lazy load the agent class
                if agent_info['class'] is None:
                    import importlib
                    module = importlib.import_module(agent_info['module'])
                    agent_info['class'] = getattr(module, agent_info['class_name'])
                
                agent_info['instance'] = agent_info['class'](
                    register_in_flux=False  # Already registered
                )
            
            agent = agent_info['instance']
            
            print(f"\n🤝 Hiring {agent_type}...")
            print(f"   Task: {task_description}")
            print(f"   Estimated cost: ${estimated_cost_cents/100:.2f}")
            
            # Execute task
            result = await agent.execute_task(
                task_description=task_description,
                client_id=self.agent_id,
                auto_charge=True
            )
            
            # Update spent amount and record transaction
            if result.get('status') == 'success':
                # Parse earnings from result
                earnings_str = result.get('earnings', '$0.00')
                earnings_cents = int(float(earnings_str.replace('$', '')) * 100)
                
                # Record spending in Flux (orchestrator pays the agent)
                try:
                    # Get the actual agent ID from the instance
                    recipient_agent_id = agent.agent_id if hasattr(agent, 'agent_id') else f"{agent_type}-001"
                    
                    record_agent_spending(
                        agent_id=self.agent_id,
                        recipient_id=recipient_agent_id,
                        amount_cents=earnings_cents,
                        service_description=f"{agent_type}: {task_description[:100]}",
                        task_details={
                            'agent_type': agent_type,
                            'task': task_description,
                            'timestamp': datetime.now().isoformat()
                        }
                    )
                except Exception as e:
                    print(f"⚠️  Could not record spending transaction: {e}")
                
                self.spent_cents += earnings_cents
                
                print(f"   ✅ Task completed! Cost: ${earnings_cents/100:.2f}")
                print(f"   Budget remaining: ${(self.budget_cents - self.spent_cents)/100:.2f}")
            
            return json.dumps({
                "status": "success",
                "agent_type": agent_type,
                "task": task_description,
                "result": result,
                "cost": f"${earnings_cents/100:.2f}" if result.get('status') == 'success' else "$0.00"
            }, indent=2, default=str)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def create_execution_plan(
        self,
        user_prompt: str,
        required_agents: List[str],
        workflow_steps: List[str]
    ) -> str:
        """
        Create an execution plan for the workflow.
        
        Args:
            user_prompt: Original user request
            required_agents: List of agent types needed
            workflow_steps: List of steps in order
            
        Returns:
            JSON string with execution plan
        """
        try:
            plan = {
                "user_request": user_prompt,
                "required_agents": required_agents,
                "steps": workflow_steps,
                "estimated_total_cost": sum(
                    self.available_agents[agent]['rate'] 
                    for agent in required_agents 
                    if agent in self.available_agents
                ),
                "budget_check": "OK" if self.budget_cents > sum(
                    self.available_agents[agent]['rate'] 
                    for agent in required_agents 
                    if agent in self.available_agents
                ) else "INSUFFICIENT"
            }
            
            return json.dumps(plan, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def finalize_workflow(
        self,
        workflow_summary: str,
        total_cost_cents: int
    ) -> str:
        """
        Finalize and record the completed workflow.
        
        Args:
            workflow_summary: Summary of work completed
            total_cost_cents: Total cost in cents
            
        Returns:
            JSON string with workflow record
        """
        try:
            workflow_record = {
                "id": len(self.workflows) + 1,
                "summary": workflow_summary,
                "total_cost": f"${total_cost_cents/100:.2f}",
                "completed_at": datetime.now().isoformat(),
                "budget_remaining": f"${(self.budget_cents - self.spent_cents)/100:.2f}"
            }
            
            self.workflows.append(workflow_record)
            
            return json.dumps({
                "status": "success",
                "workflow": workflow_record
            }, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    # ==================== MAIN EXECUTION ====================
    
    async def execute_prompt(
        self,
        user_prompt: str
    ) -> Dict[str, Any]:
        """
        Execute a user prompt by orchestrating specialized agents.
        
        Args:
            user_prompt: Natural language task description
            
        Returns:
            Dictionary with execution results
        """
        start_time = datetime.now()
        
        print(f"\n{'='*70}")
        print(f"🎭 ORCHESTRATOR EXECUTING PROMPT")
        print(f"{'='*70}")
        print(f"Prompt: {user_prompt}")
        print(f"Budget: ${self.budget_cents/100:.2f}")
        print(f"{'='*70}\n")
        
        # Build the orchestration prompt for Dedalus
        orchestration_prompt = f"""
You are an AI Orchestrator that coordinates specialized AI agents.

USER REQUEST: {user_prompt}

YOUR BUDGET: ${self.budget_cents/100:.2f}
ALREADY SPENT: ${self.spent_cents/100:.2f}
REMAINING: ${(self.budget_cents - self.spent_cents)/100:.2f}

AVAILABLE SPECIALIZED AGENTS:
{json.dumps({name: info['description'] + f" (${info['rate']/100:.2f}/hour)" for name, info in self.available_agents.items()}, indent=2)}

YOUR TOOLS:
1. analyze_task(user_prompt) - Analyze what needs to be done
2. check_budget() - Check current budget status
3. create_execution_plan(user_prompt, required_agents, workflow_steps) - Plan the workflow
4. hire_agent(agent_type, task_description, estimated_cost_cents) - Hire an agent to do work
5. finalize_workflow(workflow_summary, total_cost_cents) - Complete and record workflow

INSTRUCTIONS:
1. Analyze the user's request
2. Determine which specialized agents are needed
3. Create an execution plan with steps
4. Check if you have sufficient budget
5. Hire agents one by one to complete each step
6. Collect all results
7. Finalize the workflow with a summary
8. Return a comprehensive response to the user

BEGIN ORCHESTRATING NOW.
"""
        
        # Available tools for orchestrator
        tools = [
            self.analyze_task,
            self.check_budget,
            self.create_execution_plan,
            self.hire_agent,
            self.finalize_workflow
        ]
        
        try:
            # Execute with Dedalus
            result = await self.runner.run(
                input=orchestration_prompt,
                model=self.model,
                tools=tools
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                "status": "success",
                "orchestrator_id": self.agent_id,
                "user_prompt": user_prompt,
                "result": result.final_output,
                "total_spent": f"${self.spent_cents/100:.2f}",
                "budget_remaining": f"${(self.budget_cents - self.spent_cents)/100:.2f}",
                "duration_seconds": duration,
                "workflows_completed": len(self.workflows),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "orchestrator_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        stats = get_agent_dashboard_stats(self.agent_id)
        
        return {
            "agent_id": self.agent_id,
            "agent_type": "Orchestrator (Spender)",
            "budget_total": f"${self.budget_cents/100:.2f}",
            "spent": f"${self.spent_cents/100:.2f}",
            "remaining": f"${(self.budget_cents - self.spent_cents)/100:.2f}",
            "workflows_completed": len(self.workflows),
            "flux_stats": stats,
            "status": "active"
        }


# ==================== DEMO ====================

async def demo():
    """
    Demo of the Orchestrator executing a complex prompt.
    """
    print("\n" + "="*70)
    print("🎭 ORCHESTRATOR DEMO - Generalized Agent")
    print("="*70)
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator-001",
        budget=1000.0,
        register_in_flux=True
    )
    
    # Example user prompts
    prompts = [
        "I need a comprehensive marketing campaign for a new AI product. Include market research, blog content, and a campaign strategy.",
        
        "Analyze our sales data from the last 6 months and create a detailed report with visualizations.",
        
        "Review the Python codebase in our repository and provide optimization suggestions."
    ]
    
    # Execute first prompt
    print(f"\n📝 User Prompt:")
    print(f"   '{prompts[0]}'")
    
    result = await orchestrator.execute_prompt(prompts[0])
    
    print(f"\n{'='*70}")
    print("📊 EXECUTION RESULT")
    print(f"{'='*70}")
    print(json.dumps(result, indent=2, default=str))
    
    # Show status
    status = await orchestrator.get_status()
    print(f"\n{'='*70}")
    print("📈 ORCHESTRATOR STATUS")
    print(f"{'='*70}")
    print(json.dumps(status, indent=2, default=str))


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
