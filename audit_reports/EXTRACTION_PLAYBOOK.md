# Extraction & Integration Playbook

**Generated:** 2026-04-26 14:01:00 UTC

---

## Extraction Priority Rankings

Based on edge scores and component quality:


### 1. rfing_oanda_cba_restored_edge_04142026

- **Edge Score:** 41.2/100

- **Rank:** #1

- **Documented Performance:** 80.0/100

- **Notes:** High documented balance: $7,000, Has freeze manifest (performance snapshot), Explicitly mentions 'edge' in name/description



### 2. RICK_LIVE_CLEAN_FROZEN

- **Edge Score:** 38.5/100

- **Rank:** #2

- **Documented Performance:** 0.0/100



### 3. cba_oda_production_rebuilder

- **Edge Score:** 35.5/100

- **Rank:** #3

- **Documented Performance:** 0.0/100



### 4. FROZEN-V2

- **Edge Score:** 31.5/100

- **Rank:** #4

- **Documented Performance:** 0.0/100



### 5. RBOTZILLA_FINAL_v001

- **Edge Score:** 29.8/100

- **Rank:** #5

- **Documented Performance:** 0.0/100



---

## Component Extraction Guide

### Strategy Components


#### rsi_mean_reversion

- Found in 5 repositories

- Best implementations: cba_oda_production_rebuilder, rbotzilla_pheonix, multibroker_oanda_deployment_v1


#### ma_crossover

- Found in 2 repositories

- Best implementations: FROZEN-V2, R_BOTzilla_live_prototype-


### Broker Implementations


#### OANDA

- Implementations: 10

- Recommended sources: cba_oda_production_rebuilder, rfing_oanda_cba_restored_edge_04142026, OANDA_GIT_CLEAN


#### COINBASE

- Implementations: 8

- Recommended sources: cba_oda_production_rebuilder, rfing_oanda_cba_restored_edge_04142026, coinbase_clean_rbotz


### Execution Harness Patterns


#### continuous_polling

- Used in: cba_oda_production_rebuilder, live_lean_pheonix, RICK_LIVE_CLEAN_FROZEN


#### multi-broker continuous

- Used in: MULTIBROKER_ESSENTIALS_ONLY, multibroker_oanda_deployment_v1, multi_broker_rbtz


---

## Integration Steps


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


---

## Risk Assessment


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


---

## Testing Requirements


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
