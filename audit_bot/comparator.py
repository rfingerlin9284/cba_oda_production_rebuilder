"""
Comparator
Compares repositories and generates comparison tables.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class ComparisonResult:
    """Results of cross-repository comparison"""
    performance_comparison: List[Dict[str, Any]]
    feature_matrix: List[Dict[str, Any]]
    architecture_evolution: List[Dict[str, Any]]
    component_reusability: Dict[str, Any]
    best_practices: List[Dict[str, Any]]


class Comparator:
    """Compares repositories and identifies best components"""
    
    def __init__(self):
        pass
    
    def create_performance_comparison(self, 
                                     analyses: List[Dict[str, Any]], 
                                     scores: List[Any]) -> List[Dict[str, Any]]:
        """Create performance comparison table"""
        comparison = []
        
        score_dict = {s.repo_name: s for s in scores}
        
        for analysis in analyses:
            repo_name = analysis.get('repo_name', '')
            score = score_dict.get(repo_name)
            
            # Extract performance indicators
            balance_mentions = analysis.get('balance_mentions', [])
            max_balance = 0
            for mention in balance_mentions:
                try:
                    value_str = mention.get('value', '0').replace(',', '')
                    if 'k' in value_str.lower():
                        value = float(value_str.replace('k', '').replace('K', '')) * 1000
                    else:
                        value = float(value_str)
                    max_balance = max(max_balance, value)
                except:
                    pass
            
            entry = {
                "repository": repo_name,
                "documented_balance": f"${max_balance:,.0f}" if max_balance > 0 else "N/A",
                "edge_score": round(score.total_score, 1) if score else 0,
                "rank": score.rank if score else 0,
                "brokers": ", ".join(analysis.get('brokers', set())),
                "strategies": len(analysis.get('strategies', [])),
                "maturity": ", ".join(analysis.get('maturity_tags', [])[:2]) or "Standard",
                "created_date": analysis.get('created_at', 'Unknown')[:10],
            }
            
            comparison.append(entry)
        
        # Sort by edge score
        comparison.sort(key=lambda x: x['edge_score'], reverse=True)
        
        return comparison
    
    def create_feature_matrix(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create feature comparison matrix"""
        matrix = []
        
        for analysis in analyses:
            repo_name = analysis.get('repo_name', '')
            brokers = analysis.get('brokers', set())
            strategies = analysis.get('strategies', [])
            
            entry = {
                "repository": repo_name,
                "oanda_support": "✓" if "oanda" in brokers else "✗",
                "coinbase_support": "✓" if "coinbase" in brokers else "✗",
                "multi_broker": "✓" if len(brokers) > 1 else "✗",
                "strategy_count": len(strategies),
                "ma_crossover": "✓" if any('ma' in s.lower() for s in strategies) else "✗",
                "rsi": "✓" if any('rsi' in s.lower() for s in strategies) else "✗",
                "error_handling": "✓" if analysis.get('has_error_handling') else "✗",
                "logging": "✓" if analysis.get('has_logging') else "✗",
                "tests": "✓" if analysis.get('has_tests') else "✗",
                "session_aware": "✓" if analysis.get('has_session_awareness') else "✗",
                "continuous": "✓" if analysis.get('has_continuous_trading') else "✗",
            }
            
            matrix.append(entry)
        
        return matrix
    
    def analyze_architecture_evolution(self, 
                                       analyses: List[Dict[str, Any]],
                                       metadata: List[Any]) -> List[Dict[str, Any]]:
        """Analyze how architecture evolved over time"""
        evolution = []
        
        # Sort by creation date
        metadata_dict = {m.name: m for m in metadata}
        sorted_analyses = sorted(
            analyses,
            key=lambda x: metadata_dict.get(x.get('repo_name', '')).created_at 
                         if x.get('repo_name', '') in metadata_dict else '',
        )
        
        for analysis in sorted_analyses:
            repo_name = analysis.get('repo_name', '')
            meta = metadata_dict.get(repo_name)
            
            entry = {
                "repository": repo_name,
                "created": meta.created_at[:10] if meta else "Unknown",
                "age_days": meta.age_days if meta else 0,
                "brokers": len(analysis.get('brokers', set())),
                "strategies": len(analysis.get('strategies', [])),
                "execution_harness": analysis.get('execution_harness_type', 'unknown'),
                "maturity_level": self._assess_maturity_level(analysis),
                "architectural_notes": self._extract_architectural_notes(analysis),
            }
            
            evolution.append(entry)
        
        return evolution
    
    def identify_component_reusability(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify which components are most reusable"""
        component_analysis = {
            "best_strategies": self._find_best_strategies(analyses),
            "best_brokers": self._find_best_broker_implementations(analyses),
            "best_configurations": self._find_best_configurations(analyses),
            "best_execution_harness": self._find_best_execution_harness(analyses),
            "recommended_extractions": []
        }
        
        return component_analysis
    
    def identify_best_practices(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify best practices across repositories"""
        practices = []
        
        # Error handling practices
        repos_with_error_handling = [
            a['repo_name'] for a in analyses if a.get('has_error_handling')
        ]
        if repos_with_error_handling:
            practices.append({
                "practice": "Comprehensive Error Handling",
                "repos": repos_with_error_handling[:3],
                "benefit": "Improved reliability and debugging"
            })
        
        # Multi-broker architecture
        multi_broker_repos = [
            a['repo_name'] for a in analyses if len(a.get('brokers', set())) > 1
        ]
        if multi_broker_repos:
            practices.append({
                "practice": "Multi-Broker Architecture",
                "repos": multi_broker_repos[:3],
                "benefit": "Diversification and flexibility"
            })
        
        # Session awareness
        session_aware_repos = [
            a['repo_name'] for a in analyses if a.get('has_session_awareness')
        ]
        if session_aware_repos:
            practices.append({
                "practice": "Session-Aware Trading",
                "repos": session_aware_repos[:3],
                "benefit": "Respects market hours and conditions"
            })
        
        # Comprehensive logging
        logging_repos = [
            a['repo_name'] for a in analyses if a.get('has_logging')
        ]
        if len(logging_repos) > 10:  # If majority have it
            practices.append({
                "practice": "Comprehensive Logging",
                "repos": logging_repos[:3],
                "benefit": "Better monitoring and debugging"
            })
        
        return practices
    
    def _assess_maturity_level(self, analysis: Dict[str, Any]) -> str:
        """Assess maturity level of a repository"""
        maturity_tags = analysis.get('maturity_tags', [])
        
        if 'frozen' in maturity_tags or 'golden' in maturity_tags:
            return "Frozen/Baseline"
        elif 'production' in maturity_tags or 'clean' in maturity_tags:
            return "Production"
        elif 'stable' in maturity_tags:
            return "Stable"
        else:
            return "Development"
    
    def _extract_architectural_notes(self, analysis: Dict[str, Any]) -> str:
        """Extract key architectural notes"""
        notes = []
        
        if analysis.get('has_multi_broker'):
            notes.append("Multi-broker")
        if analysis.get('has_session_awareness'):
            notes.append("Session-aware")
        if analysis.get('has_continuous_trading'):
            notes.append("Continuous")
        
        exec_harness = analysis.get('execution_harness_type', '')
        if exec_harness and exec_harness != 'unknown':
            notes.append(f"{exec_harness.split(',')[0]}")
        
        return ", ".join(notes) if notes else "Standard"
    
    def _find_best_strategies(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find best strategy implementations"""
        strategy_repos = {}
        
        for analysis in analyses:
            strategies = analysis.get('strategies', [])
            repo_name = analysis.get('repo_name', '')
            
            for strategy in strategies:
                strategy_lower = strategy.lower()
                if strategy_lower not in strategy_repos:
                    strategy_repos[strategy_lower] = []
                strategy_repos[strategy_lower].append(repo_name)
        
        best_strategies = []
        for strategy, repos in strategy_repos.items():
            best_strategies.append({
                "strategy": strategy,
                "implementations": len(repos),
                "found_in": repos[:5]  # Top 5
            })
        
        return sorted(best_strategies, key=lambda x: x['implementations'], reverse=True)
    
    def _find_best_broker_implementations(self, analyses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Find best broker implementations"""
        broker_repos = {
            "oanda": [],
            "coinbase": []
        }
        
        for analysis in analyses:
            brokers = analysis.get('brokers', set())
            repo_name = analysis.get('repo_name', '')
            
            if "oanda" in brokers:
                broker_repos["oanda"].append(repo_name)
            if "coinbase" in brokers:
                broker_repos["coinbase"].append(repo_name)
        
        return broker_repos
    
    def _find_best_configurations(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find repositories with best configuration practices"""
        config_repos = []
        
        for analysis in analyses:
            config_files = analysis.get('config_files', [])
            repo_name = analysis.get('repo_name', '')
            
            if len(config_files) > 0:
                config_repos.append({
                    "repository": repo_name,
                    "config_count": len(config_files),
                    "files": config_files[:3]
                })
        
        return sorted(config_repos, key=lambda x: x['config_count'], reverse=True)[:10]
    
    def _find_best_execution_harness(self, analyses: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Find repositories by execution harness type"""
        harness_types = {}
        
        for analysis in analyses:
            harness = analysis.get('execution_harness_type', 'unknown')
            repo_name = analysis.get('repo_name', '')
            
            if harness not in harness_types:
                harness_types[harness] = []
            harness_types[harness].append(repo_name)
        
        return harness_types
