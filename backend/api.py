"""
Flask API for MT5 Portfolio Analyzer
Provides REST endpoints for portfolio analysis
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from portfolio_analyzer import PortfolioAnalyzer, StrategyMetrics, PortfolioAnalysisRequest
from mt5_parser import MT5Parser, OptimizationResult, BacktestReport, Trade, EquityPoint
from set_file_generator import SetFileGenerator
from preset_manager import PresetManager, Preset
from expert_analyzer import ExpertAnalyzer, ExpertMetrics
import os
import logging
from io import BytesIO
from werkzeug.utils import secure_filename

try:
    import openai
except ImportError:
    openai = None
    logger.warning("OpenAI package not available. GPT features will not work.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize analyzer and managers
analyzer = None
preset_manager = PresetManager()
parser = MT5Parser()
set_generator = SetFileGenerator()
expert_analyzer = ExpertAnalyzer()


def get_analyzer():
    """Get or create portfolio analyzer instance"""
    global analyzer
    if analyzer is None:
        try:
            logger.info("Initializing PortfolioAnalyzer")
            analyzer = PortfolioAnalyzer()
        except ValueError as e:
            logger.error(f"Failed to initialize analyzer: {str(e)}")
            return None, str(e)
    return analyzer, None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
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
        logger.info("Received portfolio analysis request")
        
        # Get analyzer instance
        analyzer_instance, error = get_analyzer()
        if error:
            logger.error(f"Analyzer initialization error: {error}")
            return jsonify({
                "success": False,
                "error": f"API initialization failed: {error}"
            }), 500
        
        # Parse request data
        data = request.get_json()
        if not data or 'strategies' not in data:
            logger.warning("Invalid request: missing 'strategies' field")
            return jsonify({
                "success": False,
                "error": "Missing 'strategies' in request body"
            }), 400
        
        # Validate we have at least one strategy
        if len(data['strategies']) == 0:
            logger.warning("Invalid request: no strategies provided")
            return jsonify({
                "success": False,
                "error": "At least one strategy is required"
            }), 400
        
        logger.info(f"Processing {len(data['strategies'])} strategies")
        
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
                logger.debug(f"Validated strategy {i}: {strategy.name}")
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid strategy data at index {i}: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": f"Invalid strategy data at index {i}: {str(e)}"
                }), 400
        
        # Create portfolio request
        portfolio = PortfolioAnalysisRequest(strategies=strategies)
        
        # Analyze portfolio
        result = analyzer_instance.analyze_portfolio(portfolio)
        
        # Format for display
        formatted_result = analyzer_instance.format_for_display(result)
        
        if formatted_result.get("success"):
            logger.info("Analysis completed successfully")
        else:
            logger.warning("Analysis completed with errors")
        
        return jsonify(formatted_result)
    
    except Exception as e:
        logger.exception("Unexpected error during analysis")
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


@app.route('/api/upload/optimization', methods=['POST'])
def upload_optimization_report():
    """Upload and parse optimization report"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400
        
        # Read file content
        content = file.read().decode('utf-8', errors='ignore')
        
        # Determine file type
        file_type = 'xml' if file.filename.endswith('.xml') else 'html'
        
        # Parse optimization report
        results = parser.parse_optimization_report(content, file_type)
        
        logger.info(f"Parsed optimization report with {len(results)} results")
        
        return jsonify({
            "success": True,
            "results_count": len(results),
            "results": [r.to_dict() for r in results]
        })
        
    except Exception as e:
        logger.exception("Error uploading optimization report")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/upload/forward', methods=['POST'])
