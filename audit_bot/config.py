"""
Configuration for GitHub Repository Audit Bot
"""

# GitHub Account to Audit
GITHUB_OWNER = "rfingerlin9284"

# Repository Count (as of analysis)
EXPECTED_REPO_COUNT = 24

# Known Baseline (for comparison)
BASELINE_REPO = "rfing_oanda_cba_restored_edge_04142026"
BASELINE_PERFORMANCE = {
    "oanda_balance": 7000,  # $7k+ achieved
    "date": "2026-04-14"
}

# Edge Analysis Keywords
PERFORMANCE_KEYWORDS = [
    "edge", "profit", "balance", "performance", "freeze",
    "green", "win", "loss", "capital", "gain", "return",
    "baseline", "production", "live", "practice"
]

MATURITY_KEYWORDS = [
    "frozen", "clean", "production", "final", "stable",
    "golden", "locked", "protected", "baseline", "restore"
]

BROKER_KEYWORDS = {
    "oanda": ["oanda", "forex", "fx"],
    "coinbase": ["coinbase", "crypto", "cba", "cb"],
    "multi": ["multi", "multibroker", "multi-broker"]
}

STRATEGY_KEYWORDS = [
    "ma_crossover", "rsi", "mean_reversion", "ema",
    "strategy", "signal", "indicator", "crossover"
]

# File Patterns to Analyze
CONFIG_FILES = [
    ".env", ".env.example", "config.py", "settings.py",
    "config.yaml", "config.yml", "configuration.py"
]

PERFORMANCE_FILES = [
    "FREEZE_MANIFEST.json", "performance.json", "results.json",
    "metrics.json", "backtest", "capital", "balance"
]

STRATEGY_FILES = [
    "strategy", "strategies", "trading", "signal"
]

DOC_FILES = [
    "README.md", "CHANGELOG.md", "NOTES.md", "PHASE",
    "TROUBLESHOOTING.md", "SETUP.md", "INSTALL.md"
]

# Scoring Weights
SCORING_WEIGHTS = {
    "documented_performance": 0.30,
    "code_quality": 0.20,
    "feature_completeness": 0.25,
    "maturity_signals": 0.15,
    "documentation": 0.10
}

# Output Configuration
OUTPUT_DIR = "audit_reports"
REPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# NEW: Additional documentation to generate
SPECIALIZED_DOCS = [
    "oanda_strategies.md",      # Consolidated OANDA strategy patterns
    "oanda_exec_harness.md"     # Execution harness patterns and best practices
]
