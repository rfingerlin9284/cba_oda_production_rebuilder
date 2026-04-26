"""
Edge Scorer
Scores repositories based on trading edge, code quality, and maturity.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import re


@dataclass
class EdgeScore:
    """Comprehensive edge score for a repository"""
    repo_name: str
    
    # Individual scores (0-100)
    documented_performance_score: float = 0.0
    code_quality_score: float = 0.0
    feature_completeness_score: float = 0.0
    maturity_score: float = 0.0
    documentation_score: float = 0.0
    
    # Weighted total (0-100)
    total_score: float = 0.0
    
    # Rankings
    rank: int = 0
    percentile: float = 0.0
    
    # Details
    performance_notes: List[str] = None
    quality_notes: List[str] = None
    maturity_notes: List[str] = None
    
    def __post_init__(self):
        if self.performance_notes is None:
            self.performance_notes = []
        if self.quality_notes is None:
            self.quality_notes = []
        if self.maturity_notes is None:
            self.maturity_notes = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "repo_name": self.repo_name,
            "scores": {
                "documented_performance": round(self.documented_performance_score, 2),
                "code_quality": round(self.code_quality_score, 2),
                "feature_completeness": round(self.feature_completeness_score, 2),
                "maturity": round(self.maturity_score, 2),
                "documentation": round(self.documentation_score, 2),
                "total": round(self.total_score, 2),
            },
            "ranking": {
                "rank": self.rank,
                "percentile": round(self.percentile, 2)
            },
            "notes": {
                "performance": self.performance_notes,
                "quality": self.quality_notes,
                "maturity": self.maturity_notes,
            }
        }


class EdgeScorer:
    """Scores repositories for trading edge"""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "documented_performance": 0.30,
            "code_quality": 0.20,
            "feature_completeness": 0.25,
            "maturity_signals": 0.15,
            "documentation": 0.10
        }
    
    def score_documented_performance(self, analysis: Dict[str, Any]) -> tuple[float, List[str]]:
        """Score based on documented performance (0-100)"""
        score = 0.0
        notes = []
        
        # Check for explicit performance mentions
        balance_mentions = analysis.get('balance_mentions', [])
        if balance_mentions:
            # Look for high balance numbers
            max_balance = 0
            for mention in balance_mentions:
                try:
                    value_str = mention.get('value', '0').replace(',', '')
                    # Handle "7k" format
                    if 'k' in value_str.lower():
                        value = float(value_str.replace('k', '').replace('K', '')) * 1000
                    else:
                        value = float(value_str)
                    max_balance = max(max_balance, value)
                except:
                    pass
            
            if max_balance >= 7000:
                score += 50
                notes.append(f"High documented balance: ${max_balance:,.0f}")
            elif max_balance >= 5000:
                score += 40
                notes.append(f"Good balance: ${max_balance:,.0f}")
            elif max_balance >= 3000:
                score += 30
                notes.append(f"Moderate balance: ${max_balance:,.0f}")
            elif max_balance > 0:
                score += 20
                notes.append(f"Some balance tracking: ${max_balance:,.0f}")
        
        # Check for performance-related files
        perf_files = analysis.get('performance_files', [])
        if any('freeze' in f.lower() for f in perf_files):
            score += 20
            notes.append("Has freeze manifest (performance snapshot)")
        
        if any('metric' in f.lower() or 'result' in f.lower() for f in perf_files):
            score += 10
            notes.append("Has metrics/results tracking")
        
        # Check repo name/description for performance indicators
        repo_name = analysis.get('repo_name', '').lower()
        description = analysis.get('description', '').lower()
        
        if 'edge' in repo_name or 'edge' in description:
            score += 10
            notes.append("Explicitly mentions 'edge' in name/description")
        
        if 'green' in repo_name or 'green' in description:
            score += 5
            notes.append("References 'green day' (profitable)")
        
        return min(score, 100.0), notes
    
    def score_code_quality(self, analysis: Dict[str, Any]) -> tuple[float, List[str]]:
        """Score code quality indicators (0-100)"""
        score = 0.0
        notes = []
        
        # Error handling
        if analysis.get('has_error_handling', False):
            score += 25
            notes.append("Has error handling (try/except)")
        
        # Logging
        if analysis.get('has_logging', False):
            score += 25
            notes.append("Has logging infrastructure")
        
        # Testing
        if analysis.get('has_tests', False):
            score += 20
            notes.append("Has test suite")
        
        # Configuration management
        config_files = analysis.get('config_files', [])
        if len(config_files) > 0:
            score += 15
            notes.append(f"Has {len(config_files)} configuration file(s)")
        
        # Code organization (multiple modules)
        strategies = analysis.get('strategies', [])
        if len(strategies) > 1:
            score += 10
            notes.append(f"Multiple strategies ({len(strategies)})")
        
        # API client abstraction
        if any('client' in str(f).lower() for f in config_files):
            score += 5
            notes.append("Has API client abstraction")
        
        return min(score, 100.0), notes
    
    def score_feature_completeness(self, analysis: Dict[str, Any]) -> tuple[float, List[str]]:
        """Score feature completeness (0-100)"""
        score = 0.0
        notes = []
        
        # Broker support
        brokers = analysis.get('brokers', set())
        broker_count = len(brokers)
        if broker_count >= 2:
            score += 30
            notes.append(f"Multi-broker support ({', '.join(brokers)})")
        elif broker_count == 1:
            score += 20
            notes.append(f"Single broker ({list(brokers)[0]})")
        
        # Strategy count
        strategies = analysis.get('strategies', [])
        strategy_count = len(strategies)
        if strategy_count >= 3:
            score += 25
            notes.append(f"Multiple strategies ({strategy_count})")
        elif strategy_count >= 2:
            score += 20
            notes.append(f"Two strategies")
        elif strategy_count >= 1:
            score += 10
            notes.append(f"Single strategy")
        
        # Risk management
        risk_features = analysis.get('risk_management', [])
        if risk_features:
            score += 15
            notes.append(f"Risk management features ({len(risk_features)})")
        
        # Session awareness
        if analysis.get('has_session_awareness', False):
            score += 10
            notes.append("Session-aware trading")
        
        # Continuous vs scheduled
        if analysis.get('has_continuous_trading', False):
            score += 10
            notes.append("Continuous trading capability")
        
        # Notification/alerting
        if any('notif' in str(f).lower() or 'alert' in str(f).lower() 
               for f in analysis.get('config_files', [])):
            score += 10
            notes.append("Has notification/alert system")
        
        return min(score, 100.0), notes
    
    def score_maturity(self, analysis: Dict[str, Any]) -> tuple[float, List[str]]:
        """Score maturity signals (0-100)"""
        score = 0.0
        notes = []
        
        # Maturity tags
        maturity_tags = analysis.get('maturity_tags', [])
        tag_scores = {
            'frozen': 25,
            'production': 20,
            'stable': 15,
            'clean': 15,
            'golden': 15,
            'locked': 10,
        }
        
        for tag in maturity_tags:
            tag_lower = tag.lower()
            if tag_lower in tag_scores:
                score += tag_scores[tag_lower]
                notes.append(f"Tagged as '{tag}'")
        
        # Explicit freeze/production indicators
        if analysis.get('is_frozen', False):
            score += 20
            notes.append("Explicitly frozen (no active development)")
        
        if analysis.get('is_production_ready', False):
            score += 15
            notes.append("Marked as production-ready")
        
        # Installation automation
        config_files = analysis.get('config_files', [])
        if any('install' in str(f).lower() or 'setup' in str(f).lower() 
               for f in config_files):
            score += 10
            notes.append("Has automated installation")
        
        # Comprehensive documentation
        doc_score = analysis.get('documentation_score', 0)
        if doc_score >= 80:
            score += 15
            notes.append("Comprehensive documentation")
        elif doc_score >= 50:
            score += 10
            notes.append("Good documentation")
        
        return min(score, 100.0), notes
    
    def calculate_total_score(self, edge_score: EdgeScore) -> float:
        """Calculate weighted total score"""
        total = (
            edge_score.documented_performance_score * self.weights['documented_performance'] +
            edge_score.code_quality_score * self.weights['code_quality'] +
            edge_score.feature_completeness_score * self.weights['feature_completeness'] +
            edge_score.maturity_score * self.weights['maturity_signals'] +
            edge_score.documentation_score * self.weights['documentation']
        )
        return total
    
    def score_repository(self, analysis: Dict[str, Any]) -> EdgeScore:
        """Score a single repository"""
        repo_name = analysis.get('repo_name', 'unknown')
        
        edge_score = EdgeScore(repo_name=repo_name)
        
        # Score individual components
        edge_score.documented_performance_score, edge_score.performance_notes = \
            self.score_documented_performance(analysis)
        
        edge_score.code_quality_score, edge_score.quality_notes = \
            self.score_code_quality(analysis)
        
        edge_score.feature_completeness_score, _ = \
            self.score_feature_completeness(analysis)
        
        edge_score.maturity_score, edge_score.maturity_notes = \
            self.score_maturity(analysis)
        
        edge_score.documentation_score = analysis.get('documentation_score', 0)
        
        # Calculate total
        edge_score.total_score = self.calculate_total_score(edge_score)
        
        return edge_score
    
    def rank_scores(self, scores: List[EdgeScore]) -> List[EdgeScore]:
        """Rank scores and assign percentiles"""
        # Sort by total score (descending)
        sorted_scores = sorted(scores, key=lambda x: x.total_score, reverse=True)
        
        # Assign ranks and percentiles
        total_count = len(sorted_scores)
        for i, score in enumerate(sorted_scores):
            score.rank = i + 1
            score.percentile = 100.0 * (total_count - i) / total_count
        
        return sorted_scores
