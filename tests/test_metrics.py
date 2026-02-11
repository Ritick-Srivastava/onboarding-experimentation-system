import unittest
import pandas as pd
from src.metrics import MetricCalculator

class TestMetrics(unittest.TestCase):
    def test_conversion_rate(self):
        data = {'completed_onboarding': [1, 1, 0, 0]}
        df = pd.DataFrame(data)
        metrics = MetricCalculator()
        rate = metrics.calculate_conversion_rate(df)
        self.assertEqual(rate, 0.5)

    def test_retention_rate(self):
        data = {'is_active_7d': [1, 1, 1, 0, 0]}
        df = pd.DataFrame(data)
        metrics = MetricCalculator()
        rate = metrics.calculate_retention_rate(df)
        self.assertEqual(rate, 0.6)

    def test_empty_dataframe(self):
        df = pd.DataFrame({'completed_onboarding': [], 'time_spent_seconds': []})
        metrics = MetricCalculator()
        self.assertEqual(metrics.calculate_conversion_rate(df), 0.0)
        self.assertEqual(metrics.calculate_avg_time_spent(df), 0.0)

if __name__ == '__main__':
    unittest.main()
