import pandas as pd
import numpy as np
from typing import Tuple

class DataSimulator:
    """
    Simulates user data for an onboarding A/B test.
    """
    def __init__(self, n_users: int = 1000, split_ratio: float = 0.5):
        self.n_users = n_users
        self.split_ratio = split_ratio

    def generate_data(self, 
                      control_conversion_rate: float = 0.20, 
                      treatment_lift: float = 0.05, 
                      retention_rate: float = 0.40,
                      time_spent_mean: float = 300, 
                      time_spent_std: float = 60) -> pd.DataFrame:
        """
        Generates a synthetic dataset with user metrics.
        
        Args:
            control_conversion_rate: Base conversion rate for control group (0-1).
            treatment_lift: Absolute increase in conversion rate for treatment group.
            retention_rate: Base retention rate.
            time_spent_mean: Average time spent in seconds.
            time_spent_std: Standard deviation of time spent.
            
        Returns:
            pd.DataFrame: Simulated user data.
        """
        # Removed fixed seed to allow for live, unique simulations on every run
        # np.random.seed(42)  
        
        # Assign groups
        groups = np.random.choice(['control', 'treatment'], 
                                  size=self.n_users, 
                                  p=[1-self.split_ratio, self.split_ratio])
        
        data = {
            'user_id': range(1, self.n_users + 1),
            'group': groups,
            'started_onboarding': np.ones(self.n_users, dtype=int)
        }
        
        df = pd.DataFrame(data)
        
        # Simulate completion based on group conversion rates
        # Control
        control_mask = df['group'] == 'control'
        n_control = control_mask.sum()
        df.loc[control_mask, 'completed_onboarding'] = np.random.binomial(1, control_conversion_rate, n_control)
        
        # Treatment
        treatment_mask = df['group'] == 'treatment'
        n_treatment = treatment_mask.sum()
        
        # Calculate treatment conversion using relative lift
        # treatment_lift is now expected as a relative percentage (e.g., 0.05 for 5% lift)
        treatment_conversion = control_conversion_rate * (1 + treatment_lift)
        
        # Clamp between 0 and 1
        treatment_conversion = max(0.0, min(1.0, treatment_conversion))
        
        df.loc[treatment_mask, 'completed_onboarding'] = np.random.binomial(1, treatment_conversion, n_treatment)
        
        # Simulate retention (users who completed are more likely to retain?)
        # Let's assume retention is independent or slightly correlated for simplicity, 
        # or maybe treatment has higher retention too? 
        # For now, base retention, maybe slightly higher for completers.
        base_retention = np.random.binomial(1, retention_rate, self.n_users)
        # Boost retention for those who completed onboarding (+10%)
        completers = df['completed_onboarding'] == 1
        boost = np.random.binomial(1, 0.1, self.n_users)
        final_retention = np.minimum(1, base_retention + (completers * boost))
        
        df['is_active_7d'] = final_retention
        
        # Simulate time spent (log-normal distribution often better for time, but normal is okay for simple sim)
        # Maybe treatment reduces time spent (more efficient)?
        # Let's assume treatment is slightly faster (-10%)
        time_spent = np.random.normal(time_spent_mean, time_spent_std, self.n_users)
        df.loc[treatment_mask, 'time_spent_seconds'] = time_spent[treatment_mask] * 0.9 
        df.loc[control_mask, 'time_spent_seconds'] = time_spent[control_mask]
        
        # Ensure non-negative time
        df['time_spent_seconds'] = np.maximum(0, df['time_spent_seconds'])

        return df

if __name__ == "__main__":
    sim = DataSimulator(n_users=10)
    print(sim.generate_data().head())
