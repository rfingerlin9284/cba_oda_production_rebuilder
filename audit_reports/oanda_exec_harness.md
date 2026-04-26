# OANDA Execution Harness Patterns

**Generated:** 2026-04-26 14:01:00 UTC

**Source:** Cross-repository analysis of rfingerlin9284 account


---

## Overview

This document analyzes execution harness patterns used across 
OANDA trading bot implementations, including polling strategies, 
error handling, and deployment patterns.


## Execution Harness Types


### Continuous Polling

- **Repos using this pattern:** 3

- **Examples:** cba_oda_production_rebuilder, live_lean_pheonix, R_BOTzilla_live_prototype-


#### Characteristics

Runs continuously with sleep intervals. Good for always-on systems.

### Unknown

- **Repos using this pattern:** 6

- **Examples:** rfing_oanda_cba_restored_edge_04142026, OANDA_GIT_CLEAN, MUILTIBROKER_OANDA_REPO


#### Characteristics

Characteristics need analysis.

### Multi-Broker Continuous

- **Repos using this pattern:** 1

- **Examples:** multibroker_oanda_deployment_v1


#### Characteristics

Characteristics need analysis.

---

## Polling Strategies


### Observed Polling Intervals

- **High Frequency (< 1 hour)**: Used in 5 repos, higher API usage
- **Hourly (3600s)**: Most common, good balance
- **4-Hour+**: Conservative approach, lower costs

### Recommendations

- Start with hourly polling for H1 timeframe
- Adjust based on strategy needs and API limits
- Monitor API usage and adjust accordingly


---

## Error Handling Patterns


### Error Handling Adoption

- **Repos with error handling:** 6/10
- **Common patterns:** try/except blocks, retry logic, logging

### Best Practices Identified

1. Catch specific API exceptions
2. Implement exponential backoff for retries
3. Log all errors with context
4. Alert on critical failures
5. Graceful degradation when possible


---

## Deployment Patterns


### Deployment Methods Observed

1. **Manual Start**: `python main.py` (simplest)
2. **Shell Scripts**: `start_all.sh` (common)
3. **Systemd Services**: Production-grade (rare)
4. **Tmux Sessions**: Popular for persistence

### Recommended Approach

For production: Use systemd service with auto-restart
For development: Tmux sessions for easy monitoring


---

## Session Management


### Session Awareness

- **Repos with session awareness:** 1/10

### Approaches

1. **Time-based**: Check market hours before trading
2. **API-based**: Query broker for market status
3. **Hybrid**: Combine both approaches

### Benefits

- Avoid trading during low liquidity
- Respect market hours
- Reduce unnecessary API calls


---

## Performance Considerations


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


---

## Recommended Harness Architecture


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
