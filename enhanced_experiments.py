"""
Enhanced Experimental Framework for CS29 Ski Rental Project

This module provides comprehensive experimental tools to validate algorithmic improvements
and bridge the theory-practice gap identified in the original implementation.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from scipy import stats
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import enhanced algorithms
from enhanced_algorithms import (
    EnhancedAdaptiveHybridAlgorithm, 
    TheoreticalAnalysisFramework,
    AlgorithmResult
)

# Import original algorithms for comparison
from ski_rental_algorithms import (
    AdaptiveHybridRandomAlgorithm,
    OptimalOfflineAlgorithm
)

@dataclass
class ExperimentConfig:
    """Configuration for experimental runs."""
    algorithm_name: str
    algorithm_params: Dict[str, Any]
    scenario_params: Dict[str, Any]
    num_simulations: int = 100000
    confidence_level: float = 0.95
    enable_parallel: bool = True
    random_seed: Optional[int] = None

@dataclass 
class ExperimentResult:
    """Comprehensive experiment results."""
    config: ExperimentConfig
    avg_cost: float
    std_cost: float
    competitive_ratio: float
    confidence_interval: Tuple[float, float]
    execution_time: float
    convergence_achieved: bool
    sample_size_used: int
    detailed_stats: Dict[str, float]
    scenario_classification: str
    
class EnhancedExperimentalFramework:
    """
    Comprehensive experimental framework addressing the theory-practice gap.
    """
    
    def __init__(self, output_dir: str = "enhanced_results"):
        self.output_dir = output_dir
        self.results_cache = {}
        self.theoretical_analyzer = TheoreticalAnalysisFramework()
        
        # Ensure output directory exists
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def run_enhanced_comparison_study(self, scenarios: List[Dict[str, Any]], 
                                    algorithms: List[str]) -> pd.DataFrame:
        """
        Comprehensive comparison between original and enhanced algorithms.
        """
        logger.info("Starting enhanced comparison study...")
        
        all_results = []
        
        for scenario in scenarios:
            scenario_name = scenario['name']
            params = scenario['params']
            
            logger.info(f"Processing scenario: {scenario_name}")
            
            # Test each algorithm
            for alg_name in algorithms:
                
                if alg_name == "original_adaptive":
                    config = ExperimentConfig(
                        algorithm_name=alg_name,
                        algorithm_params={},
                        scenario_params=params,
                        num_simulations=100000
                    )
                    
                    result = self._run_original_algorithm_experiment(config)
                    
                elif alg_name.startswith("enhanced_"):
                    strategy = alg_name.split("_", 1)[1]  # e.g., "multi_factor"
                    
                    config = ExperimentConfig(
                        algorithm_name=alg_name,
                        algorithm_params={'adaptive_strategy': strategy},
                        scenario_params=params,
                        num_simulations=100000
                    )
                    
                    result = self._run_enhanced_algorithm_experiment(config)
                
                # Add scenario information to result
                result_dict = asdict(result)
                result_dict['scenario_name'] = scenario_name
                result_dict['scenario_type'] = scenario.get('type', 'unknown')
                
                all_results.append(result_dict)
        
        # Convert to DataFrame for analysis
        results_df = pd.DataFrame(all_results)
        
        # Save detailed results
        results_path = f"{self.output_dir}/enhanced_comparison_results.csv"
        results_df.to_csv(results_path, index=False)
        logger.info(f"Detailed results saved to {results_path}")
        
        return results_df
    
    def _run_original_algorithm_experiment(self, config: ExperimentConfig) -> ExperimentResult:
        """Run experiment with original algorithm."""
        start_time = time.time()
        
        params = config.scenario_params
        costs = []
        
        # Set random seed if provided
        if config.random_seed:
            np.random.seed(config.random_seed)
        
        # Run simulations
        for _ in range(config.num_simulations):
            alg = AdaptiveHybridRandomAlgorithm(
                b1=params['b1'], b2=params['b2'], B=params['B'],
                d1=params['d1'], d2=params['d2']
            )
            cost = alg.run()
            costs.append(cost)
        
        # Calculate optimal cost
        opt_alg = OptimalOfflineAlgorithm(
            b1=params['b1'], b2=params['b2'], B=params['B'],
            d1=params['d1'], d2=params['d2']
        )
        optimal_cost = opt_alg.run()
        
        # Statistical analysis
        avg_cost = np.mean(costs)
        std_cost = np.std(costs)
        competitive_ratio = avg_cost / optimal_cost if optimal_cost > 0 else float('inf')
        
        # Confidence interval
        confidence_interval = stats.t.interval(
            config.confidence_level,
            len(costs) - 1,
            loc=avg_cost,
            scale=stats.sem(costs)
        )
        
        # Convergence check
        convergence_achieved = self._check_convergence(costs)
        
        execution_time = time.time() - start_time
        
        return ExperimentResult(
            config=config,
            avg_cost=avg_cost,
            std_cost=std_cost,
            competitive_ratio=competitive_ratio,
            confidence_interval=confidence_interval,
            execution_time=execution_time,
            convergence_achieved=convergence_achieved,
            sample_size_used=len(costs),
            detailed_stats=self._calculate_detailed_stats(costs),
            scenario_classification=self._classify_scenario(params)
        )
    
    def _run_enhanced_algorithm_experiment(self, config: ExperimentConfig) -> ExperimentResult:
        """Run experiment with enhanced algorithm."""
        start_time = time.time()
        
        params = config.scenario_params
        alg_params = config.algorithm_params
        
        costs = []
        alpha_values = []
        performance_metrics = []
        
        # Set random seed if provided
        if config.random_seed:
            np.random.seed(config.random_seed)
        
        # Run simulations
        for _ in range(config.num_simulations):
            alg = EnhancedAdaptiveHybridAlgorithm(
                b1=params['b1'], b2=params['b2'], B=params['B'],
                d1=params['d1'], d2=params['d2'],
                **alg_params
            )
            
            result = alg.run()
            costs.append(result.cost)
            alpha_values.append(result.alpha_value)
            
            if result.confidence_metrics:
                performance_metrics.append(result.confidence_metrics)
        
        # Calculate optimal cost
        opt_cost = EnhancedAdaptiveHybridAlgorithm(
            b1=params['b1'], b2=params['b2'], B=params['B'],
            d1=params['d1'], d2=params['d2']
        ).get_optimal_offline_cost()
        
        # Statistical analysis
        avg_cost = np.mean(costs)
        std_cost = np.std(costs)
        competitive_ratio = avg_cost / opt_cost if opt_cost > 0 else float('inf')
        
        # Enhanced confidence interval using bootstrap
        confidence_interval = self._bootstrap_confidence_interval(costs, config.confidence_level)
        
        # Convergence check with enhanced criteria
        convergence_achieved = self._enhanced_convergence_check(costs, alpha_values)
        
        execution_time = time.time() - start_time
        
        # Enhanced detailed statistics
        detailed_stats = self._calculate_enhanced_stats(costs, alpha_values, performance_metrics)
        
        return ExperimentResult(
            config=config,
            avg_cost=avg_cost,
            std_cost=std_cost,
            competitive_ratio=competitive_ratio,
            confidence_interval=confidence_interval,
            execution_time=execution_time,
            convergence_achieved=convergence_achieved,
            sample_size_used=len(costs),
            detailed_stats=detailed_stats,
            scenario_classification=self._classify_scenario(params)
        )
    
    def _check_convergence(self, costs: List[float], window_size: int = 1000) -> bool:
        """Check if simulation has converged."""
        if len(costs) < 2 * window_size:
            return False
        
        # Split into two halves and compare means
        mid_point = len(costs) // 2
        first_half_mean = np.mean(costs[:mid_point])
        second_half_mean = np.mean(costs[mid_point:])
        
        # Use relative difference
        relative_diff = abs(first_half_mean - second_half_mean) / max(first_half_mean, 1e-6)
        
        return relative_diff < 0.001  # 0.1% tolerance
    
    def _enhanced_convergence_check(self, costs: List[float], alpha_values: List[float]) -> bool:
        """Enhanced convergence check considering multiple metrics."""
        if len(costs) < 2000:
            return False
        
        # Check cost convergence
        cost_convergence = self._check_convergence(costs)
        
        # Check alpha stability
        alpha_std = np.std(alpha_values)
        alpha_convergence = alpha_std < 0.01  # Small variation in alpha
        
        # Check trend stability (no significant trend in recent samples)
        recent_costs = costs[-1000:]
        slope, _, _, p_value, _ = stats.linregress(range(len(recent_costs)), recent_costs)
        trend_stable = p_value > 0.05  # No significant trend
        
        return cost_convergence and alpha_convergence and trend_stable
    
    def _bootstrap_confidence_interval(self, data: List[float], confidence_level: float) -> Tuple[float, float]:
        """Calculate bootstrap confidence interval."""
        n_bootstrap = 10000
        bootstrap_means = []
        
        for _ in range(n_bootstrap):
            bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_means.append(np.mean(bootstrap_sample))
        
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        return np.percentile(bootstrap_means, [lower_percentile, upper_percentile])
    
    def _calculate_detailed_stats(self, costs: List[float]) -> Dict[str, float]:
        """Calculate detailed statistics for costs."""
        costs_array = np.array(costs)
        
        return {
            'mean': float(np.mean(costs_array)),
            'std': float(np.std(costs_array)),
            'median': float(np.median(costs_array)),
            'q25': float(np.percentile(costs_array, 25)),
            'q75': float(np.percentile(costs_array, 75)),
            'min': float(np.min(costs_array)),
            'max': float(np.max(costs_array)),
            'skewness': float(stats.skew(costs_array)),
            'kurtosis': float(stats.kurtosis(costs_array)),
            'coefficient_of_variation': float(np.std(costs_array) / np.mean(costs_array))
        }
    
    def _calculate_enhanced_stats(self, costs: List[float], alpha_values: List[float], 
                                performance_metrics: List[Dict]) -> Dict[str, float]:
        """Calculate enhanced statistics including algorithm-specific metrics."""
        base_stats = self._calculate_detailed_stats(costs)
        
        # Alpha statistics
        alpha_stats = {
            'alpha_mean': float(np.mean(alpha_values)),
            'alpha_std': float(np.std(alpha_values)),
            'alpha_min': float(np.min(alpha_values)),
            'alpha_max': float(np.max(alpha_values))
        }
        
        # Performance metrics (if available)
        perf_stats = {}
        if performance_metrics:
            # Aggregate performance metrics
            guard_activations = [pm.get('guard_activations', 0) for pm in performance_metrics]
            decision_points = [pm.get('decision_points', 0) for pm in performance_metrics]
            
            perf_stats = {
                'avg_guard_activations': float(np.mean(guard_activations)),
                'avg_decision_points': float(np.mean(decision_points)),
                'guard_activation_rate': float(np.mean(guard_activations)) / max(np.mean(decision_points), 1)
            }
        
        return {**base_stats, **alpha_stats, **perf_stats}
    
    def _classify_scenario(self, params: Dict[str, Any]) -> str:
        """Classify scenario type for targeted analysis."""
        b1, b2, B, d1, d2 = params['b1'], params['b2'], params['B'], params['d1'], params['d2']
        
        costs = {
            'pure_rental': d1 + d2,
            'buy1_rent2': b1 + d2,
            'rent1_buy2': d1 + b2,
            'buy_both': b1 + b2,
            'buy_combo': B
        }
        
        optimal_cost = min(costs.values())
        optimal_strategies = [k for k, v in costs.items() if v == optimal_cost]
        
        if 'buy_combo' in optimal_strategies:
            return 'combo_optimal'
        elif len([s for s in optimal_strategies if 'buy' in s and s != 'buy_combo']) > 0:
            return 'individual_optimal'
        elif 'pure_rental' in optimal_strategies:
            return 'pure_rental_optimal'
        else:
            return 'mixed_optimal'
    
    def generate_comprehensive_report(self, results_df: pd.DataFrame) -> None:
        """Generate comprehensive analysis report."""
        logger.info("Generating comprehensive report...")
        
        # Summary statistics
        summary_stats = self._generate_summary_statistics(results_df)
        
        # Competitive ratio analysis
        cr_analysis = self._analyze_competitive_ratios(results_df)
        
        # Performance improvements
        improvements = self._calculate_improvements(results_df)
        
        # Statistical significance tests
        significance_tests = self._perform_significance_tests(results_df)
        
        # Generate visualizations
        self._generate_visualizations(results_df)
        
        # Compile report
        report = {
            'summary_statistics': summary_stats,
            'competitive_ratio_analysis': cr_analysis,
            'performance_improvements': improvements,
            'statistical_significance': significance_tests,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save report
        report_path = f"{self.output_dir}/comprehensive_analysis_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Comprehensive report saved to {report_path}")
        
        # Print key findings
        self._print_key_findings(report)
    
    def _generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics."""
        summary = {}
        
        for scenario in df['scenario_name'].unique():
            scenario_data = df[df['scenario_name'] == scenario]
            
            summary[scenario] = {
                'algorithms_tested': len(scenario_data),
                'best_competitive_ratio': float(scenario_data['competitive_ratio'].min()),
                'worst_competitive_ratio': float(scenario_data['competitive_ratio'].max()),
                'avg_competitive_ratio': float(scenario_data['competitive_ratio'].mean())
            }
        
        return summary
    
    def _analyze_competitive_ratios(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze competitive ratios across algorithms and scenarios."""
        analysis = {}
        
        # Overall analysis
        analysis['overall'] = {
            'best_algorithm': df.loc[df['competitive_ratio'].idxmin(), 'algorithm_name'],
            'best_competitive_ratio': float(df['competitive_ratio'].min()),
            'worst_competitive_ratio': float(df['competitive_ratio'].max()),
            'improvement_range': float(df['competitive_ratio'].max() - df['competitive_ratio'].min())
        }
        
        # By scenario type
        by_scenario = {}
        for scenario_type in df['scenario_type'].unique():
            scenario_data = df[df['scenario_type'] == scenario_type]
            
            by_scenario[scenario_type] = {
                'best_competitive_ratio': float(scenario_data['competitive_ratio'].min()),
                'best_algorithm': scenario_data.loc[scenario_data['competitive_ratio'].idxmin(), 'algorithm_name'],
                'average_improvement': float(
                    scenario_data[scenario_data['algorithm_name'].str.startswith('enhanced')]['competitive_ratio'].mean() -
                    scenario_data[scenario_data['algorithm_name'] == 'original_adaptive']['competitive_ratio'].mean()
                ) if 'original_adaptive' in scenario_data['algorithm_name'].values else None
            }
        
        analysis['by_scenario_type'] = by_scenario
        
        return analysis
    
    def _calculate_improvements(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance improvements of enhanced algorithms."""
        improvements = {}
        
        # Get original algorithm results as baseline
        original_results = df[df['algorithm_name'] == 'original_adaptive']
        enhanced_results = df[df['algorithm_name'].str.startswith('enhanced')]
        
        for scenario in original_results['scenario_name'].unique():
            orig_cr = original_results[original_results['scenario_name'] == scenario]['competitive_ratio'].iloc[0]
            
            scenario_enhanced = enhanced_results[enhanced_results['scenario_name'] == scenario]
            
            if not scenario_enhanced.empty:
                best_enhanced_cr = scenario_enhanced['competitive_ratio'].min()
                improvement = (orig_cr - best_enhanced_cr) / orig_cr * 100  # Percentage improvement
                
                improvements[scenario] = {
                    'original_cr': float(orig_cr),
                    'best_enhanced_cr': float(best_enhanced_cr),
                    'improvement_percent': float(improvement),
                    'best_enhanced_algorithm': scenario_enhanced.loc[scenario_enhanced['competitive_ratio'].idxmin(), 'algorithm_name']
                }
        
        return improvements
    
    def _perform_significance_tests(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform statistical significance tests."""
        tests = {}
        
        # Compare original vs best enhanced for each scenario
        original_results = df[df['algorithm_name'] == 'original_adaptive']
        
        for scenario in original_results['scenario_name'].unique():
            orig_data = original_results[original_results['scenario_name'] == scenario]
            enhanced_data = df[(df['scenario_name'] == scenario) & 
                             (df['algorithm_name'].str.startswith('enhanced'))]
            
            if not enhanced_data.empty:
                best_enhanced = enhanced_data.loc[enhanced_data['competitive_ratio'].idxmin()]
                
                # Extract confidence intervals for comparison
                orig_ci = orig_data['confidence_interval'].iloc[0]
                enhanced_ci = best_enhanced['confidence_interval']
                
                # Simple significance test: check if confidence intervals overlap
                overlap = not (orig_ci[1] < enhanced_ci[0] or enhanced_ci[1] < orig_ci[0])
                
                tests[scenario] = {
                    'original_ci': orig_ci,
                    'best_enhanced_ci': enhanced_ci,
                    'confidence_intervals_overlap': overlap,
                    'significant_improvement': not overlap and best_enhanced['competitive_ratio'] < orig_data['competitive_ratio'].iloc[0]
                }
        
        return tests
    
    def _generate_visualizations(self, df: pd.DataFrame) -> None:
        """Generate comprehensive visualizations."""
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        
        # 1. Competitive Ratio Comparison
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Competitive ratios by algorithm
        ax1 = axes[0, 0]
        sns.boxplot(data=df, x='algorithm_name', y='competitive_ratio', ax=ax1)
        ax1.set_title('Competitive Ratios by Algorithm')
        ax1.tick_params(axis='x', rotation=45)
        
        # Competitive ratios by scenario type
        ax2 = axes[0, 1]
        sns.boxplot(data=df, x='scenario_type', y='competitive_ratio', ax=ax2)
        ax2.set_title('Competitive Ratios by Scenario Type')
        
        # Improvement heatmap
        ax3 = axes[1, 0]
        pivot_data = df.pivot_table(values='competitive_ratio', 
                                  index='scenario_name', 
                                  columns='algorithm_name', 
                                  aggfunc='mean')
        sns.heatmap(pivot_data, annot=True, fmt='.3f', ax=ax3, cmap='RdYlBu_r')
        ax3.set_title('Competitive Ratio Heatmap')
        
        # Algorithm performance distribution
        ax4 = axes[1, 1]
        enhanced_algos = df[df['algorithm_name'].str.startswith('enhanced')]
        original_algos = df[df['algorithm_name'] == 'original_adaptive']
        
        ax4.hist(original_algos['competitive_ratio'], alpha=0.7, label='Original', bins=20)
        ax4.hist(enhanced_algos['competitive_ratio'], alpha=0.7, label='Enhanced', bins=20)
        ax4.set_xlabel('Competitive Ratio')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Performance Distribution')
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/competitive_ratio_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Detailed performance metrics
        if 'alpha_mean' in df.columns:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # Alpha values distribution
            enhanced_data = df[df['algorithm_name'].str.startswith('enhanced')]
            sns.boxplot(data=enhanced_data, x='algorithm_name', y='alpha_mean', ax=axes[0])
            axes[0].set_title('Alpha Values by Enhanced Algorithm')
            axes[0].tick_params(axis='x', rotation=45)
            
            # Performance vs Alpha
            axes[1].scatter(enhanced_data['alpha_mean'], enhanced_data['competitive_ratio'])
            axes[1].set_xlabel('Alpha Mean')
            axes[1].set_ylabel('Competitive Ratio')
            axes[1].set_title('Performance vs Alpha Value')
            
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/alpha_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        logger.info(f"Visualizations saved to {self.output_dir}/")
    
    def _print_key_findings(self, report: Dict[str, Any]) -> None:
        """Print key findings to console."""
        print("\\n" + "="*60)
        print("KEY FINDINGS - CS29 ENHANCED ALGORITHM ANALYSIS")
        print("="*60)
        
        # Overall best performance
        overall = report['competitive_ratio_analysis']['overall']
        print(f"\\nBest Overall Algorithm: {overall['best_algorithm']}")
        print(f"Best Competitive Ratio: {overall['best_competitive_ratio']:.4f}")
        print(f"Improvement Range: {overall['improvement_range']:.4f}")
        
        # Improvements by scenario
        print("\\nPerformance Improvements:")
        improvements = report['performance_improvements']
        for scenario, data in improvements.items():
            if data['improvement_percent'] > 0:
                print(f"  {scenario}: {data['improvement_percent']:.2f}% improvement")
                print(f"    Original CR: {data['original_cr']:.4f} → Enhanced CR: {data['best_enhanced_cr']:.4f}")
        
        # Statistical significance
        print("\\nStatistically Significant Improvements:")
        sig_tests = report['statistical_significance']
        for scenario, test in sig_tests.items():
            if test['significant_improvement']:
                print(f"  ✓ {scenario}")
            else:
                print(f"  ○ {scenario} (not significant)")
        
        print("\\n" + "="*60)

# Main execution function
def run_comprehensive_analysis():
    """Run the complete enhanced analysis."""
    
    # Define test scenarios
    scenarios = [
        {
            'name': 'combo_optimal_scenario',
            'type': 'combo_optimal',
            'params': {'b1': 10, 'b2': 100, 'B': 50, 'd1': 10, 'd2': 100}
        },
        {
            'name': 'individual_optimal_scenario', 
            'type': 'individual_optimal',
            'params': {'b1': 10, 'b2': 50, 'B': 100, 'd1': 20, 'd2': 60}
        },
        {
            'name': 'pure_rental_scenario',
            'type': 'pure_rental_optimal', 
            'params': {'b1': 50, 'b2': 100, 'B': 80, 'd1': 5, 'd2': 10}
        },
        {
            'name': 'mixed_scenario',
            'type': 'mixed_optimal',
            'params': {'b1': 20, 'b2': 40, 'B': 55, 'd1': 25, 'd2': 30}
        }
    ]
    
    # Algorithms to test
    algorithms = [
        'original_adaptive',
        'enhanced_multi_factor',
        'enhanced_theoretical_optimal'
    ]
    
    # Initialize framework
    framework = EnhancedExperimentalFramework()
    
    # Run comprehensive comparison
    results_df = framework.run_enhanced_comparison_study(scenarios, algorithms)
    
    # Generate comprehensive report
    framework.generate_comprehensive_report(results_df)
    
    return results_df

if __name__ == "__main__":
    # Run the analysis
    print("Starting CS29 Enhanced Algorithm Analysis...")
    results = run_comprehensive_analysis()
    print("Analysis complete. Check 'enhanced_results/' directory for detailed outputs.")