def upload_forward_report():
    """Upload and parse forward test report"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400
        
        # Read file content
        content = file.read().decode('utf-8', errors='ignore')
        
        # Determine file type
        file_type = 'xml' if file.filename.endswith('.xml') else 'html'
        
        # Parse forward test report
        results = parser.parse_optimization_report(content, file_type)
        
        logger.info(f"Parsed forward test report with {len(results)} results")
        
        return jsonify({
            "success": True,
            "results_count": len(results),
            "results": [r.to_dict() for r in results]
        })
        
    except Exception as e:
        logger.exception("Error uploading forward test report")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/upload/backtest', methods=['POST'])
def upload_backtest_report():
    """Upload and parse backtest report"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400
        
        preset_id = request.form.get('preset_id')
        if not preset_id:
            return jsonify({"success": False, "error": "Preset ID required"}), 400
        
        # Read file content
        content = file.read().decode('utf-8', errors='ignore')
        
        # Parse backtest report
        report = parser.parse_backtest_report(content)
        
        # Update preset with backtest report
        success = preset_manager.update_preset_backtest(preset_id, report.to_dict())
        
        if not success:
            return jsonify({"success": False, "error": "Preset not found"}), 404
        
        logger.info(f"Uploaded backtest report for preset {preset_id}")
        
        return jsonify({
            "success": True,
            "preset_id": preset_id,
            "report": report.to_dict()
        })
        
    except Exception as e:
        logger.exception("Error uploading backtest report")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/analyze/best-parameters', methods=['POST'])
def find_best_parameters():
    """Find best parameters from optimization and forward test results"""
    try:
        data = request.get_json()
        
        if not data or 'optimization_results' not in data:
            return jsonify({"success": False, "error": "Missing optimization results"}), 400
        
        # Convert to OptimizationResult objects
        opt_results = []
        for r in data['optimization_results']:
            opt_results.append(OptimizationResult(
                pass_number=r.get('pass_number', 0),
                parameters=r.get('parameters', {}),
                profit=r.get('profit', 0),
                total_trades=r.get('total_trades', 0),
                profit_factor=r.get('profit_factor'),
                expected_payoff=r.get('expected_payoff'),
                drawdown=r.get('drawdown'),
                drawdown_percent=r.get('drawdown_percent'),
                sharpe_ratio=r.get('sharpe_ratio'),
                recovery_factor=r.get('recovery_factor'),
                win_rate=r.get('win_rate')
            ))
        
        # Get forward test results if provided
        fwd_results = None
        if 'forward_results' in data:
            fwd_results = []
            for r in data['forward_results']:
                fwd_results.append(OptimizationResult(
                    pass_number=r.get('pass_number', 0),
                    parameters=r.get('parameters', {}),
                    profit=r.get('profit', 0),
                    total_trades=r.get('total_trades', 0),
                    profit_factor=r.get('profit_factor'),
                    expected_payoff=r.get('expected_payoff'),
                    drawdown=r.get('drawdown'),
                    sharpe_ratio=r.get('sharpe_ratio'),
                    recovery_factor=r.get('recovery_factor')
                ))
        
        # Get filter criteria
        criteria = data.get('criteria', {})
        
        # Find best parameters
        best_results = parser.find_best_parameters(opt_results, fwd_results, criteria)
        
        logger.info(f"Found {len(best_results)} best parameter sets")
        
        return jsonify({
            "success": True,
            "best_results": [r.to_dict() for r in best_results]
        })
        
    except Exception as e:
        logger.exception("Error finding best parameters")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/gpt/recommend-parameters', methods=['POST'])
