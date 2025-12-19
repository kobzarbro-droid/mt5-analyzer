"""
Test script for Portfolio Analyzer API
Tests the API endpoints without requiring OpenAI API calls
"""

import sys
import os
from portfolio_analyzer import StrategyMetrics, PortfolioAnalysisRequest

def test_strategy_metrics():
    """Test StrategyMetrics dataclass"""
    print("Testing StrategyMetrics creation...")
    strategy = StrategyMetrics(
        name="Test Strategy",
        equity=100000.0,
        drawdown=-15.5,
        correlation=0.65,
        recovery=2.3,
        profit=45.2
    )
    assert strategy.name == "Test Strategy"
    assert strategy.equity == 100000.0
    print("✓ StrategyMetrics test passed")

def test_portfolio_request():
    """Test PortfolioAnalysisRequest dataclass"""
    print("\nTesting PortfolioAnalysisRequest creation...")
    strategies = [
        StrategyMetrics("S1", 100000, -10.0, 0.5, 2.0, 20.0),
        StrategyMetrics("S2", 150000, -12.5, 0.6, 2.5, 30.0),
    ]
    portfolio = PortfolioAnalysisRequest(strategies=strategies)
    assert len(portfolio.strategies) == 2
    print("✓ PortfolioAnalysisRequest test passed")

def test_prompt_creation():
    """Test prompt creation without API call"""
    print("\nTesting prompt creation...")
    
    # Set a dummy API key to avoid initialization error
    os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'
    
    from portfolio_analyzer import PortfolioAnalyzer
    
    analyzer = PortfolioAnalyzer(api_key='test-key')
    
    strategies = [
        StrategyMetrics("Trend Following", 125000, -12.5, 0.45, 2.8, 25.0),
        StrategyMetrics("Mean Reversion", 98000, -18.2, 0.32, 1.9, -2.0),
    ]
    portfolio = PortfolioAnalysisRequest(strategies=strategies)
    
    prompt = analyzer.create_analysis_prompt(portfolio)
    
    assert "Trend Following" in prompt
    assert "Mean Reversion" in prompt
    assert "125000" in prompt
    assert "Equity" in prompt
    assert "Drawdown" in prompt
    print("✓ Prompt creation test passed")
    print(f"\nGenerated prompt preview:\n{prompt[:300]}...")

def test_format_for_display():
    """Test result formatting"""
    print("\nTesting format_for_display...")
    
    os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'
    from portfolio_analyzer import PortfolioAnalyzer
    
    analyzer = PortfolioAnalyzer(api_key='test-key')
    
    # Test success case
    success_result = {
        "success": True,
        "analysis": "This is a test analysis with recommendations.",
        "strategies_analyzed": 5,
        "model_used": "gpt-4o"
    }
    formatted = analyzer.format_for_display(success_result)
    assert formatted["success"] == True
    assert "full_analysis" in formatted
    print("✓ Success case formatting test passed")
    
    # Test error case
    error_result = {
        "success": False,
        "error": "Test error"
    }
    formatted_error = analyzer.format_for_display(error_result)
    assert formatted_error["success"] == False
    assert "error" in formatted_error
    print("✓ Error case formatting test passed")

def main():
    """Run all tests"""
    print("=" * 60)
    print("MT5 Portfolio Analyzer - Unit Tests")
    print("=" * 60)
    
    try:
        test_strategy_metrics()
        test_portfolio_request()
        test_prompt_creation()
        test_format_for_display()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
