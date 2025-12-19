"""
Portfolio Analyzer Module for MT5 Analysis
Provides AI-powered portfolio analysis using OpenAI API
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import json


@dataclass
class StrategyMetrics:
    """Metrics for a single trading strategy"""
    name: str
    equity: float
    drawdown: float
    correlation: float
    recovery: float
    profit: float


@dataclass
class PortfolioAnalysisRequest:
    """Request data for portfolio analysis"""
    strategies: List[StrategyMetrics]


class PortfolioAnalyzer:
    """Analyzes portfolio of trading strategies using AI"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer with OpenAI API key
        
        Args:
            api_key: OpenAI API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
    
    def create_analysis_prompt(self, portfolio: PortfolioAnalysisRequest) -> str:
        """
        Create a detailed prompt for GPT-4o analysis
        
        Args:
            portfolio: Portfolio analysis request with strategy metrics
            
        Returns:
            Formatted prompt string for OpenAI API
        """
        strategies_text = ""
        for i, strategy in enumerate(portfolio.strategies, 1):
            strategies_text += f"""
Strategy {i}: {strategy.name}
- Equity: {strategy.equity}
- Drawdown: {strategy.drawdown}%
- Correlation: {strategy.correlation}
- Recovery Factor: {strategy.recovery}
- Profit: {strategy.profit}%
"""
        
        prompt = f"""Analyze the following MT5 trading portfolio with {len(portfolio.strategies)} strategies:

{strategies_text}

Please provide a comprehensive portfolio analysis including:

1. **Overall Portfolio Assessment**: Evaluate the portfolio's performance, risk profile, and diversification.

2. **Strategy Recommendations**: 
   - Which strategies should be prioritized?
   - Which strategies might be underperforming?
   - Optimal allocation suggestions

3. **Strengths**: Identify the strongest aspects of this portfolio.

4. **Weaknesses**: Identify potential risks or weaknesses.

5. **Risk Analysis**: Evaluate drawdown levels, correlation between strategies, and overall risk exposure.

6. **Actionable Recommendations**: Provide 3-5 specific actions to improve portfolio performance.

Format your response in a clear, structured manner suitable for display in a dashboard."""
        
        return prompt
    
    def analyze_portfolio(self, portfolio: PortfolioAnalysisRequest) -> Dict[str, Any]:
        """
        Send portfolio data to OpenAI API and get analysis
        
        Args:
            portfolio: Portfolio analysis request with strategy metrics
            
        Returns:
            Dictionary containing AI analysis results
        """
        try:
            import openai
            
            # Set API key
            openai.api_key = self.api_key
            
            # Create prompt
            prompt = self.create_analysis_prompt(portfolio)
            
            # Call OpenAI API (GPT-4o)
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial analyst specializing in trading portfolio analysis and risk management. Provide detailed, actionable insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract response
            analysis_text = response.choices[0].message.content
            
            return {
                "success": True,
                "analysis": analysis_text,
                "strategies_analyzed": len(portfolio.strategies),
                "model_used": "gpt-4o"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": None
            }
    
    def format_for_display(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format analysis result for UI display
        
        Args:
            analysis_result: Raw analysis result from OpenAI
            
        Returns:
            Formatted result ready for UI consumption
        """
        if not analysis_result.get("success"):
            return {
                "success": False,
                "error": analysis_result.get("error", "Unknown error"),
                "recommendations": [],
                "strengths": [],
                "weaknesses": [],
                "summary": "Analysis failed"
            }
        
        # Parse the analysis text (basic parsing, can be enhanced)
        analysis_text = analysis_result.get("analysis", "")
        
        return {
            "success": True,
            "full_analysis": analysis_text,
            "strategies_count": analysis_result.get("strategies_analyzed", 0),
            "model": analysis_result.get("model_used", "gpt-4o"),
            "timestamp": None  # Can add timestamp if needed
        }
