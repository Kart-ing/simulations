"""
CodingSpecialist Agent - Specialized in code review, debugging, and optimization.

This agent can:
- Review code for quality and best practices
- Debug and fix issues
- Optimize performance
- Suggest improvements
- Request payments for completed work
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import ast

from dedalus_labs import AsyncDedalus, DedalusRunner

# Import integrations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from integrations.flux_integration import (
    register_agent_in_flux,
    record_agent_earning,
    get_agent_dashboard_stats
)


class CodingSpecialistAgent:
    """
    A Dedalus-powered coding specialist agent with built-in code analysis tools.
    
    Uses Claude 3.5 Sonnet for superior code understanding and generation.
    """
    
    def __init__(
        self,
        agent_id: str = "coding-specialist-001",
        hourly_rate_cents: int = 5000,  # $50/hour
        model: str = "anthropic/claude-sonnet-4-20250514",
        register_in_flux: bool = True
    ):
        """
        Initialize the CodingSpecialist agent.
        
        Args:
            agent_id: Unique identifier for this agent
            hourly_rate_cents: Rate per hour in cents
            model: LLM model to use (Claude 3.5 Sonnet for best coding)
            register_in_flux: Whether to register in Flux dashboard
        """
        self.agent_id = agent_id
        self.hourly_rate_cents = hourly_rate_cents
        self.model = model
        self.total_earned_cents = 0
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Register in Flux as EARNER
        if register_in_flux:
            try:
                register_agent_in_flux(
                    agent_id=self.agent_id,
                    agent_name=self.agent_id,
                    agent_type="Coding Specialist",
                    display_name="Coding Specialist AI",
                    categories=["Coding", "Code Review", "Optimization"],
                    hourly_rate=hourly_rate_cents / 100
                )
                print(f"✅ {self.agent_id} registered in Flux as EARNER")
            except Exception as e:
                print(f"⚠️  Could not register in Flux: {e}")
        self.hourly_rate = hourly_rate
        self.model = model
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Code storage
        self.current_code: Optional[str] = None
        self.task_start_time: Optional[datetime] = None
        
    # ==================== CODING TOOLS ====================
    
    def review_code(
        self,
        code: str,
        language: str = "python",
        review_type: str = "comprehensive"
    ) -> str:
        """
        Review code for quality, best practices, and issues.
        
        Args:
            code: Code to review
            language: Programming language
            review_type: Type of review (comprehensive, security, performance, style)
            
        Returns:
            JSON string with review results
        """
        try:
            # Basic analysis
            lines = code.split('\n')
            
            review = {
                "status": "review_ready",
                "language": language,
                "review_type": review_type,
                "code_stats": {
                    "total_lines": len(lines),
                    "non_empty_lines": len([l for l in lines if l.strip()]),
                    "comment_lines": len([l for l in lines if l.strip().startswith('#')])
                },
                "review_areas": {
                    "code_quality": "Check naming, structure, readability",
                    "best_practices": "Verify language-specific best practices",
                    "potential_bugs": "Identify potential issues",
                    "security": "Check for security vulnerabilities",
                    "performance": "Analyze efficiency and optimization"
                },
                "message": "Dedalus will provide detailed code review"
            }
            
            return json.dumps(review, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def debug_code(
        self,
        code: str,
        error_message: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        Debug code and identify issues.
        
        Args:
            code: Code with potential bugs
            error_message: Optional error message
            language: Programming language
            
        Returns:
            JSON string with debugging results
        """
        try:
            debug_info = {
                "status": "ready_to_debug",
                "language": language,
                "error_provided": error_message is not None,
                "error_message": error_message,
                "debugging_steps": [
                    "Analyze code structure",
                    "Identify error location",
                    "Determine root cause",
                    "Suggest fix",
                    "Provide corrected code"
                ],
                "message": "Dedalus will debug and fix the code"
            }
            
            return json.dumps(debug_info, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def optimize_code(
        self,
        code: str,
        optimization_goal: str = "performance",
        language: str = "python"
    ) -> str:
        """
        Optimize code for performance or readability.
        
        Args:
            code: Code to optimize
            optimization_goal: Goal (performance, readability, memory)
            language: Programming language
            
        Returns:
            JSON string with optimization suggestions
        """
        try:
            return json.dumps({
                "status": "ready_to_optimize",
                "language": language,
                "optimization_goal": optimization_goal,
                "optimization_areas": {
                    "performance": "Algorithm efficiency, loop optimization",
                    "readability": "Code clarity, naming, structure",
                    "memory": "Memory usage, data structures"
                },
                "message": "Dedalus will optimize the code"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def suggest_improvements(
        self,
        code: str,
        focus_area: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        Suggest code improvements and refactoring.
        
        Args:
            code: Code to improve
            focus_area: Specific area to focus on
            language: Programming language
            
        Returns:
            JSON string with improvement suggestions
        """
        try:
            return json.dumps({
                "status": "ready_to_suggest",
                "language": language,
                "focus_area": focus_area,
                "improvement_categories": [
                    "Code organization",
                    "Error handling",
                    "Documentation",
                    "Type hints",
                    "Testing",
                    "Security"
                ],
                "message": "Dedalus will suggest improvements"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def generate_tests(
        self,
        code: str,
        test_framework: str = "pytest",
        language: str = "python"
    ) -> str:
        """
        Generate unit tests for code.
        
        Args:
            code: Code to test
            test_framework: Testing framework
            language: Programming language
            
        Returns:
            JSON string with test code
        """
        try:
            return json.dumps({
                "status": "ready_to_test",
                "language": language,
                "test_framework": test_framework,
                "test_types": [
                    "Unit tests",
                    "Edge cases",
                    "Error handling",
                    "Integration tests"
                ],
                "message": "Dedalus will generate comprehensive tests"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def calculate_cost(self, estimated_hours: float) -> int:
        """Calculate coding work cost."""
        return int(estimated_hours * self.hourly_rate * 100)
    
    # ==================== AGENT EXECUTION ====================
    
    async def execute_task(
        self,
        task_description: str,
        client_id: str,
        code: Optional[str] = None,
        auto_charge: bool = True
    ) -> Dict[str, Any]:
        """Execute a coding task using Dedalus."""
        task_start_time = datetime.now()
        
        print(f"\n💻 Coding Specialist Agent Executing Task")
        print(f"   Task: {task_description}")
        print(f"   Client: {client_id}")
        
        prompt = f"""
You are a professional coding specialist agent (ID: {self.agent_id}).

CLIENT: {client_id}
TASK: {task_description}
YOUR RATE: ${self.hourly_rate_cents/100:.2f}/hour

{"CODE PROVIDED: Yes" if code else "CODE PROVIDED: No"}

AVAILABLE TOOLS:
1. review_code(code, language, review_type) - Review code quality
2. debug_code(code, error_message, language) - Debug and fix issues
3. optimize_code(code, optimization_goal, language) - Optimize code
4. suggest_improvements(code, focus_area, language) - Suggest improvements
5. generate_tests(code, test_framework, language) - Generate tests

INSTRUCTIONS:
1. Understand the coding requirements
2. Use appropriate coding tools to complete the task
3. Provide high-quality code analysis/solutions
4. Return detailed results with code examples

Deliver excellent coding work now.
"""
        
        tools = [
            self.review_code,
            self.debug_code,
            self.optimize_code,
            self.suggest_improvements,
            self.generate_tests
        ]
        
        try:
            result = await self.runner.run(
                input=prompt,
                model=self.model,
                tools=tools
            )
            
            # Calculate earnings (assume 1 hour minimum)
            time_spent_hours = max(1.0, (datetime.now() - task_start_time).total_seconds() / 3600)
            earnings_cents = int(time_spent_hours * self.hourly_rate_cents)
            self.total_earned_cents += earnings_cents
            
            # Record in Flux dashboard
            if auto_charge:
                try:
                    record_agent_earning(
                        agent_id=self.agent_id,
                        client_id=client_id,
                        amount_cents=earnings_cents,
                        service_description=f"Coding task: {task_description[:100]}"
                    )
                    print(f"✅ Recorded ${earnings_cents/100:.2f} earning in Flux dashboard")
                except Exception as e:
                    print(f"⚠️  Could not record earning in Flux: {e}")
            
            print(f"\n✅ Coding Task Complete!")
            print(f"   Time: {time_spent_hours:.2f} hours")
            print(f"   Earnings: ${earnings_cents/100:.2f}")
            
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "task": task_description,
                "result": result.final_output,
                "time_spent_hours": round(time_spent_hours, 2),
                "earnings": f"${earnings_cents/100:.2f}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status from Flux dashboard."""
        stats = get_agent_dashboard_stats(self.agent_id)
        
        return {
            "agent_id": self.agent_id,
            "agent_type": "CodingSpecialist",
            "hourly_rate": f"${self.hourly_rate_cents/100:.2f}/hour",
            "model": self.model,
            "total_earned": f"${self.total_earned_cents/100:.2f}",
            "flux_stats": stats,
            "status": "active"
        }