def gpt_recommend_parameters():
    """Get GPT recommendations for parameter sets"""
    try:
        analyzer_instance, error = get_analyzer()
        if error:
            return jsonify({"success": False, "error": f"API initialization failed: {error}"}), 500
        
        data = request.get_json()
        
        if not data or 'parameter_sets' not in data:
            return jsonify({"success": False, "error": "Missing parameter sets"}), 400
        
        parameter_sets = data['parameter_sets']
        
        # Create prompt for GPT
        prompt = f"""Analyze the following {len(parameter_sets)} MT5 trading parameter sets and provide recommendations:

"""
        for i, param_set in enumerate(parameter_sets, 1):
            prompt += f"""
Parameter Set {i}:
- Parameters: {param_set.get('parameters', {})}
- Profit: ${param_set.get('profit', 0):.2f}
- Total Trades: {param_set.get('total_trades', 0)}
- Profit Factor: {param_set.get('profit_factor', 'N/A')}
- Drawdown: {param_set.get('drawdown', 'N/A')}
- Sharpe Ratio: {param_set.get('sharpe_ratio', 'N/A')}
- Recovery Factor: {param_set.get('recovery_factor', 'N/A')}
"""
        
        prompt += """

Please provide:
1. Which parameter set(s) show the most promise and why
2. Risk assessment for each set
3. Recommendations for further optimization
4. Which set would you recommend for live trading and why
5. Any red flags or concerns with any of the parameter sets

Format your response in a clear, structured manner."""
        
        # Call OpenAI API
        if openai is None:
            return jsonify({"success": False, "error": "OpenAI package not available"}), 500
        
        openai.api_key = analyzer_instance.api_key
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert MT5 trading strategy analyst. Provide detailed, actionable analysis of trading parameters."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        
        logger.info("GPT recommendations generated")
        
        return jsonify({
            "success": True,
            "recommendations": analysis
        })
        
    except Exception as e:
        logger.exception("Error generating GPT recommendations")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/create', methods=['POST'])
def create_preset():
    """Create a new preset from parameter set"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'parameters' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        preset = preset_manager.add_preset(
            name=data['name'],
            parameters=data['parameters'],
            optimization_metrics=data.get('optimization_metrics', {})
        )
        
        logger.info(f"Created preset: {preset.name}")
        
        return jsonify({
            "success": True,
            "preset": preset.to_dict()
        })
        
    except Exception as e:
        logger.exception("Error creating preset")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/list', methods=['GET'])
def list_presets():
    """Get all presets"""
    try:
        presets = preset_manager.get_all_presets()
        
        return jsonify({
            "success": True,
            "presets": [p.to_dict() for p in presets]
        })
        
    except Exception as e:
        logger.exception("Error listing presets")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/<preset_id>', methods=['GET'])
def get_preset(preset_id):
    """Get a specific preset"""
    try:
        preset = preset_manager.get_preset(preset_id)
        
        if not preset:
            return jsonify({"success": False, "error": "Preset not found"}), 404
        
        return jsonify({
            "success": True,
            "preset": preset.to_dict()
        })
        
    except Exception as e:
        logger.exception("Error getting preset")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/<preset_id>', methods=['DELETE'])
def delete_preset(preset_id):
    """Delete a preset"""
    try:
        success = preset_manager.delete_preset(preset_id)
        
        if not success:
            return jsonify({"success": False, "error": "Preset not found"}), 404
        
        return jsonify({"success": True})
        
    except Exception as e:
        logger.exception("Error deleting preset")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/<preset_id>/download', methods=['GET'])
def download_set_file(preset_id):
    """Download .set file for a preset"""
    try:
        preset = preset_manager.get_preset(preset_id)
        
        if not preset:
            return jsonify({"success": False, "error": "Preset not found"}), 404
        
        # Generate .set file content
        set_content = set_generator.generate_set_file(preset.parameters, preset.name)
        
        # Create BytesIO object for download
        set_file = BytesIO(set_content.encode('utf-8'))
        set_file.seek(0)
        
        filename = secure_filename(f"{preset.name}.set")
        
        return send_file(
            set_file,
            mimetype='text/plain',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.exception("Error downloading .set file")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preset/compare', methods=['POST'])
def compare_presets():
    """Compare multiple presets"""
    try:
        data = request.get_json()
        
        if not data or 'preset_ids' not in data:
            return jsonify({"success": False, "error": "Missing preset IDs"}), 400
        
        preset_ids = data['preset_ids']
        
        if not isinstance(preset_ids, list) or len(preset_ids) < 2:
            return jsonify({"success": False, "error": "At least 2 presets required for comparison"}), 400
        
        comparison = preset_manager.compare_presets(preset_ids)
        
        logger.info(f"Compared {len(preset_ids)} presets")
        
        return jsonify({
            "success": True,
            "comparison": comparison
        })
        
    except Exception as e:
        logger.exception("Error comparing presets")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/gpt/compare-presets', methods=['POST'])
def gpt_compare_presets():
    """Get GPT analysis comparing multiple presets"""
    try:
        analyzer_instance, error = get_analyzer()
        if error:
            return jsonify({"success": False, "error": f"API initialization failed: {error}"}), 500
        
        data = request.get_json()
        
        if not data or 'preset_ids' not in data:
            return jsonify({"success": False, "error": "Missing preset IDs"}), 400
        
        preset_ids = data['preset_ids']
        comparison = preset_manager.compare_presets(preset_ids)
        
        if 'error' in comparison:
            return jsonify({"success": False, "error": comparison['error']}), 400
        
        # Create prompt for GPT
        prompt = f"""Analyze and compare the following {len(comparison['presets'])} MT5 trading strategy presets:

