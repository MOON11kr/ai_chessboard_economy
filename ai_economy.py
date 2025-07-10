import matplotlib.pyplot as plt

# Parameters for ASDM
ALPHA = 0.05      # Job automation rate
BETA = 0.8        # Propensity to consume
GAMMA = 0.7       # Demand elasticity
TAU = 0.3         # Tax rate
EPSILON = 0.5     # AI firm market dependency
INITIAL_JOBS = 1000  # Initial employed workers
INITIAL_WAGE = 100   # Wage per worker
AI_PROFIT_PER_JOB = 50  # Profit per automated job
NUM_STEPS = 50     # Simulation steps


class Worker:
    """Worker consuming based on employment status."""
    def __init__(self, wage=INITIAL_WAGE):
        self.employed = True
        self.wage = wage
        self.consumption = self.wage * BETA if self.employed else 0

    def update(self):
        """Update consumption (C_t = β * W_t if employed)."""
        self.consumption = self.wage * BETA if self.employed else 0


class AIFirm:
    """AI firm automating jobs, risking economic disruption."""
    def __init__(self):
        self.material_gain = 0  # Profit (chess material gain)

    def update(self, num_employed, total_consumption, initial_consumption):
        """Automate jobs (L_t+1 = L_t - α S_t), adjust profit."""
        jobs_to_automate = int(ALPHA * num_employed)
        raw_profit = jobs_to_automate * AI_PROFIT_PER_JOB
        ratio = (total_consumption / initial_consumption
                 if initial_consumption > 0 else 0)
        self.material_gain += raw_profit * max(0, 1 - EPSILON * (1 - ratio))
        return jobs_to_automate


class NonAIFirm:
    """Non-AI firm with revenue tied to demand."""
    def __init__(self):
        self.revenue = 0

    def update(self, total_consumption):
        """Update revenue (R_t+1 = R_t - γ ΔC_t)."""
        self.revenue = GAMMA * total_consumption


class Government:
    """Government taxing and spending to support demand."""
    def __init__(self):
        self.tax_revenue = 0

    def update(self, num_employed, non_ai_firms):
        """Collect taxes, boost consumption (T_t+1 = τ R_t)."""
        wages = num_employed * INITIAL_WAGE
        firm_revenue = sum(f.revenue for f in non_ai_firms)
        self.tax_revenue = TAU * (wages + firm_revenue)
        return 0.5 * self.tax_revenue  # Stimulus effect


class Economy:
    """Economy simulating AI self-disruption feedback loop."""
    def __init__(self):
        self.num_employed = INITIAL_JOBS
        self.workers = [Worker() for _ in range(INITIAL_JOBS)]
        self.ai_firm = AIFirm()
        self.non_ai_firms = [NonAIFirm() for _ in range(5)]
        self.government = Government()
        self.total_consumption = INITIAL_JOBS * INITIAL_WAGE * BETA
        self.initial_consumption = self.total_consumption
        self.data = {
            "Employment": [self.num_employed],
            "Consumption": [self.total_consumption],
            "Tax Revenue": [0],
            "AI Profit": [0],
            "Non-AI Revenue": [0]
        }

    def step(self):
        """Advance one step, updating state and collecting data."""
        # Update workers' consumption
        for worker in self.workers:
            worker.update()
        self.total_consumption = sum(w.consumption for w in self.workers)

        # AI firm automates jobs
        jobs_to_automate = self.ai_firm.update(
            self.num_employed, self.total_consumption, self.initial_consumption
        )
        for i, worker in enumerate(self.workers):
            if i < jobs_to_automate and worker.employed:
                worker.employed = False
        self.num_employed = sum(1 for w in self.workers if w.employed)

        # Update non-AI firms
        for firm in self.non_ai_firms:
            firm.update(self.total_consumption)

        # Government taxes and spends
        stimulus = self.government.update(self.num_employed, self.non_ai_firms)
        self.total_consumption += stimulus

        # Collect data
        self.data["Employment"].append(self.num_employed)
        self.data["Consumption"].append(self.total_consumption)
        self.data["Tax Revenue"].append(self.government.tax_revenue)
        self.data["AI Profit"].append(self.ai_firm.material_gain)
        self.data["Non-AI Revenue"].append(
            sum(f.revenue for f in self.non_ai_firms)
        )


# Run simulation
if __name__ == "__main__":
    economy = Economy()
    for _ in range(NUM_STEPS):
        economy.step()

    # Normalize data for plotting
    data = economy.data
    normalized = {key: [v / max(values) for v in values]
                  for key, values in data.items()}

    # Plot results
    plt.figure(figsize=(10, 6))
    for key, values in normalized.items():
        plt.plot(values, label=key)
    plt.xlabel("Time Step")
    plt.ylabel("Normalized Value")
    plt.title("AI Economic Disruption Simulation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ai_economy_simulation.png")
    plt.show()
