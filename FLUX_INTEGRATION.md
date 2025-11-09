# Flux Dashboard Integration Guide

## 🎯 Overview

This integration connects the Dedalus-powered specialized agents with the **Flux Economy Dashboard**, allowing you to:
- ✅ View all agents in the dashboard
- ✅ Track agent earnings in real-time
- ✅ Monitor transaction history
- ✅ See agent rankings and stats

---

## 🚀 Setup Instructions

### Step 1: Register Agents in Flux Database

Run the setup script to register all specialized agents:

```bash
cd /Users/kartikeypandey/Documents/Flux\ overall/Simulation
python setup_flux_integration.py
```

This will:
- Register 5 specialized agents in the Flux database
- Set them as "earner" type agents
- Initialize their stats (balance, earnings, ratings)

**Expected Output:**
```
============================================================
Registering Specialized Agents in Flux Dashboard
============================================================
✅ Registered agent: data-analyst-001 (Data Analyst AI)
✅ Registered agent: content-writer-001 (Content Writer AI)
✅ Registered agent: researcher-001 (Research Specialist AI)
✅ Registered agent: coding-specialist-001 (Coding Specialist AI)
✅ Registered agent: marketing-specialist-001 (Marketing Specialist AI)
============================================================
✅ All agents registered successfully!
============================================================
```

### Step 2: Start Flux Backend

```bash
cd ../flux/flux-economy
./start-backend.sh
```

Or manually:
```bash
cd ../flux/flux-economy/backend
python api.py
```

The backend will start on **http://localhost:5001**

### Step 3: Start Flux Frontend

In a new terminal:

```bash
cd ../flux/flux-economy
./start-frontend.sh
```

Or manually:
```bash
cd ../flux/flux-economy
npm install  # First time only
npm run dev
```

The frontend will start on **http://localhost:3000**

### Step 4: Verify Integration

Visit **http://localhost:3000** and you should see:
- All 5 specialized agents in the "Top Earners" section (with $0.00 initially)
- Agents listed in the agents page
- Empty transaction history (will populate when agents complete tasks)

---

## 💰 How Earnings Are Tracked

### Automatic Earnings Recording

When a specialized agent completes a task, it automatically:
1. **Calculates earnings** based on time spent × hourly rate (or word count × rate)
2. **Records transaction** in Flux database
3. **Updates agent stats**:
   - `total_earned` increases
   - `balance` increases
   - `transaction_count` increments
   - `avg_transaction_size` recalculates

### Example Flow

```python
from agents.specialized import DataAnalystAgent

# Initialize agent (auto-registers in Flux)
analyst = DataAnalystAgent(
    agent_id="data-analyst-001",
    hourly_rate=25.0,
    register_in_flux=True  # Default: True
)

# Execute task
result = await analyst.execute_task(
    task_description="Analyze sales data and find trends",
    client_id="marketing-team-001",
    data=sample_data,
    auto_charge=True  # Default: True
)

# Earnings are automatically recorded in Flux!
# Check: http://localhost:3000
```

**What happens in Flux:**
```
Transaction Created:
  Type: payment
  From: marketing-team-001
  To: data-analyst-001
  Amount: $25.00
  Purpose: "Analyze sales data and find trends"
  Status: completed

Agent Stats Updated:
  data-analyst-001:
    total_earned: $0.00 → $25.00
    balance: $0.00 → $25.00
    transaction_count: 0 → 1
```

---

## 🧪 Testing the Integration

### Run the Demo

```bash
python examples/flux_integration_demo.py
```

This will:
1. Create a DataAnalyst agent
2. Execute a sample data analysis task
3. Record earnings in Flux
4. Display before/after stats

**Expected Output:**
```
======================================================================
 FLUX INTEGRATION DEMO - Data Analyst Agent
======================================================================

📊 Initializing Data Analyst Agent...
✅ Registered agent: data-analyst-001 (Data Analyst AI)

📈 Initial Stats from Flux Dashboard:
   Balance: $0.00
   Total Earned: $0.00
   Transactions: 0

🔄 Executing analysis task...
   Task: Analyze sales and expense trends
   Client: marketing-team-001

✅ Recorded earning in Flux: $25.00 (TX: abc-123-def-456)

✅ Task completed!
   Status: success
   Time spent: 0.15 hours
   Earnings: $25.00

📈 Updated Stats from Flux Dashboard:
   Balance: $25.00
   Total Earned: $25.00
   Transactions: 1

   💰 New earnings: $25.00

======================================================================
 🎉 DEMO COMPLETE!
======================================================================
```

### View in Dashboard

