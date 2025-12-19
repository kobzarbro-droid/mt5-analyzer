# MT5 Portfolio Analyzer 🤖

AI-powered portfolio analysis tool for MetaTrader 5 (MT5) trading strategies. This application uses OpenAI's GPT-4o to provide comprehensive analysis, recommendations, and insights for trading portfolios, plus powerful MT5 optimization report analysis and preset management.

## Features

### Portfolio Analysis
- **AI Portfolio Analysis**: Leverage GPT-4o to analyze up to 10 trading strategies
- **Comprehensive Metrics**: Track Equity, Drawdown, Correlation, Recovery Factor, and Profit
- **Smart Recommendations**: Get actionable insights on strategy optimization
- **Risk Assessment**: Identify strengths, weaknesses, and risk exposure
- **Data Export**: Export analysis results as JSON with timestamps and metadata

### MT5 Report Analysis (New!)
- **Upload Optimization Reports**: Parse MT5 optimization results (XML/HTML)
- **Upload Forward Test Reports**: Validate parameters with forward testing data
- **Best Parameter Finder**: Automatically identify top-performing parameter sets
- **Advanced Filtering**: Filter by profit, profit factor, trades, drawdown, Sharpe ratio
- **GPT Parameter Recommendations**: Get AI insights on which parameters to use

### Preset Management (New!)
- **Save Presets**: Convert parameter sets to reusable presets
- **Download .set Files**: Export presets as MT5 .set files for quick loading
- **Upload Backtest Reports**: Associate backtest results with each preset
- **Compare Multiple Presets**: Side-by-side comparison with charts
- **GPT Comparative Analysis**: AI-powered recommendations on best presets

### Technical Features
- **Interactive UI**: Modern tabbed interface with modal-based result display
- **Input Validation**: Comprehensive validation ensures data quality and security
- **Logging & Monitoring**: Track API usage, errors, and performance metrics
- **Timestamp Tracking**: Every analysis includes timestamp and processing time
- **Chart Visualization**: Interactive charts for comparing presets

## Architecture

The application consists of two main components:

1. **Backend (Python/Flask)**: REST API for OpenAI integration and portfolio analysis
2. **Frontend (HTML/CSS/JavaScript)**: Interactive web interface for data input and visualization

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/kobzarbro-droid/mt5-analyzer.git
   cd mt5-analyzer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the backend server**
   ```bash
   cd backend
   python api.py
   ```
   
   The API will start on `http://localhost:5000`

5. **Open the frontend**
   
   Open `frontend/index.html` in your web browser, or serve it with a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   
   Then navigate to `http://localhost:8000`

## Usage

### Portfolio Analysis Workflow

1. **Add Strategies**: Click "Add Strategy" to add up to 5 trading strategies
2. **Enter Metrics**: Fill in the metrics for each strategy:
   - **Name**: Strategy identifier
   - **Equity**: Current equity value
   - **Drawdown**: Maximum drawdown percentage
   - **Correlation**: Correlation coefficient with other strategies
   - **Recovery Factor**: Recovery factor metric
   - **Profit**: Total profit percentage

3. **Analyze**: Click "Analyze Portfolio" to send data to AI
4. **Review Results**: Analysis appears in a modal with:
   - Overall portfolio assessment
   - Strategy recommendations
   - Strengths and weaknesses
   - Risk analysis
   - Actionable recommendations

5. **Export**: Save the analysis as JSON for future reference

### MT5 Report Analysis Workflow

1. **Upload Reports**: 
   - Navigate to "MT5 Reports & Optimization" tab
   - Upload your optimization report (XML or HTML format)
   - Optionally upload forward test report for validation

2. **Filter Parameters**:
   - Set minimum profit, profit factor, and number of trades
   - Set maximum drawdown threshold
   - Choose how many top results to display

3. **Find Best Parameters**:
   - Click "Apply Filters & Find Best"
   - Review the top-performing parameter sets
   - Select multiple sets for comparison

4. **Get AI Recommendations**:
   - Select parameter sets of interest
   - Click "Get GPT Recommendations"
   - Review AI analysis of which parameters are best

5. **Save as Presets**:
   - Click "Save as Preset" on any parameter set
   - Download .set file for use in MT5 tester

### Preset Management Workflow

1. **View Presets**:
   - Navigate to "Presets & Comparison" tab
   - See all saved presets with their metrics

2. **Upload Backtest Results**:
   - Click "Upload Backtest" for any preset
   - Upload the HTML backtest report from MT5
   - Preset is updated with actual performance data

3. **Compare Presets**:
   - Select 2 or more presets using checkboxes
   - Click "Compare Selected"
   - View comparison charts and metrics

4. **Get AI Comparison**:
   - With presets selected, click "Get GPT Analysis"
   - Receive detailed AI recommendations on which preset to use

5. **Download .set Files**:
   - Click "Download .set" for any preset
   - Load the file in MT5 Strategy Tester

### Sample Data

Click "Load Sample Data" to populate the form with example strategies for testing.

## API Documentation

