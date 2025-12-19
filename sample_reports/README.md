# Sample MT5 Reports

This directory contains sample MT5 reports for testing the analyzer.

## Files

- `optimization_sample.xml` - Sample optimization report in XML format
  - Contains 5 optimization passes with different parameters
  - Shows profit, trades, profit factor, Sharpe ratio, etc.

## How to Use

1. Start the backend server:
   ```bash
   cd backend
   python api.py
   ```

2. Open the frontend in your browser:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Navigate to http://localhost:8000

3. Go to "MT5 Reports & Optimization" tab

4. Upload `optimization_sample.xml` as the optimization report

5. Try different filter settings to find best parameters

6. Get GPT recommendations and save presets

## Creating Your Own Reports

### From MT5 Strategy Tester:

1. **Optimization Report:**
   - Run optimization in MT5 Strategy Tester
   - Right-click on results → "Save as Report"
   - Choose XML or HTML format
   - Upload to the analyzer

2. **Backtest Report:**
   - Run a single backtest with specific parameters
   - Right-click → "Save as Report"
   - Choose HTML format
   - Upload when associating with a preset

## Report Format

The XML optimization report should have this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<OptimizationReport>
    <Row Pass="1">
        <Parameter name="ParamName">value</Parameter>
        <Result>profit</Result>
        <Trades>number</Trades>
        <ProfitFactor>value</ProfitFactor>
        <!-- other metrics -->
    </Row>
    <!-- more rows -->
</OptimizationReport>
```

HTML format is also supported - the parser will extract the same information from HTML tables.
