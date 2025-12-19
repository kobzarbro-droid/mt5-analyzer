"""
Test script for input validation

This module tests the comprehensive validation logic for:
- StrategyMetrics: validates equity, drawdown, correlation, recovery factor, and name
- PortfolioAnalysisRequest: validates strategy count limits

Testing methodology:
- Unit tests with explicit assertions
- Boundary value testing for numeric ranges
- Error message verification
- Both positive and negative test cases
"""

import sys
import os
from portfolio_analyzer import StrategyMetrics, PortfolioAnalysisRequest

# Test data constants
DEFAULT_EQUITY = 100000.0
DEFAULT_DRAWDOWN = -10.0
DEFAULT_CORRELATION = 0.5
DEFAULT_RECOVERY = 2.0
DEFAULT_PROFIT = 20.0

def test_valid_strategy():
    """Test creating a valid strategy"""
    print("Testing valid strategy creation...")
    strategy = StrategyMetrics(
        name="Valid Strategy",
        equity=100000.0,
        drawdown=-15.5,
        correlation=0.65,
        recovery=2.3,
        profit=45.2
    )
    assert strategy.name == "Valid Strategy"
    print("✓ Valid strategy test passed")

def test_negative_equity():
    """Test that negative equity raises error"""
    print("\nTesting negative equity validation...")
    try:
        strategy = StrategyMetrics(
            name="Test",
            equity=-1000.0,
            drawdown=-15.5,
            correlation=0.65,
            recovery=2.3,
            profit=45.2
        )
        print("✗ Should have raised ValueError for negative equity")
        return False
    except ValueError as e:
        assert "Equity must be non-negative" in str(e)
        print(f"✓ Correctly rejected negative equity: {e}")
        return True

def test_positive_drawdown():
    """Test that positive drawdown raises error"""
    print("\nTesting positive drawdown validation...")
    try:
        strategy = StrategyMetrics(
            name="Test",
            equity=100000.0,
            drawdown=15.5,  # Should be negative
            correlation=0.65,
            recovery=2.3,
            profit=45.2
        )
        print("✗ Should have raised ValueError for positive drawdown")
        return False
    except ValueError as e:
        assert "Drawdown must be negative or zero" in str(e)
        print(f"✓ Correctly rejected positive drawdown: {e}")
        return True

def test_invalid_correlation():
    """Test that correlation outside [-1, 1] raises error"""
    print("\nTesting invalid correlation validation...")
    
    # Test correlation > 1
    try:
        strategy = StrategyMetrics(
            name="Test",
            equity=100000.0,
            drawdown=-15.5,
            correlation=1.5,  # Invalid
            recovery=2.3,
            profit=45.2
        )
        print("✗ Should have raised ValueError for correlation > 1")
        return False
    except ValueError as e:
        assert "Correlation must be between" in str(e)
        print(f"✓ Correctly rejected correlation > 1: {e}")
    
    # Test correlation < -1
    try:
        strategy = StrategyMetrics(
            name="Test",
            equity=100000.0,
            drawdown=-15.5,
            correlation=-1.5,  # Invalid
            recovery=2.3,
            profit=45.2
        )
        print("✗ Should have raised ValueError for correlation < -1")
        return False
    except ValueError as e:
        assert "Correlation must be between" in str(e)
        print(f"✓ Correctly rejected correlation < -1: {e}")
    
    return True

def test_negative_recovery():
    """Test that negative recovery factor raises error"""
    print("\nTesting negative recovery factor validation...")
    try:
        strategy = StrategyMetrics(
            name="Test",
            equity=100000.0,
            drawdown=-15.5,
            correlation=0.65,
            recovery=-2.3,  # Invalid
            profit=45.2
        )
        print("✗ Should have raised ValueError for negative recovery")
        return False
    except ValueError as e:
        assert "Recovery factor must be non-negative" in str(e)
        print(f"✓ Correctly rejected negative recovery: {e}")
        return True

