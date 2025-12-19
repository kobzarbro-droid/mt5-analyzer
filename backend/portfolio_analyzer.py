"""
Portfolio Analyzer Module for MT5 Analysis
Provides AI-powered portfolio analysis using OpenAI API
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
MAX_STRATEGIES = 10
MIN_STRATEGIES = 1
MIN_CORRELATION = -1.0
MAX_CORRELATION = 1.0


@dataclass
class StrategyMetrics:
    """Metrics for a single trading strategy"""
    name: str
    equity: float
    drawdown: float
    correlation: float
    recovery: float
    profit: float
    
    def __post_init__(self):
        """Validate strategy metrics after initialization"""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Strategy name must be a non-empty string")
        
        if self.equity < 0:
            raise ValueError(f"Equity must be non-negative, got {self.equity}")
        
        if self.drawdown > 0:
            raise ValueError(f"Drawdown must be negative or zero, got {self.drawdown}")
        
        if not MIN_CORRELATION <= self.correlation <= MAX_CORRELATION:
            raise ValueError(f"Correlation must be between {MIN_CORRELATION} and {MAX_CORRELATION}, got {self.correlation}")
        
        if self.recovery < 0:
            raise ValueError(f"Recovery factor must be non-negative, got {self.recovery}")
        
        logger.debug(f"Validated strategy metrics for: {self.name}")


@dataclass
class PortfolioAnalysisRequest:
    """Request data for portfolio analysis"""
    strategies: List[StrategyMetrics]
    
    def __post_init__(self):
        """Validate portfolio request after initialization"""
        if len(self.strategies) < MIN_STRATEGIES:
            raise ValueError(f"At least {MIN_STRATEGIES} strategy is required")
        
        if len(self.strategies) > MAX_STRATEGIES:
            raise ValueError(f"Maximum {MAX_STRATEGIES} strategies allowed, got {len(self.strategies)}")
        
        logger.info(f"Portfolio analysis request created with {len(self.strategies)} strategies")


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
            logger.error("OpenAI API key not provided")
            raise ValueError("OpenAI API key not provided")
        
        logger.info("PortfolioAnalyzer initialized successfully")
    
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
        start_time = datetime.now()
        logger.info(f"Starting portfolio analysis for {len(portfolio.strategies)} strategies")
        
        try:
            import openai
            
            # Set API key
            openai.api_key = self.api_key
            
            # Create prompt
            prompt = self.create_analysis_prompt(portfolio)
            logger.debug(f"Created analysis prompt with {len(prompt)} characters")
            
            # Call OpenAI API (GPT-4o)
            logger.info("Sending request to OpenAI API")
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
            elapsed_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Analysis completed successfully in {elapsed_time:.2f} seconds")
            logger.debug(f"Response length: {len(analysis_text)} characters")
            
            return {
                "success": True,
                "analysis": analysis_text,
                "strategies_analyzed": len(portfolio.strategies),
                "model_used": "gpt-4o",
                "timestamp": datetime.now().isoformat(),
                "processing_time": elapsed_time
            }
            
        except Exception as e:
            elapsed_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Analysis failed after {elapsed_time:.2f} seconds: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "analysis": None,
                "timestamp": datetime.now().isoformat()
            }
    
    def format_for_display(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format analysis result for UI display
        
        Args:
            analysis_result: Raw analysis result from OpenAI
            
        Returns:
            Formatted result ready for UI consumption
        """
        logger.debug("Formatting analysis result for display")
        
        if not analysis_result.get("success"):
            logger.warning("Formatting failed analysis result")
            return {
                "success": False,
                "error": analysis_result.get("error", "Unknown error"),
                "recommendations": [],
                "strengths": [],
                "weaknesses": [],
                "summary": "Analysis failed",
                "timestamp": analysis_result.get("timestamp", datetime.now().isoformat())
            }
        
        # Parse the analysis text (basic parsing, can be enhanced)
        analysis_text = analysis_result.get("analysis", "")
        
        result = {
            "success": True,
            "full_analysis": analysis_text,
            "strategies_count": analysis_result.get("strategies_analyzed", 0),
            "model": analysis_result.get("model_used", "gpt-4o"),
            "timestamp": analysis_result.get("timestamp", datetime.now().isoformat()),
            "processing_time": analysis_result.get("processing_time")
        }
        
        logger.info("Analysis result formatted successfully")
        return result