"""
        for preset_info in comparison['presets']:
            prompt += f"""
Preset: {preset_info['name']}
Parameters: {preset_info['parameters']}
"""
            if 'backtest_metrics' in preset_info:
                metrics = preset_info['backtest_metrics']
                prompt += f"""Backtest Results:
- Net Profit: ${metrics.get('total_net_profit', 0):.2f}
- Profit Factor: {metrics.get('profit_factor', 'N/A')}
- Max Drawdown: ${metrics.get('maximal_drawdown', 0):.2f}
- Sharpe Ratio: {metrics.get('sharpe_ratio', 'N/A')}
- Recovery Factor: {metrics.get('recovery_factor', 'N/A')}
- Total Trades: {metrics.get('total_trades', 0)}
- Win Rate: {metrics.get('win_rate', 0):.2f}%
"""
            prompt += "\n"
        
        prompt += """
Please provide a comprehensive comparative analysis including:

1. **Performance Ranking**: Rank the presets from best to worst with justification
2. **Risk Assessment**: Compare risk profiles of each preset
3. **Consistency Analysis**: Which preset shows most consistent performance
4. **Recommendation**: Which preset(s) would you recommend for live trading and why
5. **Optimization Suggestions**: How could each preset be improved
6. **Red Flags**: Any concerns or warnings about any of the presets

