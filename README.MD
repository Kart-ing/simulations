# AgentPay Simulation

**AI Agent Marketplace powered by Dedalus and AgentPay SDK**

This repository contains Dedalus-powered AI agents that can hire each other, provide services, and transact using the AgentPay payment infrastructure.

---

## 🎯 What's Inside

- **🛠️ Tools**: Reusable tool functions for Dedalus agents (payments, data analysis, content, research)
- **🤖 Specialized Agents**: Service provider agents (Data Analyst, Content Writer, Researcher, Code Reviewer, Image Generator)
- **🎭 Orchestrator**: Coordinator agent that can hire and manage specialized agents
- **🏪 Marketplace**: Service catalog, pricing, and agent discovery
- **🎬 Scenarios**: End-to-end workflows (marketing campaigns, product launches, data pipelines)
- **📊 Visualization**: Earnings dashboards and transaction analytics

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Install AgentPay SDK
cd ../AgentPay-SDK
pip install -e .
```

### Installation

```bash
# Clone this repo
git clone https://github.com/YourOrg/AgentPay-Simulation.git
cd AgentPay-Simulation

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env
```

### Run Your First Simulation

```bash
# Simple agent interaction
python scenarios/simple_hire.py

# Full marketing campaign
python scenarios/marketing_campaign.py

# Launch earnings dashboard
python visualization/earnings_dashboard.py
```

---

## 📁 Repository Structure

```
Simulation/
├── tools/                    # Tool functions for agents
│   ├── payment_tools.py     # AgentPay SDK wrappers
│   ├── data_tools.py        # Data analysis tools
│   ├── content_tools.py     # Content creation
│   ├── research_tools.py    # Web search & research
│   ├── code_tools.py        # Code review tools
│   └── creative_tools.py    # Image/video generation
│
├── agents/                   # Dedalus agent implementations
│   ├── specialized/         # Service provider agents
│   │   ├── data_analyst.py
│   │   ├── content_writer.py
│   │   ├── researcher.py
│   │   ├── code_reviewer.py
│   │   └── image_generator.py
│   │
│   └── orchestrator/        # Coordinator agent
│       └── orchestrator.py
│
├── marketplace/             # Marketplace infrastructure
│   ├── service_catalog.py  # Service listings & pricing
│   ├── service_registry.py # Agent discovery
│   └── contract_manager.py # Service contracts
│
├── scenarios/               # Demo scenarios
│   ├── simple_hire.py      # Basic agent hiring
│   ├── marketing_campaign.py
│   ├── product_launch.py
│   └── data_pipeline.py
│
├── demo_agents/             # Pre-configured agent teams
│   ├── marketing_team.py
│   └── dev_team.py
│
├── visualization/           # Analytics & dashboards
│   ├── earnings_dashboard.py
│   └── transaction_flow.py
│
└── notebooks/               # Jupyter analysis
    └── marketplace_analysis.ipynb
```

---

## 🤖 Available Agents

### Specialized Agents (Service Providers)

| Agent | Capabilities | Base Price | Tools |
|-------|-------------|------------|-------|
| **Data Analyst** | Data analysis, cleaning, visualization | $25 | `analyze_data()`, `clean_data()` |
| **Content Writer** | Blog posts, ad copy, technical writing | $15-30 | `write_content()`, `generate_copy()` |
| **Researcher** | Market research, fact-checking, web scraping | $20-50 | `search_web()`, `fact_check()` |
| **Code Reviewer** | Code review, bug detection, best practices | $15-60 | `review_code()`, `detect_bugs()` |
| **Image Generator** | Marketing images, graphics, mockups | $10-40 | `generate_image()`, `edit_image()` |

### Orchestrator Agent

The orchestrator can:
- Break down complex goals into subtasks
- Hire appropriate specialized agents
- Manage payments and coordination
- Aggregate results into final deliverables

---

## 💡 Example Usage

### Simple Agent Hire

```python
import asyncio
from agents.specialized.data_analyst import DataAnalystAgent
from agentpay import AgentPaySDK

async def main():
    # Initialize SDK
    sdk = AgentPaySDK()
    
    # Fund client agent
    sdk.register_agent("client-001")
    sdk.fund_agent("client-001", 10000)  # $100
    
    # Create analyst agent
    analyst = DataAnalystAgent(sdk)
    
    # Hire for task
    result = await analyst.execute_task(
        task_description="Analyze Q4 sales data and identify trends",
        client_agent_id="client-001"
    )
    
    print(f"Analysis complete: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Orchestrator Workflow

```python
from agents.orchestrator.orchestrator import OrchestratorAgent

async def main():
    orchestrator = OrchestratorAgent(budget=100000)  # $1,000 budget
    
    result = await orchestrator.execute_goal(
        goal="""
        Launch a marketing campaign for our new AI tool:
        1. Research target audience and competitors
        2. Write compelling ad copy
        3. Generate 5 marketing images
        4. Create landing page content
        """
    )
    
    print(f"Campaign complete!")
    print(f"Total spent: ${result.total_spent / 100}")
    print(f"Agents hired: {result.hired_agents}")

asyncio.run(main())
```

---

## 🔧 Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-...          # For Dedalus agents
AGENTPAY_MODE=local            # 'local' or 'remote'
AGENTPAY_API_KEY=...           # Only if using remote mode
```

### Agent Pricing

Edit `marketplace/service_catalog.py` to customize pricing:

```python
PRICING = {
    "data_analyst": {
        "base": 2500,  # $25
        "tiers": {
            "small_dataset": 2500,
            "medium_dataset": 5000,
            "large_dataset": 10000
        }
    },
    # ... more agents
}
```

---

## 📊 Monitoring & Analytics

### View Earnings

```python
from visualization.earnings_dashboard import show_earnings

# Show earnings for all agents
show_earnings(sdk)
```

### Transaction Flow

```python
from visualization.transaction_flow import visualize_transactions

# Visualize payment network
visualize_transactions(sdk, agent_id="orchestrator-001")
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test specific agent
pytest tests/test_data_analyst.py

# Test marketplace
pytest tests/test_marketplace.py
```

---

## 📚 Documentation

- [Tool Development Guide](docs/TOOLS.md) - Creating new tools
- [Agent Development Guide](docs/AGENTS.md) - Building new agents
- [Marketplace Guide](docs/MARKETPLACE.md) - Service catalog & pricing
- [Scenarios Guide](docs/SCENARIOS.md) - Creating workflows

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🔗 Related Projects

- [AgentPay SDK](https://github.com/Swayam-Bansal/AgentPay-SDK) - Payment infrastructure for AI agents
- [Dedalus Labs](https://docs.dedaluslabs.ai/) - AI agent framework

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/YourOrg/AgentPay-Simulation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YourOrg/AgentPay-Simulation/discussions)
- **Discord**: [Join our community](https://discord.gg/...)

---

**Built with ❤️ using Dedalus and AgentPay**
