import click
import pandas as pd
from src.simulation import DataSimulator
from src.metrics import MetricCalculator
from src.analysis.stats import StatisticalTest

@click.group()
def cli():
    """Onboarding Experimentation System CLI"""
    pass

@cli.command()
@click.option('--users', default=1000, help='Number of users to simulate')
@click.option('--control-rate', default=0.20, help='Control group conversion rate')
@click.option('--lift', default=0.05, help='Expected lift in treatment group')
@click.option('--output', default='experiment_data.csv', help='Output file for data')
def simulate(users, control_rate, lift, output):
    """Simulate user data for the experiment."""
    click.echo(f"Simulating data for {users} users...")
    sim = DataSimulator(n_users=users)
    df = sim.generate_data(control_conversion_rate=control_rate, treatment_lift=lift)
    df.to_csv(output, index=False)
    click.echo(f"Data saved to {output}")

@cli.command()
@click.option('--input', default='experiment_data.csv', help='Input data file')
def analyze(input):
    """Analyze experiment results from a data file."""
    try:
        df = pd.read_csv(input)
    except FileNotFoundError:
        click.echo(f"Error: File {input} not found. Run 'simulate' first.")
        return

    control_df = df[df['group'] == 'control']
    treatment_df = df[df['group'] == 'treatment']
    
    click.echo(f"Analyzing experiment with {len(df)} users ({len(control_df)} Control, {len(treatment_df)} Treatment)...")

    # Metrics
    calc = MetricCalculator()
    metrics = {
        'Conversion Rate': 'conversion_rate',
        'Retention Rate': 'retention_rate_7d',
        'Avg Time (s)': 'avg_time_spent'
    }
    
    # Statistical Tests
    stats_test = StatisticalTest()
    stat_results = stats_test.analyze_experiment(control_df, treatment_df)
    
    click.echo("\n--- Experiment Results: Methodology Comparison ---\n")
    
    # Print table header
    header = f"{'Metric':<18} | {'Frequentist':<15} | {'Bayesian':<30}"
    click.echo(header)
    click.echo(f"{'':<18} | {'(P-Value)':<15} | {'(Prob T>C / Exp Loss)':<30}")
    click.echo("-" * 75)
    
    for label, metric_key in metrics.items():
        # Display data
        m_results = stat_results[metric_key]
        
        freq_p = m_results['frequentist']['p_value']
        freq_sig = "*" if freq_p < 0.05 else ""
        
        bay_prob = m_results['bayesian']['prob_t_better']
        bay_loss = m_results['bayesian']['expected_loss']
        
        click.echo(f"{label:<18} | {freq_p:.4f}{freq_sig:<10} | {bay_prob:>7.2%} / {bay_loss:.4f}")

    click.echo("\nDecision Logic:")
    # Comparison
    conv_res = stat_results['conversion_rate']
    
    f_sig = conv_res['frequentist']['significant']
    b_sig = conv_res['bayesian']['prob_t_better'] > 0.95
    
    if f_sig and b_sig:
        click.echo("[SUCCESS] CONSENSUS: Both frameworks agree this change is significant.")
    elif b_sig and not f_sig:
        click.echo("[WARNING] CONFLICT: Bayesian shows high confidence, but Frequentist is not significant yet.")
    elif f_sig and not b_sig:
        click.echo("[WARNING] CONFLICT: Frequentist is significant, but Bayesian risk (Exp Loss) might be high.")
    else:
        click.echo("[REJECT] CONSENSUS: Neither framework suggests shipping.")

if __name__ == '__main__':
    cli()
