"""
MarketingSpecialist Agent - Specialized in marketing strategy, campaigns, and analytics.

This agent can:
- Create marketing strategies
- Design campaign plans
- Analyze marketing data
- Generate marketing content
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


class MarketingSpecialistAgent:
    """
    A Dedalus-powered marketing specialist agent with built-in marketing tools.
    
    Uses GPT-4 for strategic thinking and Claude for creative content.
    """
    
    def __init__(
        self,
        agent_id: str = "marketing-specialist-001",
        hourly_rate_cents: int = 4000,  # $40/hour
        model: str = "openai/gpt-4.1",
        register_in_flux: bool = True
    ):
        """
        Initialize the MarketingSpecialist agent.
        
        Args:
            agent_id: Unique identifier for this agent
            hourly_rate_cents: Rate per hour in cents
            model: LLM model to use
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
                    agent_type="Marketing Specialist",
                    display_name="Marketing Specialist AI",
                    categories=["Marketing", "Strategy", "Campaigns"],
                    hourly_rate=hourly_rate_cents / 100
                )
                print(f"✅ {self.agent_id} registered in Flux as EARNER")
            except Exception as e:
                print(f"⚠️  Could not register in Flux: {e}")
        self.model = model
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Marketing data storage
        self.campaign_data: Dict[str, Any] = {}
        self.task_start_time: Optional[datetime] = None
        
    # ==================== MARKETING TOOLS ====================
    
    def create_marketing_strategy(
        self,
        business_description: str,
        target_audience: str,
        goals: List[str],
        budget: Optional[float] = None
    ) -> str:
        """
        Create a comprehensive marketing strategy.
        
        Args:
            business_description: Description of the business
            target_audience: Target audience description
            goals: List of marketing goals
            budget: Optional budget in dollars
            
        Returns:
            JSON string with marketing strategy
        """
        try:
            strategy = {
                "status": "ready_to_strategize",
                "business": business_description,
                "target_audience": target_audience,
                "goals": goals,
                "budget": budget,
                "strategy_components": {
                    "market_analysis": "Analyze market and competition",
                    "positioning": "Define unique value proposition",
                    "channels": "Select marketing channels",
                    "tactics": "Specific marketing tactics",
                    "timeline": "Implementation timeline",
                    "metrics": "KPIs and success metrics"
                },
                "message": "Dedalus will create comprehensive strategy"
            }
            
            return json.dumps(strategy, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def design_campaign(
        self,
        campaign_goal: str,
        campaign_type: str,
        duration_weeks: int,
        budget: float
    ) -> str:
        """
        Design a marketing campaign.
        
        Args:
            campaign_goal: Main goal of the campaign
            campaign_type: Type (product_launch, brand_awareness, lead_gen)
            duration_weeks: Campaign duration in weeks
            budget: Campaign budget in dollars
            
        Returns:
            JSON string with campaign plan
        """
        try:
            campaign = {
                "status": "ready_to_design",
                "goal": campaign_goal,
                "type": campaign_type,
                "duration_weeks": duration_weeks,
                "budget": budget,
                "campaign_elements": {
                    "creative_concept": "Central creative idea",
                    "messaging": "Key messages and taglines",
                    "channels": "Marketing channels to use",
                    "content_calendar": "Content schedule",
                    "budget_allocation": "Budget by channel",
                    "success_metrics": "How to measure success"
                },
                "message": "Dedalus will design detailed campaign"
            }
            
            return json.dumps(campaign, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def analyze_marketing_data(
        self,
        metrics: Dict[str, float],
        campaign_name: str,
        analysis_type: str = "performance"
    ) -> str:
        """
        Analyze marketing metrics and performance.
        
        Args:
            metrics: Dictionary of marketing metrics
            campaign_name: Name of the campaign
            analysis_type: Type of analysis (performance, roi, attribution)
            
        Returns:
            JSON string with analysis results
        """
        try:
            analysis = {
                "status": "ready_to_analyze",
                "campaign": campaign_name,
                "analysis_type": analysis_type,
                "metrics_provided": list(metrics.keys()),
                "analysis_areas": {
                    "performance": "Overall campaign performance",
                    "roi": "Return on investment calculation",
                    "trends": "Performance trends over time",
                    "recommendations": "Optimization recommendations"
                },
                "message": "Dedalus will analyze marketing data"
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def generate_marketing_content(
        self,
        content_type: str,
        platform: str,
        topic: str,
        tone: str = "professional"
    ) -> str:
        """
        Generate marketing content for various platforms.
        
        Args:
            content_type: Type of content (post, email, ad, video_script)
            platform: Platform (social_media, email, website, ads)
            topic: Content topic
            tone: Content tone
            
        Returns:
            JSON string with content
        """
        try:
            return json.dumps({
                "status": "ready_to_create",
                "content_type": content_type,
                "platform": platform,
                "topic": topic,
                "tone": tone,
                "content_specs": {
                    "social_media": "Short, engaging, with hashtags",
                    "email": "Subject line, body, CTA",
                    "website": "SEO-optimized, informative",
                    "ads": "Attention-grabbing, conversion-focused"
                },
                "message": "Dedalus will generate platform-optimized content"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def competitor_analysis(
        self,
        competitors: List[str],
        analysis_focus: str = "comprehensive"
    ) -> str:
        """
        Analyze competitors' marketing strategies.
        
        Args:
            competitors: List of competitor names
            analysis_focus: Focus area (comprehensive, social_media, content, ads)
            
        Returns:
            JSON string with competitor analysis
        """
        try:
            return json.dumps({
                "status": "ready_to_analyze",
                "competitors": competitors,
                "analysis_focus": analysis_focus,
                "analysis_areas": [
                    "Marketing channels used",
                    "Content strategy",
                    "Messaging and positioning",
                    "Strengths and weaknesses",
                    "Opportunities for differentiation"
                ],
                "message": "Dedalus will analyze competitors"
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def calculate_roi(
        self,
        campaign_cost: float,
        revenue_generated: float
    ) -> str:
        """
        Calculate marketing ROI.
        
        Args:
            campaign_cost: Total campaign cost
            revenue_generated: Revenue attributed to campaign
            
        Returns:
            JSON string with ROI calculation
        """
        try:
            roi = ((revenue_generated - campaign_cost) / campaign_cost) * 100
            
            return json.dumps({
                "status": "success",
                "campaign_cost": campaign_cost,
                "revenue_generated": revenue_generated,
                "roi_percentage": round(roi, 2),
                "roi_interpretation": "positive" if roi > 0 else "negative",
                "profit": revenue_generated - campaign_cost
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def calculate_cost(self, estimated_hours: float) -> int:
        """Calculate marketing work cost."""
        return int(estimated_hours * self.hourly_rate * 100)
    
    # ==================== AGENT EXECUTION ====================
    
    async def execute_task(
        self,
        task_description: str,
        client_id: str,
        auto_charge: bool = True
    ) -> Dict[str, Any]:
        """Execute a marketing task using Dedalus."""
        task_start_time = datetime.now()
        
        print(f"\n📢 Marketing Specialist Agent Executing Task")
        print(f"   Task: {task_description}")
        print(f"   Client: {client_id}")
        
        prompt = f"""
You are a professional marketing specialist agent (ID: {self.agent_id}).

CLIENT: {client_id}
TASK: {task_description}
YOUR RATE: ${self.hourly_rate}/hour

AVAILABLE TOOLS:
1. create_marketing_strategy(business_description, target_audience, goals, budget) - Create strategy
2. design_campaign(campaign_goal, campaign_type, duration_weeks, budget) - Design campaigns
3. analyze_marketing_data(metrics, campaign_name, analysis_type) - Analyze performance
4. generate_marketing_content(content_type, platform, topic, tone) - Create content
5. competitor_analysis(competitors, analysis_focus) - Analyze competitors
6. calculate_roi(campaign_cost, revenue_generated) - Calculate ROI
7. calculate_cost(estimated_hours) - Calculate cost
8. request_payment_from_client(agent_id, client_id, amount, description) - Request payment

INSTRUCTIONS:
1. Understand the marketing requirements
2. Use appropriate marketing tools to complete the task
3. Provide strategic, data-driven recommendations
4. Estimate time spent (in hours)
5. {"Calculate cost and request payment from client" if auto_charge else "Provide cost estimate"}
6. Return comprehensive marketing deliverables

Create exceptional marketing work now.
"""
        
        tools = [
            self.analyze_market,
            self.create_campaign,
            self.generate_marketing_content,
            self.measure_metrics
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
                        service_description=f"Marketing task: {task_description[:100]}"
                    )
                    print(f"✅ Recorded ${earnings_cents/100:.2f} earning in Flux dashboard")
                except Exception as e:
                    print(f"⚠️  Could not record earning in Flux: {e}")
            
            print(f"\n✅ Marketing Task Complete!")
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
            "agent_type": "MarketingSpecialist",
            "hourly_rate": f"${self.hourly_rate_cents/100:.2f}/hour",
            "model": self.model,
            "total_earned": f"${self.total_earned_cents/100:.2f}",
            "flux_stats": stats,
            "status": "active"
        }
