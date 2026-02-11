import pandas as pd
from typing import Dict, Any

class MetricCalculator:
    """
    Calculates key metrics for the experimentation system.
    """
    
    @staticmethod
    def calculate_conversion_rate(df: pd.DataFrame) -> float:
        """Calculates completion rate."""
        if len(df) == 0:
            return 0.0
        return df['completed_onboarding'].mean()

    @staticmethod
    def calculate_retention_rate(df: pd.DataFrame) -> float:
        """Calculates 7-day retention rate."""
        if len(df) == 0:
            return 0.0
        return df['is_active_7d'].mean()

    @staticmethod
    def calculate_avg_time_spent(df: pd.DataFrame) -> float:
        """Calculates average time spent in onboarding (seconds)."""
        if len(df) == 0:
            return 0.0
        return df['time_spent_seconds'].mean()

    def generate_report(self, control_df: pd.DataFrame, treatment_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Generates a comparison report of metrics between control and treatment groups.
        """
        metrics = {
            'conversion_rate': self.calculate_conversion_rate,
            'retention_rate_7d': self.calculate_retention_rate,
            'avg_time_spent': self.calculate_avg_time_spent
        }
        
        report = {}
        for name, func in metrics.items():
            control_val = func(control_df)
            treatment_val = func(treatment_df)
            lift = (treatment_val - control_val) / control_val if control_val > 0 else 0.0
            
            report[name] = {
                'control': control_val,
                'treatment': treatment_val,
                'lift_percent': lift * 100
            }
            
        return report
