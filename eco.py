import matplotlib.pyplot as plt
import numpy as np


# Parameters for ASDM (can be adjusted)
ALPHA_MEAN = 0.05       # Mean job automation rate
ALPHA_STD = 0.01        # Std dev for stochastic automation rate
BETA = 0.8              # Propensity to consume
GAMMA = 0.7             # Demand elasticity for non-AI firms
TAU = 0.3               # Tax rate
EPSILON = 0.5           # AI firm's market dependency on consumption
INITIAL_JOBS = 1000     # Initial employed workers
INITIAL_WAGE_MEAN = 100  # Average wage per worker
INITIAL_WAGE_STD = 10    # Wage heterogeneity (std dev)
AI_PROFIT_PER_JOB = 50   # Profit per automated job
NUM_STEPS = 50           # Simulation steps


class Worker:
    """Worker with heterogeneous wage and consumption based on employment."""
    def __init__(self, wage):
        self.employed = True
        self.wage = wage
        self.consumption = self.wage * BETA if self.employed else 0

    def update(self):
        """Update consumption (C_t = β * W_t if employed)."""
        self.consumption = self.wage * BETA if self.employed else 0


class AIFirm:
    """
    AI firm automating jobs and adjusting profits based on market conditions.
    """
    def __init__(self):
        self.material_gain = 0  # Accumulated profit

    def update(self, num_employed, total_consumption, initial_consumption):
        """
        Automate jobs with stochastic rate, calculate adjusted profit.

        Returns:
            int: Number of jobs automated this step
        """
        # Stochastic automation rate simulating shocks in tech adoption
        alpha = max(0, np.random.normal(ALPHA_MEAN, ALPHA_STD))

        jobs_to_automate = int(alpha * num_employed)
        raw_profit = jobs_to_automate * AI_PROFIT_PER_JOB

        # Market effect: profit adjusted by consumption ratio
        ratio = (
            total_consumption / initial_consumption
            if initial_consumption > 0
            else 0
        )
        profit_adjusted = raw_profit * max(0, 1 - EPSILON * (1 - ratio))

        self.material_gain += profit_adjusted
        return jobs_to_automate


class NonAIFirm:
    """Non-AI firm with revenue tied linearly to total consumption."""
    def __init__(self):
        self.revenue = 0

    def update(self, total_consumption):
        """Revenue proportional to total consumption (demand)."""
        self.revenue = GAMMA * total_consumption


class Government:
    """Government collects taxes and provides stimulus to support demand."""
    def __init__(self):
        self.tax_revenue = 0

    def update(self, num_employed, non_ai_firms, workers):
        """
        Tax wages and firm revenues, return stimulus (fraction of tax).

        Args:
            num_employed: Currently employed workers
            non_ai_firms: List of NonAIFirm instances
            workers: List of Worker instances

        Returns:
            float: Government stimulus amount
        """
        wages = sum(
            worker.wage
            for worker in workers
            if worker.employed
        )
        firm_revenue = sum(f.revenue for f in non_ai_firms)
        self.tax_revenue = TAU * (wages + firm_revenue)
        return 0.5 * self.tax_revenue  # Government stimulus spending


class Economy:
    """Economy simulating AI disruption with heterogeneity and shocks."""
    def __init__(self):
        # Initialize workers with wage heterogeneity
        wages = np.random.normal(
            INITIAL_WAGE_MEAN,
            INITIAL_WAGE_STD,
            INITIAL_JOBS
        )
        wages = np.clip(wages, a_min=10, a_max=None)  # No negative wages

        self.workers = [Worker(wage=w) for w in wages]
        self.num_employed = INITIAL_JOBS
        self.ai_firm = AIFirm()
        self.non_ai_firms = [NonAIFirm() for _ in range(5)]
        self.government = Government()

        # Initial total consumption
        self.total_consumption = sum(w.consumption for w in self.workers)
        self.initial_consumption = self.total_consumption

        # Store simulation data
        self.data = {
            "Employment": [self.num_employed],
            "Consumption": [self.total_consumption],
            "Tax Revenue": [0],
            "AI Profit": [0],
            "Non-AI Revenue": [0]
        }

    def step(self):
        """Run one timestep of the economy simulation."""
        # Update workers' consumption based on employment and wage
        for worker in self.workers:
            worker.update()
        self.total_consumption = sum(w.consumption for w in self.workers)

        # AI firm automates jobs
        jobs_to_automate = self.ai_firm.update(
            self.num_employed,
            self.total_consumption,
            self.initial_consumption
        )

        # Automate jobs by setting workers to unemployed
        employed_indices = [
            i for i, w in enumerate(self.workers)
            if w.employed
        ]
        to_automate_indices = employed_indices[:jobs_to_automate]

        for idx in to_automate_indices:
            self.workers[idx].employed = False

        self.num_employed = sum(1 for w in self.workers if w.employed)

        # Update non-AI firms' revenue based on new consumption
        for firm in self.non_ai_firms:
            firm.update(self.total_consumption)

        stimulus = self.government.update(
            self.num_employed,
            self.non_ai_firms,
            self.workers
        )
        self.total_consumption += stimulus

        # Record data for analysis
        self.data["Employment"].append(self.num_employed)
        self.data["Consumption"].append(self.total_consumption)
        self.data["Tax Revenue"].append(self.government.tax_revenue)
        self.data["AI Profit"].append(self.ai_firm.material_gain)
        self.data["Non-AI Revenue"].append(
            sum(f.revenue for f in self.non_ai_firms)
        )


def run_simulation():
    """Run and visualize the economic simulation."""
    economy = Economy()

    for _ in range(NUM_STEPS):
        economy.step()

    data = economy.data
    # Normalize for visualization purposes
    normalized = {
        key: [v / max(values) if max(values) > 0 else 0 for v in values]
        for key, values in data.items()
    }

    plt.figure(figsize=(10, 6))
    for key, values in normalized.items():
        plt.plot(values, label=key)
    plt.xlabel("Time Step")
    plt.ylabel("Normalized Value")
    plt.title("AI Economic Disruption Simulation with Heterogeneity & Shocks")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_simulation()