### Endpoints

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "MT5 Portfolio Analyzer"
}
```

#### `POST /api/portfolio/analyze`
Analyze a portfolio of strategies.

**Request Body:**
```json
{
  "strategies": [
    {
      "name": "Strategy 1",
      "equity": 150000,
      "drawdown": -15.5,
      "correlation": 0.65,
      "recovery": 2.3,
      "profit": 45.2
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "full_analysis": "Detailed AI analysis text...",
  "strategies_count": 5,
  "model": "gpt-4o"
}
```

#### `GET /api/portfolio/test`
Test endpoint with pre-loaded sample data.

### New MT5 Report Endpoints

#### `POST /api/upload/optimization`
Upload and parse MT5 optimization report.

**Form Data:**
- `file`: Optimization report file (XML or HTML)

**Response:**
```json
{
  "success": true,
  "results_count": 100,
  "results": [
    {
      "pass_number": 1,
      "parameters": {"StopLoss": 50, "TakeProfit": 100},
      "profit": 1250.50,
      "total_trades": 45,
      "profit_factor": 1.85,
      "sharpe_ratio": 1.45
    }
  ]
}
```

#### `POST /api/upload/forward`
Upload and parse MT5 forward test report (same format as optimization).

#### `POST /api/upload/backtest`
Upload MT5 backtest report and associate with a preset.

**Form Data:**
- `file`: Backtest report HTML file
- `preset_id`: ID of the preset to update

**Response:**
```json
{
  "success": true,
  "preset_id": "preset_1_123456",
  "report": {
    "total_net_profit": 1500.00,
    "profit_factor": 2.0,
    "maximal_drawdown": 200.00,
    "total_trades": 50
  }
}
```

#### `POST /api/analyze/best-parameters`
Find best parameter sets from optimization results.

**Request Body:**
```json
{
  "optimization_results": [...],
  "forward_results": [...],
  "criteria": {
    "min_profit": 1000,
    "min_profit_factor": 1.5,
    "min_trades": 10,
    "max_drawdown": 20,
    "top_n": 10
  }
}
```

#### `POST /api/gpt/recommend-parameters`
Get GPT recommendations for parameter sets.

**Request Body:**
```json
{
  "parameter_sets": [...]
}
```

#### `POST /api/preset/create`
Create a new preset from parameters.

**Request Body:**
```json
{
  "name": "My Preset",
  "parameters": {"StopLoss": 50, "TakeProfit": 100},
  "optimization_metrics": {"profit": 1250.50}
}
```

#### `GET /api/preset/list`
Get all presets.

#### `GET /api/preset/<preset_id>`
Get a specific preset.

#### `DELETE /api/preset/<preset_id>`
Delete a preset.

#### `GET /api/preset/<preset_id>/download`
Download .set file for a preset.

#### `POST /api/preset/compare`
Compare multiple presets.

**Request Body:**
```json
{
  "preset_ids": ["preset_1", "preset_2"]
}
```

#### `POST /api/gpt/compare-presets`
Get GPT comparative analysis of presets.

**Request Body:**
```json
{
  "preset_ids": ["preset_1", "preset_2"]
}
```

## Project Structure

```
mt5-analyzer/
├── backend/
│   ├── __init__.py
│   ├── api.py                    # Flask REST API with MT5 endpoints
│   ├── portfolio_analyzer.py     # Core portfolio analysis logic
│   ├── mt5_parser.py            # MT5 report parser (NEW)
│   ├── set_file_generator.py   # .set file generator (NEW)
│   ├── preset_manager.py        # Preset management (NEW)
│   ├── test_api.py              # Unit tests
│   ├── test_validation.py       # Validation tests
│   └── test_mt5_integration.py  # MT5 feature tests (NEW)
├── frontend/
│   ├── index.html               # Main UI with tabs (UPDATED)
│   └── static/
│       ├── app_enhanced.js      # Enhanced JavaScript (NEW)
│       ├── app.js               # Original JavaScript
│       └── styles.css           # UI styles (UPDATED)
├── requirements.txt             # Python dependencies (UPDATED)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── SECURITY.md                  # Security guidelines
├── CHANGELOG.md                 # Version history
├── QUICKSTART.md                # Quick start guide
└── IMPLEMENTATION_NOTES.md      # Technical details
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Backend server port (default: 5000)
- `DEBUG`: Enable debug mode (default: False)

### API Configuration

To use a different OpenAI model, modify the `model` parameter in `backend/portfolio_analyzer.py`:

```python
response = openai.chat.completions.create(
    model="gpt-4o",  # Change to "gpt-4-turbo" or other models
    # ...
)
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests (when implemented)
pytest
```

### Code Style

The project follows PEP 8 style guidelines for Python code.

## Security Notes

⚠️ **Important Security Considerations:**

1. Never commit your `.env` file or expose your OpenAI API key
2. Consider implementing rate limiting for production use (see [SECURITY.md](SECURITY.md))
3. ✅ **Comprehensive input validation implemented** - All strategy metrics are validated
4. ✅ **Logging enabled** - API requests and errors are tracked
5. Use HTTPS in production environments
6. Implement authentication for production deployments

For detailed security guidelines and best practices, see **[SECURITY.md](SECURITY.md)**.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

**Issue**: "OpenAI API key not provided"
- **Solution**: Ensure `.env` file exists with valid `OPENAI_API_KEY`

**Issue**: CORS errors in browser
- **Solution**: Ensure Flask-CORS is installed and configured properly

**Issue**: Connection refused on API calls
- **Solution**: Verify backend server is running on correct port

## Roadmap

- [ ] Add user authentication
- [ ] Implement historical analysis tracking
- [ ] Add more visualization charts
- [ ] Support for additional metrics
- [ ] Multi-language support
- [ ] Mobile-responsive improvements

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for MT5 traders**