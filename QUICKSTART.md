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

---

Happy Analyzing! 🎯📈
