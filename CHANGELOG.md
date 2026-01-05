# Changelog

All notable changes to the MT5 Portfolio Analyzer project will be documented in this file.

## [2.0.0] - 2026-01 - Expert Dashboard Release 🚀

### Added - Major Features

#### Expert Performance Dashboard
- **Magic Number Support**: Automatically detect and group trades by expert magic number
- **Interactive Equity Curves**: Real-time Chart.js visualizations with zoom, pan, and tooltips
- **Overall Performance View**: Combined equity curve showing performance across all experts
- **Individual Expert Analysis**: Detailed cards for each expert with comprehensive metrics
- **Expert Comparison**: Overlay multiple expert equity curves for side-by-side comparison
- **Smart Filtering**: Filter experts by magic number, date range, and trading symbol
- **Dynamic Sorting**: Sort experts by profit, win rate, trades, profit factor, or recovery factor

#### Backend Infrastructure
- New `expert_analyzer.py` module with `ExpertAnalyzer` class
  - `group_by_magic()`: Group trades by magic number
  - `calculate_metrics_by_expert()`: Comprehensive metrics calculation
  - `calculate_equity_curves()`: Generate equity curves for each expert
  - `compare_experts()`: Compare multiple experts
- Enhanced data models:
  - `Trade` dataclass with magic_number support
  - `EquityPoint` dataclass for equity curve tracking
  - `ExpertMetrics` dataclass with 15+ performance metrics
  - `ComparisonResult` dataclass for expert comparisons
- Updated `MT5Parser`:
  - Extract magic_number from backtest reports
  - `calculate_equity_curve()` method for trade sequence analysis
  - Enhanced trade parsing with SL/TP levels

#### New API Endpoints
- `POST /api/experts/analyze`: Analyze experts from backtest with magic number grouping
- `POST /api/experts/equity-curve`: Get equity curves for selected experts
- `GET /api/experts/metrics`: Retrieve expert performance metrics
- `POST /api/experts/compare`: Compare multiple experts

#### Expert Metrics
- Net Profit & Total Loss
- Win Rate (%)
- Profit Factor
- Average Profit/Loss per Trade
- Maximum Drawdown ($ and %)
- Recovery Factor
- Sharpe Ratio
- Total Trades (profit/loss breakdown)
- Unique Symbols Traded

#### Docker & Deployment
- Complete Docker containerization
  - `Dockerfile` for Python/Flask backend
  - `docker-compose.yml` orchestrating full stack
  - Nginx reverse proxy for frontend
  - Health checks for all services
  - Volume persistence for presets
- Production-ready configuration
  - Nginx with gzip compression
  - CORS handling
  - Security headers
  - SSL/TLS ready
- One-command deployment: `docker-compose up -d`

### Changed

#### Frontend Enhancements
- Added 4th tab: "Expert Dashboard"
- Updated API URL handling for Docker/production environments
- Fixed `presetsList` variable naming conflict bug
- Enhanced Chart.js integration with multiple chart types
- Responsive CSS for mobile devices
- New dashboard-specific styling with cards, metrics, and comparison views

#### Backend Improvements
- Enhanced trade parsing to extract magic numbers from various report formats
- Improved equity curve calculation with datetime handling
- Better error handling and logging throughout expert analysis

#### Documentation
- Comprehensive `DOCKER.md` setup guide
- Updated `README.md` with Expert Dashboard features
- Added Docker quick start instructions
- Enhanced usage workflows with Expert Dashboard examples

### Technical Details

#### Architecture
```
mt5-analyzer/
├── backend/
│   ├── expert_analyzer.py  (NEW - 350+ lines)
│   ├── mt5_parser.py       (UPDATED - magic number support)
│   └── api.py             (UPDATED - 4 new endpoints)
├── frontend/
│   ├── index.html         (UPDATED - dashboard tab)
│   └── static/
│       ├── app_enhanced.js (UPDATED - 600+ lines of dashboard code)
│       └── styles.css      (UPDATED - 300+ lines of dashboard styles)
├── Dockerfile             (NEW)
├── docker-compose.yml     (NEW)
├── nginx.conf            (NEW)
└── DOCKER.md             (NEW)
```

#### Performance
- Efficient equity curve calculation with sorted trades
- Lazy chart rendering with `setTimeout` to avoid blocking UI
- Optimized Chart.js configuration for large datasets
- Memory-efficient expert caching

### Security
- Input validation on all new endpoints
- Secure trade data parsing with error handling
- Docker security best practices
- Nginx security headers implementation

### Bug Fixes
- Fixed presetsList variable shadowing issue
- Improved error handling in file upload
- Better validation of magic number data
- Fixed API URL handling for different deployment scenarios

## [1.1.0] - Unreleased

### Added
- Comprehensive input validation for all strategy metrics
  - Equity must be non-negative
  - Drawdown must be negative or zero
  - Correlation must be between -1 and 1
  - Recovery factor must be non-negative
  - Strategy name must be a non-empty string
- Portfolio-level validation
  - Minimum 1 strategy required
  - Maximum 10 strategies allowed
- Logging system throughout the application
  - API request/response logging
  - Error tracking and debugging information
  - Performance metrics logging
- Timestamp tracking for all analyses
  - Analysis timestamp in ISO format
  - Processing time in seconds
  - Display in UI with formatted date/time
- Enhanced error messages
  - More specific validation error messages
  - Better error context (e.g., "at index N")
  - Improved debugging information
- Improved export functionality
  - Export timestamp separate from analysis timestamp
  - Processing time included in export
  - Better metadata in exported JSON files
- Comprehensive validation test suite
  - Tests for all validation rules
  - Boundary value testing
  - Error message verification

### Changed
- Updated StrategyMetrics dataclass to include post-initialization validation
- Updated PortfolioAnalysisRequest to validate strategy count
- Enhanced API error responses to include timestamps
- Improved frontend display with timestamp and processing time information
- Updated export format to include more metadata

### Technical Details

#### Backend Changes
- `portfolio_analyzer.py`:
  - Added logging configuration
  - Implemented `__post_init__` validation methods
  - Added timestamp and processing time tracking
  - Enhanced error handling with contextual information
  
- `api.py`:
  - Added logging throughout request handling
  - Improved error messages with request context
  - Better exception handling and logging

- `api_test_mock.py`:
  - Added timestamp support
  - Added processing time simulation
  - Consistent error response format

#### Frontend Changes
- `app.js` and `app_test.js`:
  - Display analysis timestamp in readable format
  - Show processing time when available
  - Enhanced export with additional metadata
  - Improved error message display

#### Testing
- New `test_validation.py` with comprehensive validation tests:
  - Valid input testing
  - Invalid input rejection testing
  - Boundary value testing
  - Error message verification

### Security
- Input validation prevents invalid data from being processed
- Better error messages without exposing sensitive information
- Logging helps track potential security issues

## [1.0.0] - 2024-12

### Added
- Initial release of MT5 Portfolio Analyzer
- AI-powered portfolio analysis using GPT-4o
- Flask REST API backend
- Interactive web frontend
- Support for up to 5 strategies
- Mock API for testing without OpenAI API key
- Comprehensive documentation
- Sample data loading
- JSON export functionality