def test_empty_name():
    """Test that empty strategy name raises error"""
    print("\nTesting empty strategy name validation...")
    try:
        strategy = StrategyMetrics(
            name="",  # Invalid
            equity=100000.0,
            drawdown=-15.5,
            correlation=0.65,
            recovery=2.3,
            profit=45.2
        )
        print("✗ Should have raised ValueError for empty name")
        return False
    except ValueError as e:
        assert "name must be a non-empty string" in str(e)
        print(f"✓ Correctly rejected empty name: {e}")
        return True

def test_empty_portfolio():
    """Test that empty portfolio raises error"""
    print("\nTesting empty portfolio validation...")
    try:
        portfolio = PortfolioAnalysisRequest(strategies=[])
        print("✗ Should have raised ValueError for empty portfolio")
        return False
    except ValueError as e:
        assert "strategy is required" in str(e)
        print(f"✓ Correctly rejected empty portfolio: {e}")
        return True

def test_too_many_strategies():
    """Test that too many strategies raises error"""
    print("\nTesting maximum strategies limit...")
    try:
        strategies = [
            StrategyMetrics(f"Strategy {i}", DEFAULT_EQUITY, DEFAULT_DRAWDOWN, DEFAULT_CORRELATION, DEFAULT_RECOVERY, DEFAULT_PROFIT)
            for i in range(15)  # More than max allowed (10)
        ]
        portfolio = PortfolioAnalysisRequest(strategies=strategies)
        print("✗ Should have raised ValueError for too many strategies")
        return False
    except ValueError as e:
        assert "Maximum 10 strategies allowed" in str(e)
        print(f"✓ Correctly rejected portfolio with >10 strategies: {e}")
        return True

def test_boundary_values():
    """Test boundary values for all fields"""
    print("\nTesting boundary values...")
    
    # Test zero drawdown (should be valid)
    strategy1 = StrategyMetrics("Test", 0.0, 0.0, 0.0, 0.0, 0.0)
    assert strategy1.drawdown == 0.0
    print("✓ Zero drawdown accepted")
    
    # Test correlation boundaries
    strategy2 = StrategyMetrics("Test", DEFAULT_EQUITY, DEFAULT_DRAWDOWN, -1.0, DEFAULT_RECOVERY, DEFAULT_PROFIT)
    assert strategy2.correlation == -1.0
    print("✓ Correlation = -1.0 accepted")
    
    strategy3 = StrategyMetrics("Test", DEFAULT_EQUITY, DEFAULT_DRAWDOWN, 1.0, DEFAULT_RECOVERY, DEFAULT_PROFIT)
    assert strategy3.correlation == 1.0
    print("✓ Correlation = 1.0 accepted")
    
    # Test exactly 10 strategies (should be valid)
    strategies = [
        StrategyMetrics(f"Strategy {i}", DEFAULT_EQUITY, DEFAULT_DRAWDOWN, DEFAULT_CORRELATION, DEFAULT_RECOVERY, DEFAULT_PROFIT)
        for i in range(10)
    ]
    portfolio = PortfolioAnalysisRequest(strategies=strategies)
    assert len(portfolio.strategies) == 10
    print("✓ Portfolio with exactly 10 strategies accepted")
    
    return True

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("MT5 Portfolio Analyzer - Validation Tests")
    print("=" * 60)
    
    tests = [
        test_valid_strategy,
        test_negative_equity,
        test_positive_drawdown,
        test_invalid_correlation,
        test_negative_recovery,
        test_empty_name,
        test_empty_portfolio,
        test_too_many_strategies,
        test_boundary_values
    ]
    
    failed = []
    
    for test in tests:
        try:
            result = test()
            if result is False:
                failed.append(test.__name__)
        except Exception as e:
            print(f"\n✗ Test {test.__name__} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            failed.append(test.__name__)
    
    print("\n" + "=" * 60)
    if not failed:
        print("✓ All validation tests passed successfully!")
        print("=" * 60)
        return 0
    else:
        print(f"✗ {len(failed)} test(s) failed:")
        for test_name in failed:
            print(f"  - {test_name}")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
