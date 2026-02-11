# Onboarding Experimentation System

## Overview
This project is an end-to-end experimentation system designed for a learning platform's onboarding/signup flow. It allows for:
- Simulating user data (Control vs. Treatment groups).
- Calculating key metrics (e.g., completion rates, retention).
- Performing statistical A/B tests.
- Generating final decisions on whether to ship experiments.

## Project Structure
- `src/simulation`: Modules for generating synthetic user data.
- `src/analysis`: Statistical analysis and metric calculation.
- `src/cli`: Command-line interface for running experiments.
- `tests`: Unit and integration tests.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI:
   ```bash
   python main.py
   ```