Format your response in a clear, structured manner with specific recommendations."""
        
        # Call OpenAI API
        if openai is None:
            return jsonify({"success": False, "error": "OpenAI package not available"}), 500
        
        openai.api_key = analyzer_instance.api_key
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert MT5 trading strategy analyst with deep knowledge of risk management and portfolio optimization."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        analysis = response.choices[0].message.content
        
        logger.info("GPT comparison analysis generated")
        
        return jsonify({
            "success": True,
            "comparison_data": comparison,
            "gpt_analysis": analysis
        })
        
    except Exception as e:
        logger.exception("Error generating GPT comparison")
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== Expert Analysis Endpoints ====================

@app.route('/api/experts/analyze', methods=['POST'])
def analyze_experts():
    """
    Analyze experts from uploaded reports with grouping by magic number
    
    Expected JSON body:
    {
        "backtest_report": BacktestReport dict or HTML content,
        "group_by": "magic_number",
        "calculate_equity": true,
        "initial_balance": 10000
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Parse backtest report if HTML content provided
        backtest_report = data.get('backtest_report')
        initial_balance = float(data.get('initial_balance', 10000))
        calculate_equity = data.get('calculate_equity', True)
        
        if isinstance(backtest_report, str):
            # Parse HTML report
            report = parser.parse_backtest_report(backtest_report)
            trades = report.trades
        elif isinstance(backtest_report, dict):
            # Use provided dict
            trades = backtest_report.get('trades', [])
        else:
            return jsonify({"success": False, "error": "Invalid backtest report format"}), 400
        
        if not trades:
            return jsonify({"success": False, "error": "No trades found in report"}), 400
        
        # Group trades by magic number
        trades_by_magic = expert_analyzer.group_by_magic_from_dict(trades)
        
        # Calculate metrics for each expert
        metrics_by_expert = expert_analyzer.calculate_metrics_from_dict(trades_by_magic, initial_balance)
        
        # Calculate equity curves if requested
        equity_curves = {}
        if calculate_equity:
            # Convert dict trades to Trade objects for equity calculation
            trades_obj_by_magic = {}
            for magic, trade_dicts in trades_by_magic.items():
                trades_obj = []
                for td in trade_dicts:
                    trade = Trade(
                        ticket=td.get('ticket', ''),
                        magic_number=td.get('magic_number', 0),
                        time=td.get('time', ''),
                        symbol=td.get('symbol', ''),
                        type=td.get('type', ''),
                        volume=td.get('volume', 0.0),
                        price=td.get('price', 0.0),
                        sl=td.get('sl', 0.0),
                        tp=td.get('tp', 0.0),
                        profit=td.get('profit', 0.0)
                    )
                    trades_obj.append(trade)
                trades_obj_by_magic[magic] = trades_obj
            
            equity_curves_obj = expert_analyzer.calculate_equity_curves(trades_obj_by_magic, initial_balance)
            # Convert to dict format
            for magic, curve in equity_curves_obj.items():
                equity_curves[magic] = [point.to_dict() for point in curve]
        
        # Calculate overall equity curve
        overall_equity = []
        if calculate_equity and trades:
            # Convert all trades to Trade objects
            all_trades_obj = []
            for td in trades:
                trade = Trade(
                    ticket=td.get('ticket', ''),
                    magic_number=td.get('magic_number', 0),
                    time=td.get('time', ''),
                    symbol=td.get('symbol', ''),
                    type=td.get('type', ''),
                    volume=td.get('volume', 0.0),
                    price=td.get('price', 0.0),
                    sl=td.get('sl', 0.0),
                    tp=td.get('tp', 0.0),
                    profit=td.get('profit', 0.0)
                )
                all_trades_obj.append(trade)
            
            overall_curve = parser.calculate_equity_curve(all_trades_obj, initial_balance)
            overall_equity = [point.to_dict() for point in overall_curve]
        
        # Calculate overall metrics
        total_profit = sum(metrics.net_profit for metrics in metrics_by_expert.values())
        
        # Format response
        experts_data = {}
        for magic, metrics in metrics_by_expert.items():
            experts_data[str(magic)] = {
                "name": f"Expert {magic}",
                "magic_number": magic,
                "metrics": metrics.to_dict(),
                "equity_curve": equity_curves.get(magic, [])
            }
        
        logger.info(f"Analyzed {len(experts_data)} experts")
        
        return jsonify({
            "success": True,
            "experts": experts_data,
            "overall": {
                "equity_curve": overall_equity,
                "total_profit": total_profit,
                "experts_count": len(experts_data)
            }
        })
        
    except Exception as e:
        logger.exception("Error analyzing experts")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/experts/equity-curve', methods=['POST'])
def get_equity_curves():
    """
    Get equity curves for selected experts
    
    Expected JSON body:
    {
        "trades": [...],
        "magic_numbers": [12345, 67890],
        "initial_balance": 10000
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        trades = data.get('trades', [])
        magic_numbers = data.get('magic_numbers', [])
        initial_balance = float(data.get('initial_balance', 10000))
        
        if not trades:
            return jsonify({"success": False, "error": "No trades provided"}), 400
        
        # Group trades by magic number
        trades_by_magic = expert_analyzer.group_by_magic_from_dict(trades)
        
        # Filter by requested magic numbers if provided
        if magic_numbers:
            trades_by_magic = {k: v for k, v in trades_by_magic.items() if k in magic_numbers}
        
        # Convert dict trades to Trade objects
        trades_obj_by_magic = {}
        for magic, trade_dicts in trades_by_magic.items():
            trades_obj = []
            for td in trade_dicts:
                trade = Trade(
                    ticket=td.get('ticket', ''),
                    magic_number=td.get('magic_number', 0),
                    time=td.get('time', ''),
                    symbol=td.get('symbol', ''),
                    type=td.get('type', ''),
                    volume=td.get('volume', 0.0),
                    price=td.get('price', 0.0),
                    sl=td.get('sl', 0.0),
                    tp=td.get('tp', 0.0),
                    profit=td.get('profit', 0.0)
                )
                trades_obj.append(trade)
            trades_obj_by_magic[magic] = trades_obj
        
        # Calculate equity curves
        equity_curves_obj = expert_analyzer.calculate_equity_curves(trades_obj_by_magic, initial_balance)
        
        # Convert to dict format
        equity_curves = {}
        for magic, curve in equity_curves_obj.items():
            equity_curves[str(magic)] = [point.to_dict() for point in curve]
        
        logger.info(f"Generated equity curves for {len(equity_curves)} experts")
        
        return jsonify({
            "success": True,
            "equity_curves": equity_curves
        })
        
    except Exception as e:
        logger.exception("Error generating equity curves")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/experts/metrics', methods=['GET', 'POST'])
def get_expert_metrics():
    """
    Get metrics for all experts or specific expert
    
    Query params (GET): ?magic_number=12345
    Or POST with JSON: {"trades": [...], "initial_balance": 10000}
    """
    try:
        if request.method == 'POST':
            data = request.get_json()
            
            if not data:
                return jsonify({"success": False, "error": "No data provided"}), 400
            
            trades = data.get('trades', [])
            initial_balance = float(data.get('initial_balance', 10000))
            
            if not trades:
                return jsonify({"success": False, "error": "No trades provided"}), 400
            
            # Group trades and calculate metrics
            trades_by_magic = expert_analyzer.group_by_magic_from_dict(trades)
            metrics_by_expert = expert_analyzer.calculate_metrics_from_dict(trades_by_magic, initial_balance)
            
            # Convert to dict format
            metrics_dict = {}
            for magic, metrics in metrics_by_expert.items():
                metrics_dict[str(magic)] = metrics.to_dict()
            
            return jsonify({
                "success": True,
                "metrics": metrics_dict
            })
        
        else:  # GET request
            magic_number = request.args.get('magic_number', type=int)
            
            if magic_number is not None:
                # Get specific expert from cache
                if magic_number in expert_analyzer.experts_cache:
                    metrics = expert_analyzer.experts_cache[magic_number]
                    return jsonify({
                        "success": True,
                        "metrics": metrics.to_dict()
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": f"Expert {magic_number} not found in cache"
                    }), 404
            else:
                # Get all experts from cache
                metrics_dict = {}
                for magic, metrics in expert_analyzer.experts_cache.items():
                    metrics_dict[str(magic)] = metrics.to_dict()
                
                return jsonify({
                    "success": True,
                    "metrics": metrics_dict
                })
        
    except Exception as e:
        logger.exception("Error getting expert metrics")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/experts/compare', methods=['POST'])
def compare_experts():
    """
    Compare multiple experts
    
    Expected JSON body:
    {
        "expert_ids": [12345, 67890],
        "trades": [...],
        "initial_balance": 10000
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        expert_ids = data.get('expert_ids', [])
        trades = data.get('trades')
        initial_balance = float(data.get('initial_balance', 10000))
        
        if not expert_ids:
            return jsonify({"success": False, "error": "No expert IDs provided"}), 400
        
        # If trades provided, calculate metrics first
        if trades:
            trades_by_magic = expert_analyzer.group_by_magic_from_dict(trades)
            expert_analyzer.calculate_metrics_from_dict(trades_by_magic, initial_balance)
        
        # Compare experts
        comparison = expert_analyzer.compare_experts(expert_ids)
        
        logger.info(f"Compared {len(expert_ids)} experts")
        
        return jsonify({
            "success": True,
            "comparison": comparison.to_dict()
        })
        
    except Exception as e:
        logger.exception("Error comparing experts")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