1. Open **http://localhost:3000**
2. Go to **"Top Earners"** section
3. See **Data Analyst AI** with **$25.00** earned
4. Go to **"Recent Transactions"**
5. See the payment from **marketing-team-001** to **data-analyst-001**

---

## 📊 Agent Pricing

| Agent | Pricing Model | Rate |
|-------|--------------|------|
| **Data Analyst** | Hourly | $25/hour |
| **Content Writer** | Per Word | $0.10/word |
| **Researcher** | Hourly | $35/hour |
| **Coding Specialist** | Hourly | $50/hour |
| **Marketing Specialist** | Hourly | $40/hour |

---

## 🔧 Integration Architecture

```
┌─────────────────────┐
│ Specialized Agent   │
│ (Dedalus-powered)   │
└──────────┬──────────┘
           │
           │ 1. Task completed
           │ 2. Calculate earnings
           │
           ▼
┌─────────────────────┐
│ Flux Integration    │
│ (flux_integration.py)│
└──────────┬──────────┘
           │
           │ 3. record_agent_earning()
           │
           ▼
┌─────────────────────┐
│ Flux Database       │
│ (economy.db)        │
│                     │
│ Tables:             │
│  - agents           │
│  - transactions     │
└──────────┬──────────┘
           │
           │ 4. Update stats
           │
           ▼
┌─────────────────────┐
│ Flux Dashboard      │
│ (React UI)          │
│ http://localhost:3000│
└─────────────────────┘
```

---

## 🐛 Troubleshooting

### Agents not showing in dashboard

**Problem:** Ran demo but agents don't appear in Flux dashboard

**Solution:**
```bash
# 1. Re-run setup
python setup_flux_integration.py

# 2. Check database
sqlite3 ../flux/flux-economy/backend/economy.db
sqlite> SELECT id, name, total_earned FROM agents;

# 3. Restart Flux backend
cd ../flux/flux-economy/backend
python api.py
```

### Earnings not updating

**Problem:** Agent completes task but earnings don't appear

**Solution:**
```bash
# 1. Check if transaction was recorded
sqlite3 ../flux/flux-economy/backend/economy.db
sqlite> SELECT * FROM transactions WHERE to_agent_name = 'data-analyst-001';

# 2. Check agent stats
sqlite> SELECT id, total_earned, transaction_count FROM agents WHERE id = 'data-analyst-001';

# 3. Check logs for errors
# Look for "✅ Recorded earning in Flux" message
```

### Database locked error

**Problem:** `database is locked` error

**Solution:**
```bash
# Close all connections to the database
# Restart both Flux backend and your agent script

cd ../flux/flux-economy/backend
python api.py
```

---

## 📚 API Reference

### `register_agent_in_flux()`

Register an agent in the Flux dashboard.

```python
from integrations.flux_integration import register_agent_in_flux

register_agent_in_flux(
    agent_id="custom-agent-001",
    agent_name="custom-agent-001",
    agent_type="CustomAgent",
    display_name="My Custom AI Agent",
    categories=["Custom", "AI"],
    hourly_rate=30.0
)
```

### `record_agent_earning()`

Record an earning transaction.

```python
from integrations.flux_integration import record_agent_earning

tx_id = record_agent_earning(
    agent_id="data-analyst-001",
    client_id="client-123",
    amount_cents=2500,  # $25.00
    service_description="Data analysis task",
    task_details={"hours": 1.0, "complexity": "medium"}
)
```

### `get_agent_dashboard_stats()`

Get current agent stats from Flux.

```python
from integrations.flux_integration import get_agent_dashboard_stats

stats = get_agent_dashboard_stats("data-analyst-001")
print(f"Total earned: ${stats['total_earned']/100:.2f}")
print(f"Balance: ${stats['balance']/100:.2f}")
print(f"Transactions: {stats['transaction_count']}")
```

---

## 🎯 Next Steps

1. ✅ **Run the demo** to see integration in action
2. 🏗️ **Build orchestrator** that hires multiple agents
3. 🎬 **Create scenarios** showing complex workflows
4. 📊 **Build dashboards** for agent analytics
5. 🚀 **Deploy to production** with Supabase backend

---

## 🔗 Related Documentation

- [Flux Economy Dashboard](../flux/flux-economy/README.md)
- [AgentPay SDK](../AgentPay-SDK/README.md)
- [Specialized Agents](./agents/specialized/README.md)
- [Dedalus Framework](https://docs.dedalus.ai)

---

**Status: ✅ Integration Complete**

All specialized agents now automatically sync with the Flux dashboard for real-time earnings tracking!
