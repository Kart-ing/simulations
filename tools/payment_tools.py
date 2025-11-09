"""Payment tools for Dedalus agents.

These tools wrap the AgentPaySDK to provide payment capabilities
that Dedalus agents can use as function tools.
"""

import sys
import os

# Add parent directory to path to import agentpay
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../AgentPay-SDK')))

from agentpay import AgentPaySDK
from typing import Dict, Any, Optional

# Global SDK instance (initialized per agent)
_sdk_instances: Dict[str, AgentPaySDK] = {}


def get_sdk(agent_id: str) -> AgentPaySDK:
    """Get or create SDK instance for an agent."""
    if agent_id not in _sdk_instances:
        _sdk_instances[agent_id] = AgentPaySDK()  # Local mode by default
    return _sdk_instances[agent_id]


def request_payment_from_client(
    agent_id: str,
    client_agent_id: str,
    amount: int,
    service_description: str
) -> Dict[str, Any]:
    """Request payment from a client agent for services rendered.
    
    Use this tool when you've completed work for a client and need to get paid.
    
    Args:
        agent_id: Your agent ID (the service provider)
        client_agent_id: The client's agent ID (who will pay)
        amount: Payment amount in cents (e.g., 2500 = $25.00)
        service_description: Description of service provided
    
    Returns:
        Dictionary with payment status and transaction details
    
    Example:
        result = request_payment_from_client(
            agent_id="data-analyst-001",
            client_agent_id="marketing-agent-001",
            amount=2500,  # $25
            service_description="Analyzed Q4 sales data and generated insights report"
        )
    """
    sdk = get_sdk(agent_id)
    
    try:
        result = sdk.transfer_to_agent(
            from_agent_id=client_agent_id,
            to_agent_id=agent_id,
            amount=amount,
            purpose=service_description
        )
        
        if result['status'] == 'completed':
            return {
                "success": True,
                "message": f"Payment of ${amount / 100:.2f} received from {client_agent_id}",
                "transaction_id": result['transaction_id'],
                "amount_received": amount
            }
        else:
            return {
                "success": False,
                "message": f"Payment failed: {result.get('error', 'Unknown error')}",
                "amount_requested": amount
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Payment error: {str(e)}",
            "amount_requested": amount
        }


def pay_for_service(
    agent_id: str,
    service_provider_id: str,
    amount: int,
    service_description: str
) -> Dict[str, Any]:
    """Pay another agent for their services.
    
    Use this tool when you're hiring another agent and need to pay them.
    
    Args:
        agent_id: Your agent ID (the one paying)
        service_provider_id: The service provider's agent ID
        amount: Payment amount in cents
        service_description: What you're paying for
    
    Returns:
        Dictionary with payment status
    
    Example:
        result = pay_for_service(
            agent_id="orchestrator-001",
            service_provider_id="data-analyst-001",
            amount=2500,
            service_description="Data analysis service for Q4 report"
        )
    """
    sdk = get_sdk(agent_id)
    
    try:
        result = sdk.transfer_to_agent(
            from_agent_id=agent_id,
            to_agent_id=service_provider_id,
            amount=amount,
            purpose=service_description
        )
        
        if result['status'] == 'completed':
            return {
                "success": True,
                "message": f"Paid ${amount / 100:.2f} to {service_provider_id}",
                "transaction_id": result['transaction_id'],
                "amount_paid": amount
            }
        else:
            return {
                "success": False,
                "message": f"Payment failed: {result.get('error', 'Unknown error')}",
                "amount_attempted": amount
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Payment error: {str(e)}",
            "amount_attempted": amount
        }


def check_balance(agent_id: str) -> Dict[str, Any]:
    """Check your current balance and financial summary.
    
    Args:
        agent_id: Your agent ID
    
    Returns:
        Dictionary with balance, earnings, and spending info
    
    Example:
        balance_info = check_balance("data-analyst-001")
        # Returns: {
        #     "current_balance": 5000,  # $50
        #     "total_earned": 10000,    # $100
        #     "total_spent": 5000,      # $50
        #     "net_profit": 5000        # $50
        # }
    """
    sdk = get_sdk(agent_id)
    
    try:
        summary = sdk.get_agent_balance_summary(agent_id)
        return {
            "success": True,
            "current_balance": summary['current_balance'],
            "total_earned": summary['total_earned'],
            "total_spent": summary['total_spent'],
            "net_profit": summary['net_profit'],
            "balance_formatted": f"${summary['current_balance'] / 100:.2f}",
            "earned_formatted": f"${summary['total_earned'] / 100:.2f}",
            "spent_formatted": f"${summary['total_spent'] / 100:.2f}",
            "profit_formatted": f"${summary['net_profit'] / 100:.2f}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking balance: {str(e)}"
        }


def get_earnings_history(agent_id: str, limit: int = 10) -> Dict[str, Any]:
    """Get your recent earnings history.
    
    Args:
        agent_id: Your agent ID
        limit: Maximum number of transactions to return
    
    Returns:
        Dictionary with earnings transactions
    
    Example:
        history = get_earnings_history("data-analyst-001", limit=5)
    """
    sdk = get_sdk(agent_id)
    
    try:
        earnings = sdk.get_agent_earnings(agent_id)
        
        transactions = earnings['transactions'][:limit]
        
        return {
            "success": True,
            "total_earned": earnings['total_earned'],
            "total_earned_formatted": f"${earnings['total_earned'] / 100:.2f}",
            "transaction_count": earnings['transaction_count'],
            "recent_transactions": [
                {
                    "from": txn['from_agent'],
                    "amount": txn['amount'],
                    "amount_formatted": f"${txn['amount'] / 100:.2f}",
                    "purpose": txn['purpose'],
                    "timestamp": txn['timestamp']
                }
                for txn in transactions
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting earnings: {str(e)}"
        }


def get_quote(
    service_type: str,
    complexity: str = "medium",
    urgency: str = "normal"
) -> Dict[str, Any]:
    """Get a price quote for a service.
    
    Args:
        service_type: Type of service (data_analysis, content_writing, research, etc.)
        complexity: Complexity level (simple, medium, complex)
        urgency: Urgency level (normal, urgent, critical)
    
    Returns:
        Dictionary with price quote
    
    Example:
        quote = get_quote("data_analysis", complexity="complex", urgency="urgent")
    """
    # Base prices in cents
    base_prices = {
        "data_analysis": 2500,      # $25
        "content_writing": 1500,    # $15
        "research": 2000,           # $20
        "code_review": 1500,        # $15
        "image_generation": 1000    # $10
    }
    
    # Complexity multipliers
    complexity_multipliers = {
        "simple": 0.8,
        "medium": 1.0,
        "complex": 1.5
    }
    
    # Urgency multipliers
    urgency_multipliers = {
        "normal": 1.0,
        "urgent": 1.3,
        "critical": 1.6
    }
    
    base_price = base_prices.get(service_type, 2000)
    complexity_mult = complexity_multipliers.get(complexity, 1.0)
    urgency_mult = urgency_multipliers.get(urgency, 1.0)
    
    final_price = int(base_price * complexity_mult * urgency_mult)
    
    return {
        "success": True,
        "service_type": service_type,
        "base_price": base_price,
        "complexity": complexity,
        "urgency": urgency,
        "final_price": final_price,
        "price_formatted": f"${final_price / 100:.2f}",
        "breakdown": {
            "base": f"${base_price / 100:.2f}",
            "complexity_adjustment": f"{(complexity_mult - 1) * 100:+.0f}%",
            "urgency_adjustment": f"{(urgency_mult - 1) * 100:+.0f}%"
        }
    }
