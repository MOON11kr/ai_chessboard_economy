```markdown
# AI Chessboard Economy Model

This repository contains the Python implementation of the "Chessboard Economy" model, as described in the paper:  
**"The Self-Limiting Dynamics of AI Automation: A Chessboard Model of Economic Collapse"**  
by Karishma M Patel and Shivang Mishra.

## Overview
The model simulates the cascading effects of AI-driven job displacement on macroeconomic indicators using a multi-agent system. Key features include:
- Stochastic wage distributions and automation rates.
- Spatial visualization of job loss and wage distribution on a 2D grid.
- Dynamic feedback loops between automation, consumption, and profitability.
- Policy interventions such as taxation, stimulus, and Universal Basic Income (UBI).

## Key Components
1. **Workers**: Consume a fraction of their income if employed.
2. **AI Firms**: Automate jobs probabilistically, with profits tied to market demand.
3. **Non-AI Firms**: Revenue depends on aggregate consumption.
4. **Government**: Collects taxes and reinvests a portion as stimulus.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MOOM11kr/ai_chessboard_economy.git
   ```
2. Install the required dependencies:
   ```bash
   pip install numpy matplotlib pandas
   ```

## Usage
Run the main simulation script to generate results:
```bash
python main_simulation.py
```
This will produce:
- Line graphs of key metrics (employment, consumption, tax revenue, AI profit).
- An animated heatmap showing spatial job loss dynamics (saved as `ai_disruption_chessboard.gif`).

## Model Parameters
Adjustable parameters in `config.py` include:
- `alpha`: Job automation rate.
- `beta`: Propensity to consume.
- `tau`: Tax rate.
- `sigma`: Fraction of tax revenue used for stimulus.
- `epsilon`: Sensitivity of AI profit to demand drop.

## Policy Scenarios
The model supports testing various policy interventions (e.g., UBI, progressive taxation). Example configurations are provided in `policy_scenarios.py`.

## Outputs
- **Normalized Trends**: Time-series data for macroeconomic indicators (see `Figure 1` in the paper).
- **Chessboard Heatmap**: Visualizes unemployment spread across the grid (supplementary animation).

## References
For theoretical background, see the [paper](https://example.com) and citations therein.

## License
This project is open-source under the MIT License. See `LICENSE` for details.

## Contact
- Karishma M Patel: karishma2p@gmail.com  
- Shivang Mishra: shivang.m04@gmail.com  
```

