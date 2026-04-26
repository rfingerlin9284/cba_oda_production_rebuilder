"""
Code Analyzer
Analyzes repository structure, configuration files, and trading components.
"""

import re
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
import json


@dataclass
class RepositoryAnalysis:
    """Complete analysis of a single repository"""
    repo_name: str
    
    # Configuration
    config_files: List[str] = field(default_factory=list)
    env_variables: Dict[str, str] = field(default_factory=dict)
    
    # Performance indicators
    performance_files: List[str] = field(default_factory=list)
    balance_mentions: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Trading components
    strategies: List[str] = field(default_factory=list)
    brokers: Set[str] = field(default_factory=set)
    risk_management: List[str] = field(default_factory=list)
    
    # Architecture
    has_multi_broker: bool = False
    has_session_awareness: bool = False
    has_continuous_trading: bool = False
    execution_harness_type: Optional[str] = None
    
    # Code quality
    has_logging: bool = False
    has_error_handling: bool = False
    has_tests: bool = False
    documentation_score: int = 0
    
    # Maturity signals
    maturity_tags: List[str] = field(default_factory=list)
    is_frozen: bool = False
    is_production_ready: bool = False


class CodeAnalyzer:
    """Analyzes code structure and components"""
    
    def __init__(self):
        self.performance_patterns = [
            r'balance.*?(\d+[\d,]*\.?\d*)',
            r'profit.*?(\d+[\d,]*\.?\d*)',
            r'capital.*?(\d+[\d,]*\.?\d*)',
            r'\$\s*(\d+[\d,]*\.?\d*)k',
            r'NAV.*?(\d+[\d,]*\.?\d*)',
        ]
        
        self.strategy_patterns = [
            r'ma_crossover',
            r'rsi.*?reversion',
            r'ema.*?cross',
            r'bollinger',
            r'macd',
            r'momentum',
        ]
        
    def analyze_file_content(self, filepath: str, content: str) -> Dict[str, Any]:
        """Analyze a single file's content"""
        analysis = {
            "file": filepath,
            "strategies": [],
            "brokers": [],
            "performance_mentions": [],
            "config_items": [],
            "has_error_handling": False,
            "has_logging": False,
        }
        
        # Detect strategies
        for pattern in self.strategy_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                analysis["strategies"].append(pattern)
        
        # Detect brokers
        if re.search(r'oanda', content, re.IGNORECASE):
            analysis["brokers"].append("oanda")
        if re.search(r'coinbase|cba', content, re.IGNORECASE):
            analysis["brokers"].append("coinbase")
        
        # Detect performance mentions
        for pattern in self.performance_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                analysis["performance_mentions"].append({
                    "value": match.group(1) if match.groups() else match.group(0),
                    "context": content[max(0, match.start()-50):min(len(content), match.end()+50)]
                })
        
        # Detect code quality indicators
        if re.search(r'try:|except:|catch', content):
            analysis["has_error_handling"] = True
        if re.search(r'logger\.|logging\.|log\(', content):
            analysis["has_logging"] = True
        
        return analysis
    
    def analyze_readme(self, content: str) -> Dict[str, Any]:
        """Special analysis for README files"""
        analysis = {
            "has_installation": bool(re.search(r'install|setup', content, re.IGNORECASE)),
            "has_usage": bool(re.search(r'usage|how to|running', content, re.IGNORECASE)),
            "has_api_docs": bool(re.search(r'api|endpoint|credentials', content, re.IGNORECASE)),
            "maturity_indicators": [],
            "performance_claims": [],
        }
        
        # Maturity indicators
        maturity_keywords = ['frozen', 'production', 'stable', 'clean', 'golden', 'locked']
        for keyword in maturity_keywords:
            if re.search(rf'\b{keyword}\b', content, re.IGNORECASE):
                analysis["maturity_indicators"].append(keyword)
        
        # Extract performance claims
        for pattern in self.performance_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                analysis["performance_claims"].append({
                    "value": match.group(1) if match.groups() else match.group(0),
                    "context": content[max(0, match.start()-100):min(len(content), match.end()+100)]
                })
        
        return analysis
    
    def detect_execution_harness(self, files: List[Dict[str, str]]) -> str:
        """Detect the type of execution harness used"""
        patterns = {
            "continuous_polling": r'while\s+True.*?sleep|poll.*?interval',
            "scheduled_cron": r'cron|schedule|@scheduled',
            "event_driven": r'webhook|event.*?handler|on_.*?event',
            "tmux_background": r'tmux|screen|daemon',
        }
        
        detected = []
        for file_info in files:
            content = file_info.get('content', '')
            for harness_type, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    detected.append(harness_type)
        
        if detected:
            return ", ".join(set(detected))
        return "unknown"
    
    def score_documentation(self, files: List[str], readme_analysis: Dict) -> int:
        """Score documentation completeness (0-100)"""
        score = 0
        
        # README quality
        if readme_analysis.get("has_installation"):
            score += 20
        if readme_analysis.get("has_usage"):
            score += 20
        if readme_analysis.get("has_api_docs"):
            score += 10
        
        # Additional docs
        doc_patterns = ['PHASE', 'TROUBLESHOOTING', 'CHANGELOG', 'SETUP', 'GUIDE']
        for pattern in doc_patterns:
            if any(pattern.lower() in f.lower() for f in files):
                score += 10
        
        return min(score, 100)
    
    def extract_strategy_details(self, strategy_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract detailed information about trading strategies"""
        strategies = []
        
        for file_info in strategy_files:
            content = file_info.get('content', '')
            filepath = file_info.get('path', '')
            
            strategy_info = {
                "file": filepath,
                "name": self._extract_strategy_name(filepath, content),
                "indicators": self._extract_indicators(content),
                "entry_conditions": self._extract_conditions(content, "buy|long|enter"),
                "exit_conditions": self._extract_conditions(content, "sell|short|exit|close"),
                "parameters": self._extract_parameters(content),
            }
            
            strategies.append(strategy_info)
        
        return strategies
    
    def _extract_strategy_name(self, filepath: str, content: str) -> str:
        """Extract strategy name from file or content"""
        # Try from filename
        if 'ma_crossover' in filepath.lower():
            return "MA Crossover"
        if 'rsi' in filepath.lower():
            return "RSI Mean Reversion"
        
        # Try from class name
        class_match = re.search(r'class\s+(\w+Strategy)', content)
        if class_match:
            return class_match.group(1)
        
        return "Unknown Strategy"
    
    def _extract_indicators(self, content: str) -> List[str]:
        """Extract technical indicators used"""
        indicators = []
        indicator_patterns = {
            'EMA': r'ema|exponential.*?moving',
            'SMA': r'sma|simple.*?moving',
            'RSI': r'rsi|relative.*?strength',
            'MACD': r'macd',
            'Bollinger': r'bollinger|bbands',
            'ATR': r'atr|average.*?true.*?range',
        }
        
        for name, pattern in indicator_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                indicators.append(name)
        
        return indicators
    
    def _extract_conditions(self, content: str, pattern: str) -> List[str]:
        """Extract trading conditions (entry/exit)"""
        conditions = []
        matches = re.finditer(rf'(if.*?{pattern}.*?:)', content, re.IGNORECASE | re.MULTILINE)
        for match in matches[:5]:  # Limit to first 5
            conditions.append(match.group(1).strip())
        
        return conditions
    
    def _extract_parameters(self, content: str) -> Dict[str, Any]:
        """Extract strategy parameters"""
        params = {}
        
        # Look for common parameter patterns
        param_patterns = [
            r'(\w+_period)\s*=\s*(\d+)',
            r'(\w+_threshold)\s*=\s*([\d.]+)',
            r'fast\s*=\s*(\d+)',
            r'slow\s*=\s*(\d+)',
        ]
        
        for pattern in param_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    params[match.group(1)] = match.group(2)
                elif len(match.groups()) == 1:
                    params[pattern.split('=')[0].strip()] = match.group(1)
        
        return params
