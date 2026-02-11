import unittest
from src.simulation import DataSimulator

class TestSimulation(unittest.TestCase):
    def test_generate_data_shape(self):
        sim = DataSimulator(n_users=100)
        df = sim.generate_data()
        self.assertEqual(len(df), 100)
        self.assertIn('group', df.columns)
        self.assertIn('completed_onboarding', df.columns)
        self.assertIn('time_spent_seconds', df.columns)

    def test_control_vs_treatment(self):
        sim = DataSimulator(n_users=200)
        df = sim.generate_data()
        groups = df['group'].unique()
        self.assertIn('control', groups)
        self.assertIn('treatment', groups)

if __name__ == '__main__':
    unittest.main()
