"""
Researcher Agent - Specialized in research, fact-finding, and information synthesis.

This agent can:
- Conduct web research
- Synthesize information from multiple sources
- Create research reports
- Fact-check claims
- Request payments for completed work
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

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


class ResearcherAgent:
    """
    A Dedalus-powered research agent with built-in research tools.
    
    Uses GPT-4 for superior reasoning and research capabilities.
    """
    
    def __init__(
        self,
        agent_id: str = "researcher-001",
        hourly_rate_cents: int = 3500,  # $35/hour
        model: str = "openai/gpt-4.1",
        register_in_flux: bool = True
    ):
        """
        Initialize the Researcher agent.
        
        Args:
            agent_id: Unique identifier for this agent
            hourly_rate_cents: Rate per hour in cents
            model: LLM model to use (GPT-4 for best research)
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
                    agent_type="Researcher",
                    display_name="Research Specialist AI",
                    categories=["Research", "Fact-Checking", "Analysis"],
                    hourly_rate=hourly_rate_cents / 100
                )
                print(f"✅ {self.agent_id} registered in Flux as EARNER")
            except Exception as e:
                print(f"⚠️  Could not register in Flux: {e}")
        self.model = model
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Research storage
        self.research_notes: List[str] = []
        self.task_start_time: Optional[datetime] = None
        
    # ==================== RESEARCH TOOLS ====================
    
    def search_web(
        self,
        query: str,
        search_type: str = "general"
    ) -> str:
        """
        Simulate web search (in production, integrate with real search API).
        
        Args:
            query: Search query
            search_type: Type of search (general, academic, news, images)
            
        Returns:
            JSON string with search results
        """
        try:
            return json.dumps({
                "status": "search_ready",
                "query": query,
                "search_type": search_type,
                "message": "In production, this would integrate with Google, Bing, or academic databases",
                "note": "Dedalus can use its knowledge to provide research insights"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def synthesize_information(
        self,
        sources: List[str],
        topic: str
    ) -> str:
        """
        Synthesize information from multiple sources.
        
        Args:
            sources: List of information sources
            topic: Main topic to focus on
            
        Returns:
            JSON string with synthesis
        """
        try:
            return json.dumps({
                "status": "ready_to_synthesize",
                "topic": topic,
                "source_count": len(sources),
                "sources": sources,
                "message": "Dedalus will analyze and synthesize information"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def create_research_report(
        self,
        research_question: str,
        findings: List[str],
        report_format: str = "executive_summary"
    ) -> str:
        """
        Create a structured research report.
        
        Args:
            research_question: The main research question
            findings: List of key findings
            report_format: Format (executive_summary, detailed, presentation)
            
        Returns:
            JSON string with report structure
        """
        try:
            return json.dumps({
                "status": "ready_to_report",
                "research_question": research_question,
                "findings_count": len(findings),
                "format": report_format,
                "structure": {
                    "executive_summary": "Key findings overview",
                    "methodology": "Research approach",
                    "findings": "Detailed findings with evidence",
                    "conclusions": "Conclusions and recommendations"
                },
                "message": "Dedalus will create comprehensive research report"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def fact_check(
        self,
        claim: str,
        context: Optional[str] = None
    ) -> str:
        """
        Fact-check a claim.
        
        Args:
            claim: The claim to verify
            context: Optional context for the claim
            
        Returns:
            JSON string with fact-check results
        """
        try:
            return json.dumps({
                "status": "ready_to_verify",
                "claim": claim,
                "context": context,
                "verification_steps": [
                    "Identify key facts in the claim",
                    "Search for authoritative sources",
                    "Cross-reference multiple sources",
                    "Assess credibility of sources",
                    "Provide verdict with evidence"
                ],
                "message": "Dedalus will verify the claim using its knowledge"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def extract_insights(
        self,
        data: str,
        focus_area: Optional[str] = None
    ) -> str:
        """
        Extract key insights from research data.
        
        Args:
            data: Research data or text
            focus_area: Specific area to focus on
            
        Returns:
            JSON string with insights
        """
        try:
            return json.dumps({
                "status": "ready_to_analyze",
                "data_length": len(data),
                "focus_area": focus_area,
                "message": "Dedalus will extract actionable insights"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def calculate_cost(self, estimated_hours: float) -> int:
        """Calculate research cost."""
        return int(estimated_hours * self.hourly_rate * 100)
    
    # ==================== AGENT EXECUTION ====================
    
    async def execute_task(
        self,
        task_description: str,
        client_id: str,
        auto_charge: bool = True
    ) -> Dict[str, Any]:
        """Execute a research task using Dedalus."""
        task_start_time = datetime.now()
        
        print(f"\n🔍 Researcher Agent Executing Task")
        print(f"   Task: {task_description}")
        print(f"   Client: {client_id}")
        
        prompt = f"""
You are a professional research agent (ID: {self.agent_id}).

CLIENT: {client_id}
TASK: {task_description}
YOUR RATE: ${self.hourly_rate_cents/100:.2f}/hour

AVAILABLE TOOLS:
1. search_web(query, search_type) - Search for information
2. synthesize_information(sources, topic) - Combine multiple sources
3. create_research_report(research_question, findings, format) - Create reports
4. fact_check(claim, context) - Verify claims
5. extract_insights(data, focus_area) - Extract key insights

INSTRUCTIONS:
1. Break down the research question
2. Use appropriate research tools to gather information
3. Analyze and synthesize findings
4. Create a comprehensive report
5. Return detailed research results

Conduct thorough research now.
"""
        
        tools = [
            self.search_web,
            self.synthesize_information,
            self.create_research_report,
            self.fact_check,
            self.extract_insights
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
                        service_description=f"Research task: {task_description[:100]}"
                    )
                    print(f"✅ Recorded ${earnings_cents/100:.2f} earning in Flux dashboard")
                except Exception as e:
                    print(f"⚠️  Could not record earning in Flux: {e}")
            
            print(f"\n✅ Research Complete!")
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
            "agent_type": "Researcher",
            "hourly_rate": f"${self.hourly_rate_cents/100:.2f}/hour",
            "model": self.model,
            "total_earned": f"${self.total_earned_cents/100:.2f}",
            "flux_stats": stats,
            "status": "active"
        }
