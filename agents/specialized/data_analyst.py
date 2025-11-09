"""
DataAnalyst Agent - Specialized in data analysis, cleaning, and visualization.

This agent can:
- Analyze datasets and extract insights
- Clean and transform data
- Create visualizations
- Find patterns and trends
- Request payments for completed work
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime

from dedalus_labs import AsyncDedalus, DedalusRunner

# Import payment tools and Flux integration
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from tools.payment_tools import (
    request_payment_from_client,
    pay_for_service,
    check_balance,
    get_earnings_history,
    get_quote
)
from integrations.flux_integration import (
    register_agent_in_flux,
    record_agent_earning,
    get_agent_dashboard_stats
)


class DataAnalystAgent:
    """
    A Dedalus-powered data analyst agent with built-in data analysis tools.
    
    This agent can perform data analysis tasks and automatically handle payments.
    """
    
    def __init__(
        self,
        agent_id: str = "data-analyst-001",
        hourly_rate_cents: int = 2500,  # $25/hour
        model: str = "openai/gpt-4.1",
        register_in_flux: bool = True
    ):
        """
        Initialize the DataAnalyst agent.
        
        Args:
            agent_id: Unique identifier for this agent
            hourly_rate_cents: Rate per hour in cents
            model: LLM model to use (default: gpt-4.1)
            register_in_flux: Whether to register in Flux dashboard (default: True)
        """
        self.agent_id = agent_id
        self.hourly_rate_cents = hourly_rate_cents
        self.model = model
        self.total_earned_cents = 0
        
        # Initialize Dedalus
        self.client = AsyncDedalus()
        self.runner = DedalusRunner(self.client)
        
        # Data storage for current task
        self.current_data: Optional[pd.DataFrame] = None
        self.task_start_time: Optional[datetime] = None
        
        # Register in Flux dashboard
        if register_in_flux:
            try:
                register_agent_in_flux(
                    agent_id=self.agent_id,
                    agent_name=self.agent_id,
                    agent_type="DataAnalyst",
                    display_name="Data Analyst AI",
                    categories=["Data Analysis", "Statistics", "Visualization"],
                    hourly_rate=self.hourly_rate
                )
            except Exception as e:
                print(f"⚠️  Could not register in Flux dashboard: {e}")
        
    # ==================== DATA ANALYSIS TOOLS ====================
    
    def analyze_data(
        self,
        data_dict: Dict[str, List],
        analysis_type: str = "descriptive"
    ) -> str:
        """
        Analyze a dataset and return statistical insights.
        
        Args:
            data_dict: Dictionary representing the dataset (column -> values)
            analysis_type: Type of analysis ('descriptive', 'correlation', 'summary')
            
        Returns:
            JSON string with analysis results
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data_dict)
            self.current_data = df
            
            results = {
                "status": "success",
                "rows": len(df),
                "columns": list(df.columns),
                "analysis_type": analysis_type
            }
            
            if analysis_type == "descriptive":
                # Descriptive statistics
                desc = df.describe().to_dict()
                results["statistics"] = desc
                results["data_types"] = df.dtypes.astype(str).to_dict()
                results["missing_values"] = df.isnull().sum().to_dict()
                
            elif analysis_type == "correlation":
                # Correlation analysis (numeric columns only)
                numeric_df = df.select_dtypes(include=[np.number])
                if not numeric_df.empty:
                    corr = numeric_df.corr().to_dict()
                    results["correlation_matrix"] = corr
                else:
                    results["error"] = "No numeric columns for correlation"
                    
            elif analysis_type == "summary":
                # Quick summary
                results["summary"] = {
                    "shape": df.shape,
                    "memory_usage": df.memory_usage(deep=True).sum(),
                    "duplicate_rows": df.duplicated().sum(),
                    "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
                    "categorical_columns": len(df.select_dtypes(include=['object']).columns)
                }
            
            return json.dumps(results, indent=2, default=str)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def clean_data(
        self,
        data_dict: Dict[str, List],
        operations: List[str]
    ) -> str:
        """
        Clean and transform data.
        
        Args:
            data_dict: Dictionary representing the dataset
            operations: List of operations to perform:
                - 'remove_duplicates': Remove duplicate rows
                - 'fill_missing': Fill missing values with mean/mode
                - 'remove_outliers': Remove statistical outliers
                - 'normalize': Normalize numeric columns
                
        Returns:
            JSON string with cleaned data and report
        """
        try:
            df = pd.DataFrame(data_dict)
            original_rows = len(df)
            changes = []
            
            if 'remove_duplicates' in operations:
                before = len(df)
                df = df.drop_duplicates()
                after = len(df)
                changes.append(f"Removed {before - after} duplicate rows")
            
            if 'fill_missing' in operations:
                for col in df.columns:
                    missing_count = df[col].isnull().sum()
                    if missing_count > 0:
                        if df[col].dtype in [np.float64, np.int64]:
                            df[col].fillna(df[col].mean(), inplace=True)
                            changes.append(f"Filled {missing_count} missing values in '{col}' with mean")
                        else:
                            df[col].fillna(df[col].mode()[0], inplace=True)
                            changes.append(f"Filled {missing_count} missing values in '{col}' with mode")
            
            if 'remove_outliers' in operations:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    before = len(df)
                    df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
                    after = len(df)
                    if before != after:
                        changes.append(f"Removed {before - after} outliers from '{col}'")
            
            if 'normalize' in operations:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
                changes.append(f"Normalized {len(numeric_cols)} numeric columns")
            
            self.current_data = df
            
            return json.dumps({
                "status": "success",
                "original_rows": original_rows,
                "final_rows": len(df),
                "changes": changes,
                "cleaned_data": df.to_dict(orient='list')
            }, indent=2, default=str)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def visualize_data(
        self,
        data_dict: Dict[str, List],
        chart_type: str,
        x_column: str,
        y_column: Optional[str] = None
    ) -> str:
        """
        Create a visualization of the data.
        
        Args:
            data_dict: Dictionary representing the dataset
            chart_type: Type of chart ('bar', 'line', 'scatter', 'histogram')
            x_column: Column for x-axis
            y_column: Column for y-axis (if applicable)
            
        Returns:
            JSON string with base64 encoded image
        """
        try:
            df = pd.DataFrame(data_dict)
            
            plt.figure(figsize=(10, 6))
            
            if chart_type == 'bar':
                if y_column:
                    df.plot(x=x_column, y=y_column, kind='bar')
                else:
                    df[x_column].value_counts().plot(kind='bar')
                    
            elif chart_type == 'line':
                if y_column:
                    plt.plot(df[x_column], df[y_column])
                else:
                    plt.plot(df[x_column])
                    
            elif chart_type == 'scatter':
                if y_column:
                    plt.scatter(df[x_column], df[y_column])
                else:
                    return json.dumps({"status": "error", "error": "Scatter plot requires y_column"})
                    
            elif chart_type == 'histogram':
                df[x_column].hist(bins=30)
            
            plt.xlabel(x_column)
            if y_column:
                plt.ylabel(y_column)
            plt.title(f'{chart_type.capitalize()} Chart')
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return json.dumps({
                "status": "success",
                "chart_type": chart_type,
                "image_base64": image_base64,
                "message": "Chart created successfully. Image is base64 encoded."
            })
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def find_patterns(
        self,
        data_dict: Dict[str, List],
        pattern_type: str = "trends"
    ) -> str:
        """
        Find patterns and trends in the data.
        
        Args:
            data_dict: Dictionary representing the dataset
            pattern_type: Type of pattern ('trends', 'anomalies', 'clusters')
            
        Returns:
            JSON string with pattern analysis
        """
        try:
            df = pd.DataFrame(data_dict)
            results = {
                "status": "success",
                "pattern_type": pattern_type,
                "findings": []
            }
            
            if pattern_type == "trends":
                # Analyze trends in numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    # Simple trend: compare first half vs second half
                    mid = len(df) // 2
                    first_half_mean = df[col].iloc[:mid].mean()
                    second_half_mean = df[col].iloc[mid:].mean()
                    change = ((second_half_mean - first_half_mean) / first_half_mean) * 100
                    
                    results["findings"].append({
                        "column": col,
                        "trend": "increasing" if change > 5 else "decreasing" if change < -5 else "stable",
                        "change_percent": round(change, 2),
                        "first_half_avg": round(first_half_mean, 2),
                        "second_half_avg": round(second_half_mean, 2)
                    })
            
            elif pattern_type == "anomalies":
                # Find anomalies using z-score
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    mean = df[col].mean()
                    std = df[col].std()
                    z_scores = np.abs((df[col] - mean) / std)
                    anomalies = df[z_scores > 3]
                    
                    if len(anomalies) > 0:
                        results["findings"].append({
                            "column": col,
                            "anomaly_count": len(anomalies),
                            "anomaly_values": anomalies[col].tolist()[:10]  # First 10
                        })
            
            elif pattern_type == "clusters":
                # Simple clustering: group by categorical columns
                categorical_cols = df.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    value_counts = df[col].value_counts()
                    results["findings"].append({
                        "column": col,
                        "unique_values": len(value_counts),
                        "top_values": value_counts.head(5).to_dict()
                    })
            
            return json.dumps(results, indent=2, default=str)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            })
    
    def calculate_task_cost(self, estimated_hours: float) -> int:
        """
        Calculate cost for a task based on estimated hours.
        
        Args:
            estimated_hours: Estimated hours for the task
            
        Returns:
            Cost in cents
        """
        return int(estimated_hours * self.hourly_rate * 100)
    
    # ==================== AGENT EXECUTION ====================
    
    async def execute_task(
        self,
        task_description: str,
        client_id: str,
        data: Optional[Dict[str, List]] = None,
        auto_charge: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a data analysis task using Dedalus.
        
        Args:
            task_description: Description of the task
            client_id: ID of the client requesting the task
            data: Optional dataset to analyze
            auto_charge: Whether to automatically request payment after task
            
        Returns:
            Dictionary with task results and payment status
        """
        task_start_time = datetime.now()
        
        print(f"\n📊 Data Analyst Agent Executing Task")
        print(f"   Task: {task_description}")
        print(f"   Client: {client_id}")
        
        # Build the prompt for Dedalus
        prompt = f"""
You are a professional data analyst agent (ID: {self.agent_id}).

CLIENT: {client_id}
TASK: {task_description}
YOUR RATE: ${self.hourly_rate_cents/100:.2f}/hour

{"DATASET PROVIDED: Yes (access it via the tools)" if data else "DATASET PROVIDED: No"}

AVAILABLE TOOLS:
1. analyze_data(data_dict, analysis_type) - Perform statistical analysis
2. clean_data(data_dict, operations) - Clean and transform data
3. visualize_data(data_dict, chart_type, x_column, y_column) - Create charts
4. find_patterns(data_dict, pattern_type) - Find trends and patterns

INSTRUCTIONS:
1. Analyze the task requirements
2. Use the appropriate data analysis tools to complete the task
3. Provide clear insights and findings
4. Return a summary of your work

Begin working on the task now.
"""
        
        # Prepare tools for Dedalus
        tools = [
            self.analyze_data,
            self.clean_data,
            self.visualize_data,
            self.find_patterns
        ]
        
        # Execute with Dedalus
        try:
            result = await self.runner.run(
                input=prompt,
                model=self.model,
                tools=tools
            )
            
            # Calculate actual time spent (minimum 1 hour)
            time_spent_hours = max(1.0, (datetime.now() - task_start_time).total_seconds() / 3600)
            
            # Calculate earnings
            earnings_cents = int(time_spent_hours * self.hourly_rate_cents)
            self.total_earned_cents += earnings_cents
            
            # Record earning in Flux dashboard
            if auto_charge:
                try:
                    record_agent_earning(
                        agent_id=self.agent_id,
                        client_id=client_id,
                        amount_cents=earnings_cents,
                        service_description=f"Data analysis: {task_description[:100]}"
                    )
                    print(f"✅ Recorded ${earnings_cents/100:.2f} earning in Flux dashboard")
                except Exception as e:
                    print(f"⚠️  Could not record earning in Flux: {e}")
            
            print(f"\n✅ Data Analysis Complete!")
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
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary with agent status and balance
        """
        balance_info = check_balance(self.agent_id)
        
        return {
            "agent_id": self.agent_id,
            "agent_type": "DataAnalyst",
            "hourly_rate": self.hourly_rate,
            "model": self.model,
            "balance": balance_info,
            "status": "active"
        }


# ==================== EXAMPLE USAGE ====================

async def demo():
    """
    Demonstration of the DataAnalyst agent.
    """
    # Initialize agent
    analyst = DataAnalystAgent(
        agent_id="data-analyst-001",
        hourly_rate=25.0
    )
    
    # Sample dataset
    sample_data = {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "sales": [12000, 15000, 13000, 18000, 22000, 25000],
        "expenses": [8000, 9000, 8500, 10000, 12000, 13000]
    }
    
    print("=" * 60)
    print("DataAnalyst Agent Demo")
    print("=" * 60)
    
    # Execute a task
    result = await analyst.execute_task(
        task_description="Analyze the sales and expense data. Find trends and create a summary report.",
        client_id="marketing-team-001",
        data=sample_data,
        auto_charge=True
    )
    
    print(json.dumps(result, indent=2))
    
    # Check agent status
    status = await analyst.get_status()
    print("\n" + "=" * 60)
    print("Agent Status")
    print("=" * 60)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
