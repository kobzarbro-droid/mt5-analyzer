# Changelog

All notable changes to the MT5 Portfolio Analyzer project will be documented in this file.

## [Unreleased]

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
