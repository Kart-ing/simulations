"""
ContentWriter Agent - Specialized in content creation, copywriting, and creative writing.

This agent can:
- Write blog posts, articles, and copy
- Create marketing content
- Edit and improve existing content
- Generate creative ideas
- Automatically registers as EARNER in Flux dashboard
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


class ContentWriterAgent:
    """
    A Dedalus-powered content writer agent with built-in writing tools.
    
    Uses Claude Sonnet 3.5 for superior creative writing capabilities.
    Automatically registers as EARNER in Flux dashboard.
    """
    
    def __init__(
        self,
        agent_id: str = "content-writer-001",
        price_per_word_cents: int = 10,  # $0.10 per word
        model: str = "anthropic/claude-sonnet-4-20250514",
        register_in_flux: bool = True
    ):
        """
        Initialize the Content Writer agent.
        
        Args:
            agent_id: Unique identifier
            price_per_word_cents: Price per word in cents
            model: LLM model to use
            register_in_flux: Whether to register in Flux dashboard
        """
        self.agent_id = agent_id
        self.price_per_word_cents = price_per_word_cents
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
                    agent_type="Content Writer",
                    display_name="Content Writer AI",
                    categories=["Writing", "Content Creation", "Marketing"],
                    hourly_rate=None,  # We charge per word
                    pricing_model=f"${self.price_per_word_cents/100:.2f}/word"
                )
                print(f"✅ {self.agent_id} registered in Flux as EARNER")
            except Exception as e:
                print(f"⚠️  Could not register in Flux: {e}")
    
    # ==================== CONTENT WRITING TOOLS ====================
    
    def write_blog_post(
        self,
        topic: str,
        tone: str = "professional",
        word_count: int = 800,
        keywords: Optional[List[str]] = None
    ) -> str:
        """
        Write a complete blog post.
        
        Args:
            topic: The topic to write about
            tone: Writing tone (professional, casual, friendly, authoritative)
            word_count: Target word count
            keywords: Optional SEO keywords to include
            
        Returns:
            JSON string with the blog post
        """
        try:
            content_structure = {
                "status": "ready_to_write",
                "topic": topic,
                "tone": tone,
                "target_words": word_count,
                "keywords": keywords or [],
                "structure": {
                    "introduction": "Hook the reader, introduce topic",
                    "main_sections": "3-4 main points with examples",
                    "conclusion": "Summary and call-to-action"
                },
                "message": "Dedalus will generate the actual content"
            }
            
            return json.dumps(content_structure, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def write_marketing_copy(
        self,
        product_name: str,
        product_description: str,
        copy_type: str = "landing_page",
        target_audience: str = "general"
    ) -> str:
        """
        Write marketing copy for a product or service.
        
        Args:
            product_name: Name of the product/service
            product_description: Description of what it does
            copy_type: Type of copy (landing_page, email, ad, social_media)
            target_audience: Target audience description
            
        Returns:
            JSON string with marketing copy
        """
        try:
            copy_structure = {
                "status": "ready_to_write",
                "product": product_name,
                "description": product_description,
                "copy_type": copy_type,
                "audience": target_audience,
                "elements": {
                    "headline": "Attention-grabbing headline",
                    "subheadline": "Supporting subheadline",
                    "body": "Benefits and features",
                    "cta": "Clear call-to-action"
                },
                "message": "Dedalus will generate persuasive copy"
            }
            
            return json.dumps(copy_structure, indent=2)
            
        except Exception as e:
            return json.dumps({"status": "error", "error": str(e)})
    
    def count_words(self, text: str) -> str:
        """Count words in text and return as JSON."""
        word_count = len(text.split())
        return json.dumps({"word_count": word_count})
    
    # ==================== AGENT EXECUTION ====================
    
    async def execute_task(
        self,
        task_description: str,
        client_id: str,
        auto_charge: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a content writing task using Dedalus.
        
        Args:
            task_description: Description of the writing task
            client_id: ID of the client requesting the task
            auto_charge: Whether to automatically record earnings in Flux
            
        Returns:
            Dictionary with task results and payment status
        """
        task_start_time = datetime.now()
        
        print(f"\n📝 Content Writer Agent Executing Task")
        print(f"   Task: {task_description}")
        print(f"   Client: {client_id}")
        
        prompt = f"""
You are a professional content writer agent (ID: {self.agent_id}).

CLIENT: {client_id}
TASK: {task_description}
YOUR RATE: ${self.price_per_word_cents/100:.2f} per word

AVAILABLE TOOLS:
1. write_blog_post(topic, tone, word_count, keywords) - Write blog posts
2. write_marketing_copy(product_name, product_description, copy_type, target_audience) - Write marketing copy
3. count_words(text) - Count words in text

INSTRUCTIONS:
1. Understand the writing requirements
2. Use the appropriate writing tools to complete the task
3. Produce high-quality, engaging content
4. Return the completed content

Write exceptional content now.
"""
        
        tools = [
            self.write_blog_post,
            self.write_marketing_copy,
            self.count_words
        ]
        
        try:
            result = await self.runner.run(
                input=prompt,
                model=self.model,
                tools=tools
            )
            
            # Calculate earnings based on word count
            word_count = len(result.final_output.split())
            earnings_cents = word_count * self.price_per_word_cents
            self.total_earned_cents += earnings_cents
            
            # Record in Flux dashboard
            if auto_charge:
                try:
                    record_agent_earning(
                        agent_id=self.agent_id,
                        client_id=client_id,
                        amount_cents=earnings_cents,
                        service_description=f"Created {word_count}-word content"
                    )
                    print(f"✅ Recorded ${earnings_cents/100:.2f} earning in Flux dashboard")
                except Exception as e:
                    print(f"⚠️  Could not record earning in Flux: {e}")
            
            print(f"\n✅ Content Writing Complete!")
            print(f"   Word Count: {word_count}")
            print(f"   Earnings: ${earnings_cents/100:.2f}")
            print(f"   Total Earned: ${self.total_earned_cents/100:.2f}")
            
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "task": task_description,
                "content": result.final_output,
                "word_count": word_count,
                "earnings": f"${earnings_cents/100:.2f}",
                "total_earned": f"${self.total_earned_cents/100:.2f}",
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
            "agent_type": "Content Writer",
            "price_per_word": f"${self.price_per_word_cents/100:.2f}",
            "model": self.model,
            "total_earned": f"${self.total_earned_cents/100:.2f}",
            "flux_stats": stats,
            "status": "active"
        }
