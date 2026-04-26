# GitHub Repository Audit Bot

Automated audit system for analyzing trading bot repositories to identify optimal "edge" characteristics and extraction opportunities.

## Overview

This audit bot analyzes all 24 repositories in the rfingerlin9284 GitHub account to:
- Identify repositories with the best trading "edge" (performance/profitability)
- Compare features, strategies, and architectures
- Recommend components for extraction and integration
- Generate specialized documentation for OANDA strategies and execution harness patterns

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Prepare Repository Data

The audit bot needs repository data from GitHub. You can:

**Option A: Use existing GitHub search results**
```bash
# If you have GitHub API response saved:
python audit_engine.py path/to/github_search_results.json
```

**Option B: Create sample data for testing**
```bash
python fetch_repo_data.py --create-sample
python audit_engine.py repos_sample.json
```

**Option C: In the actual GitHub Copilot environment**
The audit would use `github-mcp-server` tools to fetch live data automatically.

### Step 2: Run the Audit

```bash
python audit_engine.py repos.json --output-dir audit_reports
```

## Output Files

The audit generates the following reports in the `audit_reports/` directory:

1. **MASTER_AUDIT_REPORT.md** - Complete audit findings for all repositories
2. **EXTRACTION_PLAYBOOK.md** - Step-by-step extraction and integration guide
3. **oanda_strategies.md** - Consolidated OANDA strategy patterns and best practices
4. **oanda_exec_harness.md** - Execution harness patterns and recommendations
5. **audit_data.json** - Machine-readable audit data

## Key Features

### Edge Scoring
Repositories are scored on:
- **Documented Performance** (30%): Account balances, profitability metrics
- **Code Quality** (20%): Error handling, logging, testing
- **Feature Completeness** (25%): Broker support, strategies, risk management
- **Maturity Signals** (15%): Frozen/production tags, stability indicators
- **Documentation** (10%): README quality, guides, setup docs

### Component Analysis
- Strategy implementations (MA Crossover, RSI, etc.)
- Broker integrations (OANDA, Coinbase)
- Risk management patterns
- Execution harness types
- Session management approaches

### Comparison Tables
- Performance ranking across all repos
- Feature matrix showing capabilities
- Architecture evolution timeline
- Component reusability analysis

## Architecture

```
audit_bot/
├── config.py              # Configuration and constants
├── github_analyzer.py     # Repository metadata analysis
├── code_analyzer.py       # Code structure and component analysis
├── edge_scorer.py         # Performance scoring system
├── comparator.py          # Cross-repository comparison
├── report_generator.py    # Markdown report generation
├── audit_engine.py        # Main orchestration
├── fetch_repo_data.py     # Repository data fetcher
└── requirements.txt       # Python dependencies
```

## Specialized Documentation

### oanda_strategies.md
Comprehensive analysis of OANDA trading strategies including:
- Strategy pattern catalog
- Parameter analysis across repos
- Strategy-performance correlation
- Best practices and recommendations
- Optimal configurations

### oanda_exec_harness.md
Execution harness documentation including:
- Harness type classification
- Polling strategy analysis
- Error handling patterns
- Deployment approaches
- Session management techniques
- Performance considerations
- Recommended architecture with code examples

## Integration with RBOTZILLA Operator

The audit recognizes and documents patterns similar to the RBOTZILLA operator system:
- Safety-first execution policies
- Intent classification systems
- Dedicated bot operators
- Restart safety checks
- Version management
- Freeze/restore workflows

## Safety Notes

- **READ-ONLY**: The audit never modifies source repositories
- **HISTORICAL**: Analyzes repositories as-is without changes
- **INDEPENDENT**: Runs autonomously with minimal intervention
- **COMPREHENSIVE**: Every repository gets equal analytical attention

## Example Output

```
Top 5 Repositories by Edge Score:
1. rfing_oanda_cba_restored_edge_04142026: 87.3/100
2. rbotzilla_pheonix: 76.5/100
3. OANDA_GIT_CLEAN: 72.1/100
4. rick_clean_live: 68.9/100
5. multibroker_oanda_deployment_v1: 65.4/100
```

## Next Steps After Audit

1. Review MASTER_AUDIT_REPORT.md for top performers
2. Study EXTRACTION_PLAYBOOK.md for integration recommendations
3. Review oanda_strategies.md for strategy improvements
4. Review oanda_exec_harness.md for execution improvements
5. Follow extraction priorities to integrate best components

## License

MIT - See LICENSE file in parent directory
