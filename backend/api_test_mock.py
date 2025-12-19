"""
Flask API for MT5 Portfolio Analyzer - Test Version with Mock AI
Provides REST endpoints for portfolio analysis with mocked AI responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from portfolio_analyzer import StrategyMetrics, PortfolioAnalysisRequest
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

def mock_ai_analysis(portfolio):
    """Generate a mock AI analysis for testing"""
    strategies = portfolio.strategies
    
    # Calculate some basic stats
    avg_profit = sum(s.profit for s in strategies) / len(strategies)
    avg_drawdown = sum(s.drawdown for s in strategies) / len(strategies)
    avg_correlation = sum(s.correlation for s in strategies) / len(strategies)
    best_strategy = max(strategies, key=lambda s: s.profit)
    worst_strategy = min(strategies, key=lambda s: s.profit)
    
    analysis = f"""## Overall Portfolio Assessment

Your portfolio consists of {len(strategies)} trading strategies with an average profit of {avg_profit:.1f}% and an average drawdown of {avg_drawdown:.1f}%. The portfolio shows moderate diversification with an average correlation of {avg_correlation:.2f}.

## Strategy Recommendations

**Top Performer:** {best_strategy.name} (Profit: {best_strategy.profit:.1f}%)
- This strategy demonstrates strong performance and should be prioritized in your allocation.
- Consider increasing position size if risk parameters remain acceptable.

**Underperformer:** {worst_strategy.name} (Profit: {worst_strategy.profit:.1f}%)
- This strategy requires careful review and potential optimization.
- Consider reducing exposure or implementing stricter risk controls.

**Allocation Suggestions:**
1. Allocate 30-40% to top-performing strategies
2. Limit exposure to underperforming strategies to 10-15%
3. Maintain balanced allocation across remaining strategies

## Strengths

1. **Portfolio Diversification:** The strategies show varying correlation levels, which helps reduce overall portfolio risk.

2. **Risk Management:** Average drawdown of {avg_drawdown:.1f}% indicates reasonable risk control across the portfolio.

3. **Recovery Capability:** The strategies demonstrate good recovery factors, suggesting resilience after drawdown periods.

4. **Performance Mix:** The portfolio includes both high-performing and stable strategies, providing a balanced risk-return profile.

## Weaknesses

1. **Drawdown Exposure:** Some strategies show significant drawdowns that could impact overall portfolio stability during market stress.

2. **Correlation Risk:** Higher correlation between certain strategies may reduce diversification benefits during market extremes.

3. **Performance Variance:** The gap between best and worst performers is substantial, suggesting potential for portfolio optimization.

4. **Recovery Time:** Strategies with lower recovery factors may require longer periods to recuperate from losses.

## Risk Analysis

**Drawdown Assessment:**
- Maximum individual drawdown: {min(s.drawdown for s in strategies):.1f}%
- Average portfolio drawdown: {avg_drawdown:.1f}%
- Risk level: {'High' if avg_drawdown < -15 else 'Moderate' if avg_drawdown < -10 else 'Low'}

**Correlation Analysis:**
- Average correlation: {avg_correlation:.2f}
- Diversification benefit: {'Strong' if avg_correlation < 0.4 else 'Moderate' if avg_correlation < 0.6 else 'Limited'}

**Overall Risk Exposure:**
The portfolio presents a {'high' if avg_drawdown < -15 else 'moderate'} risk profile. Consider implementing additional risk controls and position sizing rules.

## Actionable Recommendations

1. **Rebalance Portfolio Allocation:** Shift capital toward consistently profitable strategies while reducing exposure to underperformers.

2. **Implement Stop-Loss Rules:** Set maximum drawdown limits at -20% for individual strategies to protect capital.

3. **Monitor Correlation:** Regularly review correlation metrics and adjust allocations if strategies become too correlated.

4. **Enhance Underperformers:** Analyze and optimize parameters for strategies showing negative or minimal returns.

5. **Consider Scaling:** For top-performing strategies with low drawdowns, gradually increase position sizes while maintaining risk limits.

---

*This analysis is based on the provided metrics and should be combined with ongoing monitoring and risk management practices.*"""
    
    return analysis


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "MT5 Portfolio Analyzer (Test Mode)"
    })


@app.route('/api/portfolio/analyze', methods=['POST'])
def analyze_portfolio():
    """
    Analyze portfolio endpoint with mock AI
    """
    start_time = time.time()
    
    try:
        # Parse request data
        data = request.get_json()
        if not data or 'strategies' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'strategies' in request body",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Validate we have at least one strategy
        if len(data['strategies']) == 0:
            return jsonify({
                "success": False,
                "error": "At least one strategy is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Convert to StrategyMetrics objects
        strategies = []
        for i, strategy_data in enumerate(data['strategies'], 1):
            try:
                strategy = StrategyMetrics(
                    name=strategy_data.get('name', f'Strategy {i}'),
                    equity=float(strategy_data.get('equity', 0)),
                    drawdown=float(strategy_data.get('drawdown', 0)),
                    correlation=float(strategy_data.get('correlation', 0)),
                    recovery=float(strategy_data.get('recovery', 0)),
                    profit=float(strategy_data.get('profit', 0))
                )
                strategies.append(strategy)
            except (ValueError, TypeError) as e:
                return jsonify({
                    "success": False,
                    "error": f"Invalid strategy data at index {i}: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }), 400
        
        # Create portfolio request
        portfolio = PortfolioAnalysisRequest(strategies=strategies)
        
        # Simulate processing time (0.5-1.5 seconds)
        time.sleep(0.5)
        
        # Generate mock analysis
        analysis_text = mock_ai_analysis(portfolio)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Format result
        result = {
            "success": True,
            "full_analysis": analysis_text,
            "strategies_count": len(strategies),
            "model": "mock-ai (test mode)",
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time
        }
        
        return jsonify(result)
    
    except Exception as e:
        processing_time = time.time() - start_time
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    print("=" * 60)
    print("MT5 Portfolio Analyzer - TEST MODE")
    print("Using mock AI responses for testing")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=debug)
