"""
Integration modules for connecting agents with external systems.
"""
from .flux_integration import (
    FluxDashboardIntegration,
    get_flux_integration,
    register_agent_in_flux,
    record_agent_earning,
    get_agent_dashboard_stats
)

__all__ = [
    'FluxDashboardIntegration',
    'get_flux_integration',
    'register_agent_in_flux',
    'record_agent_earning',
    'get_agent_dashboard_stats'
]
