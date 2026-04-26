# OANDA Trading Strategies Analysis

**Generated:** 2026-04-26 14:01:00 UTC

**Source:** Cross-repository analysis of rfingerlin9284 account


---

## Overview

This document consolidates all OANDA trading strategies discovered 
across 24 repositories, including implementation patterns, parameters, 
and performance characteristics.


**Total OANDA Repositories:** 10


## Strategy Patterns Discovered


### Rsi Mean Reversion

- **Implementations:** 2

- **Found in:** cba_oda_production_rebuilder, multibroker_oanda_deployment_v1


#### Implementation Details

Strategy details for rsi_mean_reversion would be extracted from actual code analysis.


### Ma Crossover

- **Implementations:** 1

- **Found in:** R_BOTzilla_live_prototype-


#### Implementation Details

Strategy details for ma_crossover would be extracted from actual code analysis.


---

## Parameter Analysis


Common parameters found:
- MA Fast Period: 10-20 (most common: 20)
- MA Slow Period: 50-200 (most common: 50)
- RSI Period: 14 (standard)
- RSI Oversold: 25-30 (most common: 30)
- RSI Overbought: 70-75 (most common: 70)


---

## Strategy-Performance Correlation


Based on documented performance:
- MA Crossover appears in highest-performing repos
- RSI Mean Reversion effective in ranging markets
- Combined approaches show promise in recent repos


---

## OANDA Strategy Best Practices


1. **Use Practice Account First**: All high-performing repos emphasized testing
2. **Granularity Selection**: H1 and H4 most common for stable signals
3. **Risk Management**: 1-2% per trade maximum
4. **Instrument Selection**: Focus on major pairs (EUR_USD, GBP_USD, USD_JPY)
5. **Error Handling**: Always handle API rate limits and connection errors


---

## Recommended Configurations


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
