# MT5 Portfolio Analyzer 🤖

AI-powered portfolio analysis tool for MetaTrader 5 (MT5) trading strategies. This application uses OpenAI's GPT-4o to provide comprehensive analysis, recommendations, and insights for trading portfolios.

## Features

- **AI Portfolio Analysis**: Leverage GPT-4o to analyze up to 10 trading strategies
- **Comprehensive Metrics**: Track Equity, Drawdown, Correlation, Recovery Factor, and Profit
- **Smart Recommendations**: Get actionable insights on strategy optimization
- **Risk Assessment**: Identify strengths, weaknesses, and risk exposure
- **Interactive UI**: Modern web interface with modal-based result display
- **Data Export**: Export analysis results as JSON with timestamps and metadata
- **Input Validation**: Comprehensive validation ensures data quality and security
- **Logging & Monitoring**: Track API usage, errors, and performance metrics
- **Timestamp Tracking**: Every analysis includes timestamp and processing time

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

### Basic Workflow

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

## Project Structure

```
mt5-analyzer/
├── backend/
│   ├── __init__.py
│   ├── api.py                    # Flask REST API (production)
│   ├── api_test_mock.py          # Mock API for testing
│   ├── portfolio_analyzer.py     # Core analysis logic with validation
│   ├── test_api.py               # Unit tests
│   └── test_validation.py        # Validation tests
├── frontend/
│   ├── index.html                # Main UI (production)
│   ├── index_test.html           # Test UI
│   └── static/
│       ├── app.js                # Frontend JavaScript (production)
│       ├── app_test.js           # Test mode JavaScript
│       └── styles.css            # UI styles
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── SECURITY.md                   # Security guidelines
├── CHANGELOG.md                  # Version history
├── QUICKSTART.md                 # Quick start guide
└── IMPLEMENTATION_NOTES.md       # Technical details
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