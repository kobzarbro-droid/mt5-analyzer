# Quick Start Guide - MT5 Portfolio Analyzer

## 🚀 Get Started in 5 Minutes

### Option 1: Test Mode (No API Key Required)

Perfect for trying out the system without an OpenAI API key.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the mock API server:**
   ```bash
   cd backend
   PORT=5001 python api_test_mock.py
   ```

3. **Open the test UI:**
   - Open `frontend/index_test.html` in your web browser
   - Or serve it: `cd frontend && python -m http.server 8000`
   - Navigate to: `http://localhost:8000/index_test.html`

4. **Try it out:**
   - Click "Load Sample Data" to populate 5 example strategies
   - Click "🔍 Analyze Portfolio" to see AI analysis
   - View results in the modal popup

### Option 2: Production Mode (Real OpenAI API)

For real AI-powered analysis using GPT-4o.

1. **Get OpenAI API Key:**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Create an API key in your account settings

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend:**
   ```bash
   cd backend
   python api.py
   ```

5. **Open the UI:**
   - Open `frontend/index.html` in your web browser
   - Or serve it: `cd frontend && python -m http.server 8000`
   - Navigate to: `http://localhost:8000`

## 📊 Using the Application

### Input Your Data

1. **Add Strategies**: Click "+ Add Strategy" (up to 5)
2. **Fill in Metrics** for each strategy:
   - **Name**: Your strategy identifier
   - **Equity**: Current account balance/equity
   - **Drawdown (%)**: Maximum drawdown (negative number, e.g., -15.5)
   - **Correlation**: Correlation coefficient (0-1, e.g., 0.65)
   - **Recovery Factor**: Recovery metric (e.g., 2.3)
   - **Profit (%)**: Total profit percentage (e.g., 45.2)

### Analyze

3. **Click "🔍 Analyze Portfolio"**
   - The system sends your data to AI
   - Wait a few seconds for analysis

### View Results

4. **Review AI Recommendations** in the popup:
   - Overall portfolio assessment
   - Strategy recommendations (which to prioritize/reduce)
   - Strengths and weaknesses
   - Risk analysis
   - 5 actionable recommendations

### Export

5. **Click "Export Analysis"** to save as JSON

## 📝 Example Data

Here's sample data you can use to test:

**Strategy 1: Trend Following**
- Equity: 125000
- Drawdown: -12.5
- Correlation: 0.45
- Recovery: 2.8
- Profit: 25.0

**Strategy 2: Mean Reversion**
- Equity: 98000
- Drawdown: -18.2
- Correlation: 0.32
- Recovery: 1.9
- Profit: -2.0

**Strategy 3: Breakout**
- Equity: 142000
- Drawdown: -10.1
- Correlation: 0.55
- Recovery: 3.2
- Profit: 42.0

Or just click "Load Sample Data" button! 😊

## 🔧 API Testing

Test the backend API directly:

```bash
# Health check
curl http://localhost:5000/health

# Analyze portfolio
curl -X POST http://localhost:5000/api/portfolio/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "strategies": [
      {
        "name": "Test Strategy",
        "equity": 100000,
        "drawdown": -10.5,
        "correlation": 0.6,
        "recovery": 2.5,
        "profit": 30.0
      }
    ]
  }'
```

## ❓ Troubleshooting

**Q: "OpenAI API key not provided" error**
- A: Make sure `.env` file exists with valid `OPENAI_API_KEY`

**Q: Frontend can't connect to backend**
- A: Verify backend is running on port 5000 (or 5001 for test mode)
- A: Check if frontend is trying to connect to the correct URL in `app.js`

**Q: CORS errors in browser**
- A: Ensure Flask-CORS is installed: `pip install flask-cors`

**Q: Want to test without paying for OpenAI API?**
- A: Use Test Mode (Option 1) with the mock API!

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [README_RU.md](README_RU.md) for Russian documentation
- Review the code in `backend/portfolio_analyzer.py` to understand the AI integration
- Customize the UI in `frontend/static/styles.css`

## 💡 Tips

- Start with sample data to understand the output format
- The AI provides different insights each time (temperature=0.7)
- Export your analyses to track changes over time
- Correlation closer to 1 means strategies are more similar
- Recovery factor > 2.0 is generally considered good

## 🆕 MT5 Report Analysis & Optimization (New Features!)

### Quick Start: Analyze MT5 Optimization Reports

1. **Navigate to "MT5 Reports & Optimization" tab**

2. **Upload Your Reports:**
   - **Optimization Report**: Click "Upload Optimization" and select your MT5 optimization results file (XML or HTML)
   - **Forward Test Report** (optional): Upload forward test results for validation

3. **Set Filter Criteria:**
   - Min Profit: Minimum profit threshold (e.g., 1000)
   - Min Profit Factor: Minimum PF (e.g., 1.5)
   - Min Trades: Minimum number of trades (e.g., 10)
   - Max Drawdown: Maximum acceptable drawdown % (optional)
   - Top N Results: How many top results to show (default: 10)

4. **Find Best Parameters:**
   - Click "Apply Filters & Find Best"
   - Review the top-performing parameter sets
   - See profit, trades, profit factor, drawdown, Sharpe ratio for each

5. **Get AI Recommendations:**
   - Select parameter sets you're interested in (checkbox)
   - Click "🤖 Get GPT Recommendations"
   - AI analyzes which parameters are most promising

6. **Save as Presets:**
   - Click "💾 Save as Preset" on any parameter set
   - Give it a meaningful name
   - Download .set file for MT5

### Managing Presets

1. **Switch to "Presets & Comparison" tab**

2. **View All Presets:**
   - See all saved presets with their optimization metrics
   - Green badge = has backtest data, Yellow badge = no backtest yet

3. **Upload Backtest Results:**
   - After running a backtest in MT5, save the report as HTML
   - Click "📊 Upload Backtest" for the preset
   - Upload the HTML backtest report
   - Preset now shows actual performance data

4. **Compare Multiple Presets:**
   - Select 2+ presets using checkboxes
   - Click "Compare Selected"
   - View side-by-side metrics
   - See interactive charts comparing performance

5. **Get AI Comparison:**
   - With presets selected, click "🤖 Get GPT Analysis"
   - AI provides detailed comparative analysis
   - Get recommendations on which preset to use for live trading

6. **Download .set Files:**
   - Click "⬇️ Download .set" for any preset
   - Load the .set file in MT5 Strategy Tester
   - Run backtest with those exact parameters

### MT5 Report Formats Supported

- **Optimization Reports**: XML or HTML format from MT5 Strategy Tester
- **Forward Test Reports**: Same format as optimization
- **Backtest Reports**: HTML format from MT5 Strategy Tester

### Example Workflow

1. Run optimization in MT5 → Save results → Upload to analyzer
2. Filter to find top 10 parameter sets
3. Get GPT recommendations on best sets
4. Save top 3-5 sets as presets
5. Download .set files and run backtests in MT5
6. Upload backtest results to each preset
7. Compare all presets side-by-side
8. Get GPT analysis to choose the best for live trading

---

Happy Analyzing! 🎯📈
