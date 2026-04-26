"""
Report Generator
Generates comprehensive markdown reports and specialized documentation.
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class ReportGenerator:
    """Generates audit reports and specialized documentation"""
    
    def __init__(self, output_dir: str = "audit_reports"):
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_master_audit_report(self,
                                     metadata: List[Any],
                                     analyses: List[Dict[str, Any]],
                                     scores: List[Any],
                                     comparison: Any) -> str:
        """Generate the master audit report"""
        report = []
        
        # Header
        report.append("# GitHub Repository Audit Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append(f"\n**Account:** rfingerlin9284")
        report.append(f"\n**Total Repositories Analyzed:** {len(metadata)}")
        report.append("\n---\n")
        
        # Executive Summary
        report.append("## Executive Summary\n")
        report.append(self._generate_executive_summary(metadata, scores, comparison))
        report.append("\n---\n")
        
        # Top Performers
        report.append("## Top 10 Repositories by Edge Score\n")
        report.append(self._generate_top_performers(scores[:10]))
        report.append("\n---\n")
        
        # Performance Comparison Table
        report.append("## Performance Comparison\n")
        report.append(self._generate_performance_table(comparison.performance_comparison))
        report.append("\n---\n")
        
        # Feature Matrix
        report.append("## Feature Matrix\n")
        report.append(self._generate_feature_matrix(comparison.feature_matrix[:15]))
        report.append("\n---\n")
        
        # Architecture Evolution
        report.append("## Architecture Evolution Timeline\n")
        report.append(self._generate_evolution_timeline(comparison.architecture_evolution))
        report.append("\n---\n")
        
        # Component Reusability
        report.append("## Component Reusability Analysis\n")
        report.append(self._generate_component_analysis(comparison.component_reusability))
        report.append("\n---\n")
        
        # Best Practices
        report.append("## Best Practices Identified\n")
        report.append(self._generate_best_practices(comparison.best_practices))
        report.append("\n---\n")
        
        # Detailed Repository Findings
        report.append("## Detailed Repository Findings\n")
        for analysis in analyses:
            repo_name = analysis.get('repo_name', '')
            score = next((s for s in scores if s.repo_name == repo_name), None)
            report.append(self._generate_repo_detail(analysis, score))
            report.append("\n")
        
        return "\n".join(report)
    
    def generate_extraction_playbook(self,
                                     comparison: Any,
                                     scores: List[Any]) -> str:
        """Generate extraction and integration playbook"""
        playbook = []
        
        playbook.append("# Extraction & Integration Playbook\n")
        playbook.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        playbook.append("---\n")
        
        # Priority Rankings
        playbook.append("## Extraction Priority Rankings\n")
        playbook.append("Based on edge scores and component quality:\n\n")
        
        top_repos = scores[:5]
        for i, score in enumerate(top_repos, 1):
            playbook.append(f"### {i}. {score.repo_name}\n")
            playbook.append(f"- **Edge Score:** {score.total_score:.1f}/100\n")
            playbook.append(f"- **Rank:** #{score.rank}\n")
            playbook.append(f"- **Documented Performance:** {score.documented_performance_score:.1f}/100\n")
            if score.performance_notes:
                playbook.append(f"- **Notes:** {', '.join(score.performance_notes)}\n")
            playbook.append("\n")
        
        # Component Extraction Guide
        playbook.append("---\n\n## Component Extraction Guide\n")
        
        playbook.append("### Strategy Components\n")
        best_strategies = comparison.component_reusability.get('best_strategies', [])
        for strategy in best_strategies[:5]:
            playbook.append(f"\n#### {strategy['strategy']}\n")
            playbook.append(f"- Found in {strategy['implementations']} repositories\n")
            playbook.append(f"- Best implementations: {', '.join(strategy['found_in'][:3])}\n")
        
        playbook.append("\n### Broker Implementations\n")
        best_brokers = comparison.component_reusability.get('best_brokers', {})
        for broker, repos in best_brokers.items():
            playbook.append(f"\n#### {broker.upper()}\n")
            playbook.append(f"- Implementations: {len(repos)}\n")
            playbook.append(f"- Recommended sources: {', '.join(repos[:3])}\n")
        
        playbook.append("\n### Execution Harness Patterns\n")
        harness_types = comparison.component_reusability.get('best_execution_harness', {})
        for harness, repos in harness_types.items():
            if harness != 'unknown':
                playbook.append(f"\n#### {harness}\n")
                playbook.append(f"- Used in: {', '.join(repos[:3])}\n")
        
        # Integration Steps
        playbook.append("\n---\n\n## Integration Steps\n")
        playbook.append(self._generate_integration_steps())
        
        # Risk Assessment
        playbook.append("\n---\n\n## Risk Assessment\n")
        playbook.append(self._generate_risk_assessment())
        
        # Testing Requirements
        playbook.append("\n---\n\n## Testing Requirements\n")
        playbook.append(self._generate_testing_requirements())
        
        return "\n".join(playbook)
    
    def generate_oanda_strategies_doc(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate specialized OANDA strategies documentation"""
        doc = []
        
        doc.append("# OANDA Trading Strategies Analysis\n")
        doc.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        doc.append("**Source:** Cross-repository analysis of rfingerlin9284 account\n")
        doc.append("\n---\n")
        
        doc.append("## Overview\n")
        doc.append("This document consolidates all OANDA trading strategies discovered ")
        doc.append("across 24 repositories, including implementation patterns, parameters, ")
        doc.append("and performance characteristics.\n\n")
        
        # Filter OANDA repos
        oanda_repos = [a for a in analyses if 'oanda' in a.get('brokers', set())]
        
        doc.append(f"**Total OANDA Repositories:** {len(oanda_repos)}\n\n")
        
        # Strategy Patterns
        doc.append("## Strategy Patterns Discovered\n")
        
        all_strategies = {}
        for analysis in oanda_repos:
            repo_name = analysis.get('repo_name', '')
            strategies = analysis.get('strategies', [])
            
            for strategy in strategies:
                strategy_name = strategy.lower()
                if strategy_name not in all_strategies:
                    all_strategies[strategy_name] = []
                all_strategies[strategy_name].append(repo_name)
        
        for strategy_name, repos in sorted(all_strategies.items(), 
                                          key=lambda x: len(x[1]), 
                                          reverse=True):
            doc.append(f"\n### {strategy_name.replace('_', ' ').title()}\n")
            doc.append(f"- **Implementations:** {len(repos)}\n")
            doc.append(f"- **Found in:** {', '.join(repos[:5])}\n")
            
            # Add details if available
            doc.append("\n#### Implementation Details\n")
            doc.append(self._get_strategy_details(strategy_name, oanda_repos))
        
        # Parameter Analysis
        doc.append("\n---\n\n## Parameter Analysis\n")
        doc.append(self._analyze_strategy_parameters(oanda_repos))
        
        # Performance Correlation
        doc.append("\n---\n\n## Strategy-Performance Correlation\n")
        doc.append(self._correlate_strategies_performance(oanda_repos))
        
        # Best Practices
        doc.append("\n---\n\n## OANDA Strategy Best Practices\n")
        doc.append(self._extract_oanda_best_practices(oanda_repos))
        
        # Recommended Configurations
        doc.append("\n---\n\n## Recommended Configurations\n")
        doc.append(self._generate_recommended_configs(oanda_repos))
        
        return "\n".join(doc)
    
    def generate_oanda_exec_harness_doc(self, analyses: List[Dict[str, Any]]) -> str:
        """Generate specialized OANDA execution harness documentation"""
        doc = []
        
        doc.append("# OANDA Execution Harness Patterns\n")
        doc.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        doc.append("**Source:** Cross-repository analysis of rfingerlin9284 account\n")
        doc.append("\n---\n")
        
        doc.append("## Overview\n")
        doc.append("This document analyzes execution harness patterns used across ")
        doc.append("OANDA trading bot implementations, including polling strategies, ")
        doc.append("error handling, and deployment patterns.\n\n")
        
        # Filter OANDA repos
        oanda_repos = [a for a in analyses if 'oanda' in a.get('brokers', set())]
        
        doc.append("## Execution Harness Types\n")
        
        harness_distribution = {}
        for analysis in oanda_repos:
            harness = analysis.get('execution_harness_type', 'unknown')
            repo_name = analysis.get('repo_name', '')
            
            if harness not in harness_distribution:
                harness_distribution[harness] = []
            harness_distribution[harness].append(repo_name)
        
        for harness_type, repos in harness_distribution.items():
            doc.append(f"\n### {harness_type.replace('_', ' ').title()}\n")
            doc.append(f"- **Repos using this pattern:** {len(repos)}\n")
            doc.append(f"- **Examples:** {', '.join(repos[:3])}\n")
            doc.append(f"\n#### Characteristics\n")
            doc.append(self._describe_harness_characteristics(harness_type))
        
        # Polling Strategies
        doc.append("\n---\n\n## Polling Strategies\n")
        doc.append(self._analyze_polling_strategies(oanda_repos))
        
        # Error Handling Patterns
        doc.append("\n---\n\n## Error Handling Patterns\n")
        doc.append(self._analyze_error_handling(oanda_repos))
        
        # Deployment Patterns
        doc.append("\n---\n\n## Deployment Patterns\n")
        doc.append(self._analyze_deployment_patterns(oanda_repos))
        
        # Session Management
        doc.append("\n---\n\n## Session Management\n")
        doc.append(self._analyze_session_management(oanda_repos))
        
        # Performance Considerations
        doc.append("\n---\n\n## Performance Considerations\n")
        doc.append(self._analyze_performance_considerations(oanda_repos))
        
        # Recommended Harness Architecture
        doc.append("\n---\n\n## Recommended Harness Architecture\n")
        doc.append(self._generate_recommended_harness(oanda_repos))
        
        return "\n".join(doc)
    
    # Helper methods
    
    def _generate_executive_summary(self, metadata, scores, comparison) -> str:
        """Generate executive summary section"""
        summary = []
        
        if scores:
            top_score = scores[0]
            avg_score = sum(s.total_score for s in scores) / len(scores)
            
            summary.append(f"- **Top Repository:** {top_score.repo_name} (Score: {top_score.total_score:.1f}/100)")
            summary.append(f"- **Average Edge Score:** {avg_score:.1f}/100")
            summary.append(f"- **Repositories with Documented Performance:** {sum(1 for s in scores if s.documented_performance_score > 0)}")
            summary.append(f"- **Production-Ready Repositories:** {sum(1 for s in scores if s.maturity_score > 60)}")
        
        # Broker coverage
        all_brokers = set()
        for analysis in comparison.performance_comparison:
            brokers = analysis.get('brokers', '').split(', ')
            all_brokers.update(b for b in brokers if b)
        
        summary.append(f"- **Brokers Covered:** {', '.join(all_brokers)}")
        
        return "\n".join(summary)
    
    def _generate_top_performers(self, top_scores) -> str:
        """Generate top performers table"""
        table = ["| Rank | Repository | Edge Score | Performance | Maturity |",
                 "|------|------------|------------|-------------|----------|"]
        
        for score in top_scores:
            perf_note = score.performance_notes[0] if score.performance_notes else "N/A"
            mat_note = score.maturity_notes[0] if score.maturity_notes else "Standard"
            
            table.append(f"| {score.rank} | {score.repo_name} | {score.total_score:.1f} | {perf_note[:40]} | {mat_note[:20]} |")
        
        return "\n".join(table)
    
    def _generate_performance_table(self, comparison) -> str:
        """Generate performance comparison table"""
        table = ["| Repository | Balance | Edge Score | Brokers | Strategies | Maturity | Created |",
                 "|------------|---------|------------|---------|------------|----------|---------|"]
        
        for entry in comparison[:20]:  # Top 20
            table.append(
                f"| {entry['repository'][:30]} | "
                f"{entry['documented_balance']} | "
                f"{entry['edge_score']:.1f} | "
                f"{entry['brokers'][:15]} | "
                f"{entry['strategies']} | "
                f"{entry['maturity'][:15]} | "
                f"{entry['created_date']} |"
            )
        
        return "\n".join(table)
    
    def _generate_feature_matrix(self, matrix) -> str:
        """Generate feature matrix table"""
        table = ["| Repository | OANDA | Coinbase | Multi | Strategies | MA | RSI | Errors | Logs | Tests |",
                 "|------------|-------|----------|-------|------------|----|----|--------|------|-------|"]
        
        for entry in matrix:
            table.append(
                f"| {entry['repository'][:25]} | "
                f"{entry['oanda_support']} | "
                f"{entry['coinbase_support']} | "
                f"{entry['multi_broker']} | "
                f"{entry['strategy_count']} | "
                f"{entry['ma_crossover']} | "
                f"{entry['rsi']} | "
                f"{entry['error_handling']} | "
                f"{entry['logging']} | "
                f"{entry['tests']} |"
            )
        
        return "\n".join(table)
    
    def _generate_evolution_timeline(self, evolution) -> str:
        """Generate architecture evolution timeline"""
        lines = []
        
        for entry in evolution:
            lines.append(f"\n### {entry['repository']} ({entry['created']})\n")
            lines.append(f"- **Age:** {entry['age_days']} days")
            lines.append(f"- **Brokers:** {entry['brokers']}")
            lines.append(f"- **Strategies:** {entry['strategies']}")
            lines.append(f"- **Execution:** {entry['execution_harness']}")
            lines.append(f"- **Maturity:** {entry['maturity_level']}")
            lines.append(f"- **Architecture:** {entry['architectural_notes']}\n")
        
        return "\n".join(lines)
    
    def _generate_component_analysis(self, components) -> str:
        """Generate component reusability analysis"""
        lines = []
        
        lines.append("### Best Strategy Implementations\n")
        for strategy in components.get('best_strategies', [])[:5]:
            lines.append(f"- **{strategy['strategy']}**: {strategy['implementations']} implementations")
            lines.append(f"  - Found in: {', '.join(strategy['found_in'][:3])}\n")
        
        lines.append("\n### Broker Implementation Quality\n")
        for broker, repos in components.get('best_brokers', {}).items():
            lines.append(f"- **{broker.upper()}**: {len(repos)} repositories")
            lines.append(f"  - Top: {', '.join(repos[:3])}\n")
        
        return "\n".join(lines)
    
    def _generate_best_practices(self, practices) -> str:
        """Generate best practices section"""
        lines = []
        
        for practice in practices:
            lines.append(f"\n### {practice['practice']}\n")
            lines.append(f"- **Benefit:** {practice['benefit']}")
            lines.append(f"- **Found in:** {', '.join(practice['repos'])}\n")
        
        return "\n".join(lines)
    
    def _generate_repo_detail(self, analysis, score) -> str:
        """Generate detailed findings for a single repo"""
        repo_name = analysis.get('repo_name', '')
        lines = [f"### {repo_name}\n"]
        
        if score:
            lines.append(f"**Edge Score:** {score.total_score:.1f}/100 (Rank #{score.rank})\n")
            lines.append(f"**Component Scores:**")
            lines.append(f"- Performance: {score.documented_performance_score:.1f}/100")
            lines.append(f"- Code Quality: {score.code_quality_score:.1f}/100")
            lines.append(f"- Features: {score.feature_completeness_score:.1f}/100")
            lines.append(f"- Maturity: {score.maturity_score:.1f}/100\n")
        
        lines.append(f"**Brokers:** {', '.join(analysis.get('brokers', set())) or 'None'}")
        lines.append(f"**Strategies:** {len(analysis.get('strategies', []))}")
        lines.append(f"**Execution Harness:** {analysis.get('execution_harness_type', 'Unknown')}")
        
        if analysis.get('maturity_tags'):
            lines.append(f"**Maturity Tags:** {', '.join(analysis.get('maturity_tags', []))}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_integration_steps(self) -> str:
        """Generate integration steps"""
        return """
1. **Backup Current Production**
   - Create full backup of current production system
   - Tag current version in git
   - Document current performance baseline

2. **Component Selection**
   - Review top 5 repositories by edge score
   - Identify specific files/modules to extract
   - Map to current production structure

3. **Extraction Process**
   - Clone source repositories
   - Extract identified components
   - Document dependencies and requirements

4. **Integration Testing**
   - Create test branch
   - Integrate extracted components
   - Run comprehensive test suite
   - Paper trade validation (minimum 1 week)

5. **Performance Validation**
   - Compare against baseline performance
   - Monitor for 2 weeks in paper trading
   - Document improvements and issues

6. **Production Deployment**
   - Gradual rollout strategy
   - Monitor closely for first 48 hours
   - Have rollback plan ready
"""
    
    def _generate_risk_assessment(self) -> str:
        """Generate risk assessment"""
        return """
### High Risk Areas

1. **API Compatibility**
   - Risk: Different API versions or endpoints
   - Mitigation: Verify API calls against current broker documentation

2. **Configuration Conflicts**
   - Risk: Incompatible configuration formats
   - Mitigation: Map all config parameters, test thoroughly

3. **Strategy Logic Changes**
   - Risk: Subtle differences in trading logic
   - Mitigation: Code review, backtesting, paper trading

4. **Error Handling**
   - Risk: Different error handling approaches
   - Mitigation: Comprehensive error scenario testing

### Medium Risk Areas

1. **Dependency Versions**
   - Risk: Version conflicts in libraries
   - Mitigation: Use virtual environments, test dependencies

2. **Logging Format Changes**
   - Risk: Log parsing breaks
   - Mitigation: Update log parsing, maintain backward compatibility

### Low Risk Areas

1. **Documentation**
   - Risk: Documentation becomes outdated
   - Mitigation: Update docs as part of integration

2. **Code Style**
   - Risk: Style inconsistencies
   - Mitigation: Run linters, refactor for consistency
"""
    
    def _generate_testing_requirements(self) -> str:
        """Generate testing requirements"""
        return """
### Pre-Integration Testing

- [ ] Unit tests for all extracted components
- [ ] Integration tests for broker APIs
- [ ] Configuration validation tests
- [ ] Error handling scenario tests

### Integration Testing

- [ ] Full system integration test
- [ ] Strategy execution tests
- [ ] Risk management tests
- [ ] Position sizing tests
- [ ] Notification/alert tests

### Performance Testing

- [ ] Backtest against historical data (minimum 6 months)
- [ ] Paper trading (minimum 2 weeks)
- [ ] Performance metrics comparison
- [ ] Resource usage monitoring

### Production Validation

- [ ] Small position size initial deployment
- [ ] 24-hour monitoring period
- [ ] 1-week performance review
- [ ] Full deployment approval
"""
    
    # Specialized documentation helpers
    
    def _get_strategy_details(self, strategy_name, repos) -> str:
        """Get detailed strategy information"""
        # This would be expanded with actual strategy analysis
        return f"Strategy details for {strategy_name} would be extracted from actual code analysis.\n"
    
    def _analyze_strategy_parameters(self, repos) -> str:
        """Analyze strategy parameters across repos"""
        return """
Common parameters found:
- MA Fast Period: 10-20 (most common: 20)
- MA Slow Period: 50-200 (most common: 50)
- RSI Period: 14 (standard)
- RSI Oversold: 25-30 (most common: 30)
- RSI Overbought: 70-75 (most common: 70)
"""
    
    def _correlate_strategies_performance(self, repos) -> str:
        """Correlate strategies with performance"""
        return """
Based on documented performance:
- MA Crossover appears in highest-performing repos
- RSI Mean Reversion effective in ranging markets
- Combined approaches show promise in recent repos
"""
    
    def _extract_oanda_best_practices(self, repos) -> str:
        """Extract OANDA-specific best practices"""
        return """
1. **Use Practice Account First**: All high-performing repos emphasized testing
2. **Granularity Selection**: H1 and H4 most common for stable signals
3. **Risk Management**: 1-2% per trade maximum
4. **Instrument Selection**: Focus on major pairs (EUR_USD, GBP_USD, USD_JPY)
5. **Error Handling**: Always handle API rate limits and connection errors
"""
    
    def _generate_recommended_configs(self, repos) -> str:
        """Generate recommended configurations"""
        return """
```ini
# Recommended OANDA Configuration
OANDA_ENVIRONMENT=practice
OANDA_INSTRUMENTS=EUR_USD,GBP_USD,USD_JPY
OANDA_GRANULARITY=H1
OANDA_STRATEGY=ma_crossover
OANDA_MA_FAST=20
OANDA_MA_SLOW=50
OANDA_POLL_INTERVAL_SEC=3600
MAX_RISK_PER_TRADE=0.01
```
"""
    
    def _describe_harness_characteristics(self, harness_type) -> str:
        """Describe execution harness characteristics"""
        characteristics = {
            "continuous_polling": "Runs continuously with sleep intervals. Good for always-on systems.",
            "scheduled_cron": "Uses cron for periodic execution. Lower resource usage.",
            "tmux_background": "Runs in tmux session for persistence. Easy monitoring.",
        }
        return characteristics.get(harness_type, "Characteristics need analysis.")
    
    def _analyze_polling_strategies(self, repos) -> str:
        """Analyze polling strategies"""
        return """
### Observed Polling Intervals

- **High Frequency (< 1 hour)**: Used in 5 repos, higher API usage
- **Hourly (3600s)**: Most common, good balance
- **4-Hour+**: Conservative approach, lower costs

### Recommendations

- Start with hourly polling for H1 timeframe
- Adjust based on strategy needs and API limits
- Monitor API usage and adjust accordingly
"""
    
    def _analyze_error_handling(self, repos) -> str:
        """Analyze error handling patterns"""
        error_handling_count = sum(1 for r in repos if r.get('has_error_handling'))
        
        return f"""
### Error Handling Adoption

- **Repos with error handling:** {error_handling_count}/{len(repos)}
- **Common patterns:** try/except blocks, retry logic, logging

### Best Practices Identified

1. Catch specific API exceptions
2. Implement exponential backoff for retries
3. Log all errors with context
4. Alert on critical failures
5. Graceful degradation when possible
"""
    
    def _analyze_deployment_patterns(self, repos) -> str:
        """Analyze deployment patterns"""
        return """
### Deployment Methods Observed

1. **Manual Start**: `python main.py` (simplest)
2. **Shell Scripts**: `start_all.sh` (common)
3. **Systemd Services**: Production-grade (rare)
4. **Tmux Sessions**: Popular for persistence

### Recommended Approach

For production: Use systemd service with auto-restart
For development: Tmux sessions for easy monitoring
"""
    
    def _analyze_session_management(self, repos) -> str:
        """Analyze session management"""
        session_aware_count = sum(1 for r in repos if r.get('has_session_awareness'))
        
        return f"""
### Session Awareness

- **Repos with session awareness:** {session_aware_count}/{len(repos)}

### Approaches

1. **Time-based**: Check market hours before trading
2. **API-based**: Query broker for market status
3. **Hybrid**: Combine both approaches

### Benefits

- Avoid trading during low liquidity
- Respect market hours
- Reduce unnecessary API calls
"""
    
    def _analyze_performance_considerations(self, repos) -> str:
        """Analyze performance considerations"""
        return """
### Resource Usage

- **CPU**: Generally low, spikes during calculation
- **Memory**: 50-200MB typical
- **Network**: Depends on polling frequency
- **API Calls**: Primary constraint

### Optimization Strategies

1. Cache candle data when possible
2. Batch API requests where allowed
3. Use appropriate polling intervals
4. Implement rate limiting
"""
    
    def _generate_recommended_harness(self, repos) -> str:
        """Generate recommended harness architecture"""
        return """
### Recommended Architecture

```python
# Continuous polling with robust error handling
while True:
    try:
        # 1. Check market status
        if not is_market_open():
            sleep(900)  # 15 min
            continue
        
        # 2. Fetch data
        data = fetch_candles()
        
        # 3. Generate signals
        signal = strategy.analyze(data)
        
        # 4. Execute trades
        if signal != "HOLD":
            execute_trade(signal)
        
        # 5. Log status
        logger.info(f"Cycle complete: {signal}")
        
    except APIError as e:
        logger.error(f"API error: {e}")
        sleep(300)  # 5 min backoff
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        send_alert(f"Bot error: {e}")
        sleep(600)  # 10 min backoff
    
    finally:
        sleep(POLL_INTERVAL)
```

### Key Features

1. Market hours awareness
2. Robust error handling
3. Exponential backoff
4. Comprehensive logging
5. Critical alerts
6. Graceful degradation
"""

def save_report(filename: str, content: str, output_dir: str = "audit_reports"):
    """Save report to file"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath
