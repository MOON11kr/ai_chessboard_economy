import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# === PARAMETERS === #
GRID_ROWS, GRID_COLS = 25, 40
NUM_WORKERS = GRID_ROWS * GRID_COLS
ALPHA_MEAN, ALPHA_STD = 0.05, 0.01
BETA, GAMMA, TAU, EPSILON = 0.8, 0.7, 0.3, 0.5
INITIAL_WAGE_MEAN, INITIAL_WAGE_STD = 100, 10
AI_PROFIT_PER_JOB = 50
NUM_STEPS = 50


class Worker:
    def __init__(self, wage):
        self.wage = wage
        self.employed = True
        self.consumption = BETA * wage

    def update(self):
        self.consumption = BETA * self.wage if self.employed else 0


class AIFirm:
    def __init__(self):
        self.material_gain = 0

    def update(self, num_employed, total_consumption, initial_consumption):
        alpha = max(0, np.random.normal(ALPHA_MEAN, ALPHA_STD))
        jobs_to_automate = int(alpha * num_employed)
        raw_profit = jobs_to_automate * AI_PROFIT_PER_JOB
        ratio = (
            total_consumption / initial_consumption
            if initial_consumption > 0
            else 0
        )
        adjusted_profit = raw_profit * max(0, 1 - EPSILON * (1 - ratio))
        self.material_gain += adjusted_profit
        return jobs_to_automate


class NonAIFirm:
    def __init__(self):
        self.revenue = 0

    def update(self, total_consumption):
        self.revenue = GAMMA * total_consumption


class Government:
    def __init__(self):
        self.tax_revenue = 0

    def update(self, workers, firms):
        wages = sum(w.wage for w in workers if w.employed)
        revenue = sum(f.revenue for f in firms)
        self.tax_revenue = TAU * (wages + revenue)
        return 0.5 * self.tax_revenue


class Economy:
    def __init__(self):
        wages = np.clip(
            np.random.normal(INITIAL_WAGE_MEAN, INITIAL_WAGE_STD, NUM_WORKERS),
            10,
            None
        )
        self.workers = [Worker(w) for w in wages]
        self.ai_firm = AIFirm()
        self.non_ai_firms = [NonAIFirm() for _ in range(5)]
        self.government = Government()
        self.initial_consumption = sum(w.consumption for w in self.workers)
        self.total_consumption = self.initial_consumption
        self.history = []

    def step(self):
        for w in self.workers:
            w.update()
        self.total_consumption = sum(w.consumption for w in self.workers)

        num_employed = sum(w.employed for w in self.workers)
        jobs_to_automate = self.ai_firm.update(
            num_employed,
            self.total_consumption,
            self.initial_consumption
        )

        employed_indices = [
            i for i, w in enumerate(self.workers) if w.employed
        ]
        np.random.shuffle(employed_indices)
        for idx in employed_indices[:jobs_to_automate]:
            self.workers[idx].employed = False

        for f in self.non_ai_firms:
            f.update(self.total_consumption)

        stimulus = self.government.update(self.workers, self.non_ai_firms)
        self.total_consumption += stimulus

        self.history.append({
            "employment": [w.employed for w in self.workers],
            "wages": [w.wage if w.employed else 0 for w in self.workers],
            "ai_profit": self.ai_firm.material_gain,
            "tax_revenue": self.government.tax_revenue,
            "consumption": self.total_consumption
        })


def animate_economy():
    economy = Economy()
    for _ in range(NUM_STEPS):
        economy.step()

    # Create figure with adjusted layout
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])

    # Main plot for chessboard
    ax1 = fig.add_subplot(gs[0])
    ax1.axis("off")
    title = ax1.set_title(
        "AI Economic Disruption Simulation",
        fontsize=16,
        pad=20
    )

    # Create chessboard pattern
    chess_pattern = np.indices((GRID_ROWS, GRID_COLS)).sum(axis=0) % 2
    ax1.imshow(chess_pattern, cmap='binary', alpha=0.1)

    # Initialize heatmap for wages
    im = ax1.imshow(
        np.zeros((GRID_ROWS, GRID_COLS)),
        cmap='RdYlGn',
        vmin=0,
        vmax=150,
        alpha=0.8  # Slightly transparent to see chessboard
    )

    # Add grid lines
    ax1.set_xticks(np.arange(-0.5, GRID_COLS, 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, GRID_ROWS, 1), minor=True)
    ax1.grid(which='minor', color='black', linewidth=0.3)

    # Side panel for metrics
    ax2 = fig.add_subplot(gs[1])
    ax2.axis("off")

    # Create text box for metrics
    metrics_text = ax2.text(
        0.1, 0.5,
        "",
        transform=ax2.transAxes,
        fontsize=12,
        va='center',
        bbox=dict(facecolor='white', alpha=0.7, boxstyle='round')
    )

    # Add colorbar below chessboard with adjusted position
    cax = fig.add_axes(
        [0.15, 0.05, 0.3, 0.03]
    )  # [left, bottom, width, height]
    cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label('Wage Levels ($)', fontsize=10)

    def update(frame):
        data = economy.history[frame]
        grid = np.array(data["wages"]).reshape((GRID_ROWS, GRID_COLS))
        im.set_array(grid)
        title.set_text(f"Step {frame + 1}/{NUM_STEPS}")

        # Format metrics with larger font for key numbers
        employed_pct = np.mean(data["employment"]) * 100
        info = (
            "Economic Metrics:\n\n"
            f"Employment:  {employed_pct:.1f}%\n"
            f"AI Profit:   ${data['ai_profit']:,.0f}\n"
            f"Tax Revenue: ${data['tax_revenue']:,.0f}\n"
            f"Consumption: ${data['consumption']:,.0f}"
        )
        metrics_text.set_text(info)

        return [im, title, metrics_text]

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=NUM_STEPS,
        interval=300,
        repeat=False
    )

    ani.save("ai_disruption_chessboard.gif", writer='pillow', fps=2, dpi=100)
    plt.show()


if __name__ == "__main__":
    animate_economy()
