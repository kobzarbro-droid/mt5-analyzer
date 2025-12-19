"""
Flask API for MT5 Portfolio Analyzer
Provides REST endpoints for portfolio analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from portfolio_analyzer import PortfolioAnalyzer, StrategyMetrics, PortfolioAnalysisRequest
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize analyzer
analyzer = None


def get_analyzer():
    """Get or create portfolio analyzer instance"""
    global analyzer
    if analyzer is None:
        try:
            analyzer = PortfolioAnalyzer()
        except ValueError as e:
            return None, str(e)
    return analyzer, None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "MT5 Portfolio Analyzer"
    })


@app.route('/api/portfolio/analyze', methods=['POST'])
def analyze_portfolio():
    """
    Analyze portfolio endpoint
    
    Expected JSON body:
    {
        "strategies": [
            {
                "name": "Strategy 1",
                "equity": 150000,
                "drawdown": -15.5,
                "correlation": 0.65,
                "recovery": 2.3,
                "profit": 45.2
            },
            ...
        ]
    }
    """
    try:
        # Get analyzer instance
        analyzer_instance, error = get_analyzer()
        if error:
            return jsonify({
                "success": False,
                "error": f"API initialization failed: {error}"
            }), 500
        
        # Parse request data
        data = request.get_json()
        if not data or 'strategies' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'strategies' in request body"
            }), 400
        
        # Validate we have at least one strategy
        if len(data['strategies']) == 0:
            return jsonify({
                "success": False,
                "error": "At least one strategy is required"
            }), 400
        
        # Convert to StrategyMetrics objects
        strategies = []
        for strategy_data in data['strategies']:
            try:
                strategy = StrategyMetrics(
                    name=strategy_data.get('name', 'Unnamed Strategy'),
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
                    "error": f"Invalid strategy data: {str(e)}"
                }), 400
        
        # Create portfolio request
        portfolio = PortfolioAnalysisRequest(strategies=strategies)
        
        # Analyze portfolio
        result = analyzer_instance.analyze_portfolio(portfolio)
        
        # Format for display
        formatted_result = analyzer_instance.format_for_display(result)
        
        return jsonify(formatted_result)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/portfolio/test', methods=['GET'])
def test_analysis():
    """Test endpoint with sample data"""
    # Sample portfolio data
    sample_strategies = [
        {
            "name": "Trend Following Strategy",
            "equity": 125000,
            "drawdown": -12.5,
            "correlation": 0.45,
            "recovery": 2.8,
            "profit": 25.0
        },
        {
            "name": "Mean Reversion Strategy",
            "equity": 98000,
            "drawdown": -18.2,
            "correlation": 0.32,
            "recovery": 1.9,
            "profit": -2.0
        },
        {
            "name": "Breakout Strategy",
            "equity": 142000,
            "drawdown": -10.1,
            "correlation": 0.55,
            "recovery": 3.2,
            "profit": 42.0
        },
        {
            "name": "Grid Trading Strategy",
            "equity": 88000,
            "drawdown": -22.5,
            "correlation": 0.28,
            "recovery": 1.5,
            "profit": -12.0
        },
        {
            "name": "Scalping Strategy",
            "equity": 115000,
            "drawdown": -15.8,
            "correlation": 0.38,
            "recovery": 2.1,
            "profit": 15.0
        }
    ]
    
    return analyze_portfolio.__wrapped__(
        request=type('Request', (), {
            'get_json': lambda: {"strategies": sample_strategies}
        })()
    )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
