from scipy import stats
import pandas as pd
import numpy as np
from typing import Dict, Any

class BayesianAnalysis:
    """
    Performs Bayesian statistical analysis for A/B experiments.
    """
    
    def __init__(self, samples: int = 20000):
        self.samples = samples

    def analyze_proportion(self, control_success: int, control_total: int, 
                          treatment_success: int, treatment_total: int,
                          prior_alpha: float = 1, prior_beta: float = 1) -> Dict[str, float]:
        """
        Bayesian analysis for proportions (e.g., Conversion Rate) using Beta-Binomial model.
        """
        # Posteriors
        control_posterior = stats.beta(prior_alpha + control_success, 
                                      prior_beta + control_total - control_success)
        treatment_posterior = stats.beta(prior_alpha + treatment_success, 
                                        prior_beta + treatment_total - treatment_success)
        
        # Sampling
        c_samples = control_posterior.rvs(self.samples)
        t_samples = treatment_posterior.rvs(self.samples)
        
        # Calculations
        prob_t_better = np.mean(t_samples > c_samples)
        
        # Expected Loss: E[max(0, C - T)]
        loss_t = np.maximum(0, c_samples - t_samples)
        expected_loss = np.mean(loss_t)
        
        # Credible Intervals (95%)
        ci_t = np.percentile(t_samples, [2.5, 97.5])
        
        return {
            'prob_t_better': prob_t_better,
            'expected_loss': expected_loss,
            'posterior_mean_t': np.mean(t_samples),
            'ci_lower_t': ci_t[0],
            'ci_upper_t': ci_t[1]
        }

    def analyze_means(self, control_data: pd.Series, treatment_data: pd.Series) -> Dict[str, float]:
        """
        Bayesian analysis for continuous means (e.g., Time Spent) using Normal model.
        Assumes normal distribution with unknown mean and variance (simplified with large samples).
        """
        # For simplicity with large samples, we use normal distribution of the mean
        # Control
        c_mean, c_std = control_data.mean(), control_data.std()
        c_se = c_std / np.sqrt(len(control_data))
        
        # Treatment
        t_mean, t_std = treatment_data.mean(), treatment_data.std()
        t_se = t_std / np.sqrt(len(treatment_data))
        
        # Generate samples from the posterior of the means
        c_samples = np.random.normal(c_mean, c_se, self.samples)
        t_samples = np.random.normal(t_mean, t_se, self.samples)
        
        # Probability T < C (since lower time is better)
        prob_t_better = np.mean(t_samples < c_samples)
        
        # Expected Loss for time (loss if T is actually slower than C)
        loss_t = np.maximum(0, t_samples - c_samples)
        expected_loss = np.mean(loss_t)
        
        return {
            'prob_t_better': prob_t_better,
            'expected_loss': expected_loss,
            'posterior_mean_t': t_mean
        }

class StatisticalTest:
    """
    Analyzes experiments using both Frequentist and Bayesian statistics.
    """
    
    def __init__(self):
        self.bayesian = BayesianAnalysis()

    @staticmethod
    def frequentist_z_test(control_success: int, control_total: int, 
                           treatment_success: int, treatment_total: int) -> Dict[str, Any]:
        """Runs a Frequentist Z-test for proportions."""
        p1 = control_success / control_total
        p2 = treatment_success / treatment_total
        p_pool = (control_success + treatment_success) / (control_total + treatment_total)
        se = np.sqrt(p_pool * (1 - p_pool) * (1/control_total + 1/treatment_total))
        z_score = (p2 - p1) / se
        p_value = stats.norm.sf(abs(z_score)) * 2
        return {'p_value': p_value, 'significant': p_value < 0.05}

    @staticmethod
    def frequentist_t_test(control_data: pd.Series, treatment_data: pd.Series) -> Dict[str, Any]:
        """Runs a Frequentist T-test for means."""
        t_stat, p_value = stats.ttest_ind(control_data, treatment_data, equal_var=False)
        return {'p_value': p_value, 'significant': p_value < 0.05}

    def analyze_experiment(self, control_df: pd.DataFrame, treatment_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes the experiment using both methodologies.
        """
        results = {}
        
        # Proportions: Conversion and Retention
        for key, col in [('conversion_rate', 'completed_onboarding'), 
                         ('retention_rate_7d', 'is_active_7d')]:
            c_succ, c_total = control_df[col].sum(), len(control_df)
            t_succ, t_total = treatment_df[col].sum(), len(treatment_df)
            
            results[key] = {
                'bayesian': self.bayesian.analyze_proportion(c_succ, c_total, t_succ, t_total),
                'frequentist': self.frequentist_z_test(c_succ, c_total, t_succ, t_total)
            }
        
        # Means: Time Spent
        results['avg_time_spent'] = {
            'bayesian': self.bayesian.analyze_means(control_df['time_spent_seconds'], 
                                                   treatment_df['time_spent_seconds']),
            'frequentist': self.frequentist_t_test(control_df['time_spent_seconds'], 
                                                   treatment_df['time_spent_seconds'])
        }
        
        return results
