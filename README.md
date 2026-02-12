# 📊 Onboarding Experimentation System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyScript](https://img.shields.io/badge/PyScript-WebAssembly-orange?style=for-the-badge)](https://pyscript.net)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

An end-to-end, high-fidelity experimentation framework designed for learning platforms. This system bridges the gap between raw user behavior simulation and actionable product decisions using a dual-methodology statistical approach.

---

## 🚀 Key Features

- **Synthetic User Simulation**: Generates high-entropy user data simulating onboarding flows, conversion events, 7-day retention, and engagement metrics.
- **Dual Statistical Engine**:
    - **Frequentist Analysis**: T-Tests and P-values for classical significance testing.
    - **Bayesian Analysis**: Beta-Binomial models to calculate the *Probability of being better* and *Expected Loss* (Risk).
- **Interactive Dashboard**: A premium, PyScript-powered web interface that runs Python logic directly in the browser using WebAssembly.
- **Decision Logic**: Automated consensus matching between statistical frameworks to recommend "Ship", "Wait", or "Reject".
- **CLI Toolset**: Robust command-line interface for batch simulation and historical data analysis.

---

## 🛠️ Tech Stack

- **Backend Logic**: Python 3.9+, Pandas, NumPy, SciPy, Matplotlib
- **CLI Framework**: Click
- **Frontend**: HTML5, Tailwind CSS (Glassmorphism design)
- **Runtime**: PyScript (Micropip for in-browser dependencies)
- **Deployment**: GitHub Pages & GitHub Actions

---

## 📂 Project Structure

```text
├── .github/workflows/    # CI/CD: Automated deployment to GitHub Pages
├── src/
│   ├── analysis/
│   │   └── stats.py      # Statistical core (Frequentist & Bayesian)
│   ├── metrics.py        # Calculation of CR, Retention, and Engagement
│   └── simulation.py     # User event generation engine
├── tests/                # Comprehensive unit tests for metrics and simulation
├── index.html            # PyScript-driven Interactive Dashboard
├── main.py               # CLI Entry point
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## 💻 Usage

### 1. Command Line Interface (CLI)

First, install the local dependencies:
```bash
pip install -r requirements.txt
```

**Simulate Data:**
```bash
python main.py simulate --users 5000 --control-rate 0.15 --lift 0.05
```

**Analyze Results:**
```bash
python main.py analyze --input experiment_data.csv
```

### 2. Interactive Dashboard

You can view the dashboard live on **GitHub Pages** (if deployed) or run it locally using any static web server:

```bash
# Example using Python's built-in server
python -m http.server 8000
```
Then navigate to `http://localhost:8000`.

---

## 🧪 Testing

The system includes a suite of tests to ensure statistical accuracy and data integrity.
```bash
pytest tests/
```

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ for Data-Driven Experimentation.*
