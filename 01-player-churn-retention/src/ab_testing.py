"""
A/B testing framework for churn interventions.

Simulates treatment effects and evaluates intervention strategies.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class ABTestSimulator:
    """Simulate A/B tests for churn interventions."""
    
    def __init__(self, baseline_churn_rate: float = 0.636):
        self.baseline_churn_rate = baseline_churn_rate
        self.results = []
    
    def simulate_intervention(
        self,
        intervention_name: str,
        treatment_effect: float,
        sample_size: int = 1000,
        treatment_ratio: float = 0.5,
        random_state: int = 42
    ) -> Dict:
        """
        Simulate an A/B test for a churn intervention.
        
        Args:
            intervention_name: Name of the intervention
            treatment_effect: Relative reduction in churn rate (e.g., 0.15 = 15% reduction)
            sample_size: Total sample size
            treatment_ratio: Proportion in treatment group
            random_state: Random seed
        
        Returns:
            Dictionary with test results
        """
        np.random.seed(random_state)
        
        # Split into control and treatment
        n_treatment = int(sample_size * treatment_ratio)
        n_control = sample_size - n_treatment
        
        # Generate outcomes
        control_churn = np.random.binomial(1, self.baseline_churn_rate, n_control)
        
        # Treatment reduces churn rate
        treatment_churn_rate = self.baseline_churn_rate * (1 - treatment_effect)
        treatment_churn = np.random.binomial(1, treatment_churn_rate, n_treatment)
        
        # Calculate metrics
        control_rate = control_churn.mean()
        treatment_rate = treatment_churn.mean()
        
        # Statistical test
        chi2_stat, p_value = stats.chi2_contingency([
            [control_churn.sum(), n_control - control_churn.sum()],
            [treatment_churn.sum(), n_treatment - treatment_churn.sum()]
        ])[:2]
        
        # Effect size (relative risk reduction)
        relative_reduction = (control_rate - treatment_rate) / control_rate
        absolute_reduction = control_rate - treatment_rate
        
        # Confidence intervals
        control_ci = self._wilson_ci(control_churn.sum(), n_control)
        treatment_ci = self._wilson_ci(treatment_churn.sum(), n_treatment)
        
        result = {
            'intervention': intervention_name,
            'control_size': n_control,
            'treatment_size': n_treatment,
            'control_churn_rate': control_rate,
            'treatment_churn_rate': treatment_rate,
            'control_ci': control_ci,
            'treatment_ci': treatment_ci,
            'absolute_reduction': absolute_reduction,
            'relative_reduction': relative_reduction,
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'treatment_effect': treatment_effect
        }
        
        self.results.append(result)
        return result
    
    def _wilson_ci(self, successes: int, total: int, alpha: float = 0.05) -> Tuple[float, float]:
        """Calculate Wilson score confidence interval."""
        if total == 0:
            return (0, 0)
        
        p = successes / total
        z = stats.norm.ppf(1 - alpha / 2)
        
        denominator = 1 + z**2 / total
        center = (p + z**2 / (2 * total)) / denominator
        margin = z * np.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denominator
        
        return (max(0, center - margin), min(1, center + margin))
    
    def run_experiment_suite(self):
        """Run a suite of common churn interventions."""
        interventions = [
            {
                'name': 'Push Notification (Day 3)',
                'effect': 0.08,
                'sample_size': 2000,
                'description': 'Personalized re-engagement message'
            },
            {
                'name': 'Discount Offer (20% off)',
                'effect': 0.18,
                'sample_size': 1500,
                'description': 'Limited-time purchase incentive'
            },
            {
                'name': 'In-Game Rewards',
                'effect': 0.12,
                'sample_size': 2500,
                'description': 'Free coins/items for returning players'
            },
            {
                'name': 'Tutorial Improvement',
                'effect': 0.22,
                'sample_size': 3000,
                'description': 'Enhanced onboarding experience'
            },
            {
                'name': 'Daily Login Bonus',
                'effect': 0.15,
                'sample_size': 2000,
                'description': 'Streak-based rewards'
            },
            {
                'name': 'Social Feature Prompt',
                'effect': 0.10,
                'sample_size': 1800,
                'description': 'Encourage friend invites'
            }
        ]
        
        print("Running A/B Test Suite...")
        print("="*70)
        
        for i, intervention in enumerate(interventions, 1):
            result = self.simulate_intervention(
                intervention['name'],
                intervention['effect'],
                intervention['sample_size'],
                random_state=42 + i
            )
            
            print(f"\n{i}. {intervention['name']}")
            print(f"   {intervention['description']}")
            print(f"   Sample: {result['control_size']} control, {result['treatment_size']} treatment")
            print(f"   Control Churn: {result['control_churn_rate']:.1%} {result['control_ci']}")
            print(f"   Treatment Churn: {result['treatment_churn_rate']:.1%} {result['treatment_ci']}")
            print(f"   Reduction: {result['absolute_reduction']:.1%} absolute, {result['relative_reduction']:.1%} relative")
            print(f"   p-value: {result['p_value']:.4f} {'✓ Significant' if result['is_significant'] else '✗ Not significant'}")
    
    def plot_results(self, output_dir: str = 'output'):
        """Visualize A/B test results."""
        if not self.results:
            print("No results to plot")
            return
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.results)
        
        # Create comparison plot
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Churn rates comparison
        x = np.arange(len(df))
        width = 0.35
        
        axes[0].bar(x - width/2, df['control_churn_rate'] * 100, width, label='Control', alpha=0.8, color='#e74c3c')
        axes[0].bar(x + width/2, df['treatment_churn_rate'] * 100, width, label='Treatment', alpha=0.8, color='#2ecc71')
        
        axes[0].set_ylabel('Churn Rate (%)')
        axes[0].set_title('A/B Test Results: Control vs Treatment Churn Rates')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(df['intervention'], rotation=45, ha='right')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Effect sizes
        colors = ['green' if sig else 'gray' for sig in df['is_significant']]
        axes[1].barh(df['intervention'], df['relative_reduction'] * 100, color=colors, alpha=0.7)
        axes[1].set_xlabel('Relative Churn Reduction (%)')
        axes[1].set_title('Treatment Effect Sizes (Green = Statistically Significant)')
        axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig(output_path / 'ab_test_results.png', dpi=150, bbox_inches='tight')
        print(f"\nSaved A/B test visualization to: {output_path / 'ab_test_results.png'}")
    
    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: float = 0.05,
        power: float = 0.8
    ) -> int:
        """
        Calculate required sample size per group for A/B test.
        
        Args:
            baseline_rate: Control group conversion rate
            minimum_detectable_effect: Minimum effect to detect (relative)
            alpha: Type I error rate
            power: Statistical power (1 - Type II error rate)
        
        Returns:
            Required sample size per group
        """
        treatment_rate = baseline_rate * (1 - minimum_detectable_effect)
        
        # Z-scores
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        # Pooled proportion
        p_pooled = (baseline_rate + treatment_rate) / 2
        
        # Sample size calculation
        n = (
            (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) +
             z_beta * np.sqrt(baseline_rate * (1 - baseline_rate) + treatment_rate * (1 - treatment_rate))) ** 2
        ) / (baseline_rate - treatment_rate) ** 2
        
        return int(np.ceil(n))
    
    def sample_size_analysis(self):
        """Analyze sample size requirements for different effects."""
        print("\nSample Size Requirements (per group, α=0.05, power=0.8):")
        print("="*70)
        
        effects = [0.05, 0.10, 0.15, 0.20, 0.25]
        
        for effect in effects:
            n = self.calculate_sample_size(self.baseline_churn_rate, effect)
            print(f"To detect {effect*100:.0f}% relative reduction: {n:,} players per group (total: {2*n:,})")


if __name__ == "__main__":
    # Initialize simulator
    simulator = ABTestSimulator(baseline_churn_rate=0.636)
    
    # Run experiment suite
    simulator.run_experiment_suite()
    
    # Visualize results
    simulator.plot_results()
    
    # Sample size analysis
    simulator.sample_size_analysis()
    
    print("\n" + "="*70)
    print("A/B Testing Analysis Complete")
    print("="*70)
