"""
MT5 Report Parser Module
Parses MT5 optimization, forward test, and backtest reports
"""

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Single optimization result with parameters and metrics"""
    pass_number: int
    parameters: Dict[str, Any]
    profit: float
    total_trades: int
    profit_factor: Optional[float] = None
    expected_payoff: Optional[float] = None
    drawdown: Optional[float] = None
    drawdown_percent: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    recovery_factor: Optional[float] = None
    win_rate: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'pass_number': self.pass_number,
            'parameters': self.parameters,
            'profit': self.profit,
            'total_trades': self.total_trades,
            'profit_factor': self.profit_factor,
            'expected_payoff': self.expected_payoff,
            'drawdown': self.drawdown,
            'drawdown_percent': self.drawdown_percent,
            'sharpe_ratio': self.sharpe_ratio,
            'recovery_factor': self.recovery_factor,
            'win_rate': self.win_rate
        }


@dataclass
class BacktestReport:
    """Backtest report with trades and metrics"""
    initial_deposit: float
    total_net_profit: float
    gross_profit: float
    gross_loss: float
    profit_factor: float
    expected_payoff: float
    absolute_drawdown: float
    maximal_drawdown: float
    relative_drawdown: float
    total_trades: int
    short_positions: int
    long_positions: int
    profit_trades: int
    loss_trades: int
    sharpe_ratio: Optional[float] = None
    recovery_factor: Optional[float] = None
    trades: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'initial_deposit': self.initial_deposit,
            'total_net_profit': self.total_net_profit,
            'gross_profit': self.gross_profit,
            'gross_loss': self.gross_loss,
            'profit_factor': self.profit_factor,
            'expected_payoff': self.expected_payoff,
            'absolute_drawdown': self.absolute_drawdown,
            'maximal_drawdown': self.maximal_drawdown,
            'relative_drawdown': self.relative_drawdown,
            'total_trades': self.total_trades,
            'short_positions': self.short_positions,
            'long_positions': self.long_positions,
            'profit_trades': self.profit_trades,
            'loss_trades': self.loss_trades,
            'sharpe_ratio': self.sharpe_ratio,
            'recovery_factor': self.recovery_factor,
            'win_rate': (self.profit_trades / self.total_trades * 100) if self.total_trades > 0 else 0,
            'trades_count': len(self.trades)
        }


class MT5Parser:
    """Parser for MT5 reports"""
    
    @staticmethod
    def parse_optimization_report(file_content: str, file_type: str = 'xml') -> List[OptimizationResult]:
        """
        Parse MT5 optimization report
        
        Args:
            file_content: Content of the optimization report file
            file_type: Type of file ('xml' or 'html')
            
        Returns:
            List of optimization results
        """
        logger.info(f"Parsing optimization report (type: {file_type})")
        
        try:
            if file_type == 'xml':
                return MT5Parser._parse_optimization_xml(file_content)
            elif file_type == 'html':
                return MT5Parser._parse_optimization_html(file_content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Failed to parse optimization report: {str(e)}")
            raise
    
    @staticmethod
    def _parse_optimization_xml(content: str) -> List[OptimizationResult]:
        """Parse XML format optimization report"""
        results = []
        
        try:
            root = ET.fromstring(content)
            
            for row in root.findall('.//Row'):
                pass_num = int(row.get('Pass', 0))
                parameters = {}
                
                # Parse parameters
                for param in row.findall('Parameter'):
                    param_name = param.get('name', '')
                    param_value = param.text
                    try:
                        param_value = float(param_value) if '.' in param_value else int(param_value)
                    except (ValueError, TypeError):
                        pass
                    parameters[param_name] = param_value
                
                # Parse metrics
                profit = float(row.find('Result').text or 0)
                total_trades = int(row.find('Trades').text or 0)
                profit_factor = row.find('ProfitFactor')
                expected_payoff = row.find('ExpectedPayoff')
                drawdown = row.find('Drawdown')
                sharpe = row.find('Sharpe')
                recovery = row.find('Recovery')
                
                result = OptimizationResult(
                    pass_number=pass_num,
                    parameters=parameters,
                    profit=profit,
                    total_trades=total_trades,
                    profit_factor=float(profit_factor.text) if profit_factor is not None else None,
                    expected_payoff=float(expected_payoff.text) if expected_payoff is not None else None,
                    drawdown=float(drawdown.text) if drawdown is not None else None,
                    sharpe_ratio=float(sharpe.text) if sharpe is not None else None,
                    recovery_factor=float(recovery.text) if recovery is not None else None
                )
                
                results.append(result)
            
            logger.info(f"Parsed {len(results)} optimization results from XML")
            return results
            
        except Exception as e:
            logger.error(f"Error parsing XML optimization report: {str(e)}")
            raise
    
    @staticmethod
    def _parse_optimization_html(content: str) -> List[OptimizationResult]:
        """Parse HTML format optimization report"""
        results = []
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Find the optimization results table
            table = soup.find('table', {'class': 'optimization'}) or soup.find('table')
            
            if not table:
                raise ValueError("No optimization table found in HTML")
            
            headers = []
            rows = table.find_all('tr')
            
            for i, row in enumerate(rows):
                if i == 0:
                    # Parse headers
                    headers = [th.text.strip() for th in row.find_all(['th', 'td'])]
                    continue
                
                cols = row.find_all(['td', 'th'])
                if len(cols) < 2:
                    continue
                
                values = [col.text.strip() for col in cols]
                
                # Extract pass number and parameters
                pass_num = int(values[0]) if values[0].isdigit() else i
                parameters = {}
                
                # Extract profit and trades
                profit = 0
                total_trades = 0
                profit_factor = None
                expected_payoff = None
                drawdown = None
                
                for j, header in enumerate(headers):
                    if j >= len(values):
                        continue
                    
                    value = values[j]
                    
                    if 'profit' in header.lower() and 'factor' not in header.lower():
                        try:
                            profit = float(value.replace(',', '').replace('$', ''))
                        except (ValueError, TypeError):
                            pass
                    elif 'trades' in header.lower():
                        try:
                            total_trades = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif 'profit factor' in header.lower():
                        try:
                            profit_factor = float(value)
                        except (ValueError, TypeError):
                            pass
                    elif 'payoff' in header.lower():
                        try:
                            expected_payoff = float(value.replace(',', '').replace('$', ''))
                        except (ValueError, TypeError):
                            pass
                    elif 'drawdown' in header.lower():
                        try:
                            drawdown = float(value.replace('%', '').replace(',', ''))
                        except (ValueError, TypeError):
                            pass
                    else:
                        # Assume it's a parameter
                        try:
                            param_value = float(value) if '.' in value else int(value)
                        except (ValueError, TypeError):
                            param_value = value
                        parameters[header] = param_value
                
                result = OptimizationResult(
                    pass_number=pass_num,
                    parameters=parameters,
                    profit=profit,
                    total_trades=total_trades,
                    profit_factor=profit_factor,
                    expected_payoff=expected_payoff,
                    drawdown=drawdown
                )
                
                results.append(result)
            
            logger.info(f"Parsed {len(results)} optimization results from HTML")
            return results
            
        except Exception as e:
            logger.error(f"Error parsing HTML optimization report: {str(e)}")
            raise
    
    @staticmethod
    def parse_backtest_report(file_content: str) -> BacktestReport:
        """
        Parse MT5 backtest report (HTML format)
        
        Args:
            file_content: Content of the backtest report HTML file
            
        Returns:
            BacktestReport object
        """
        logger.info("Parsing backtest report")
        
        try:
            soup = BeautifulSoup(file_content, 'html.parser')
            
            # Extract key metrics from the report
            metrics = {}
            
            # Find all table rows with metrics
            for row in soup.find_all('tr'):
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    metrics[key] = value
            
            # Helper function to extract numeric value
            def extract_number(text: str) -> float:
                if not text:
                    return 0.0
                # Remove currency symbols, commas, and extract number
                cleaned = re.sub(r'[^\d.\-]', '', text.replace(',', ''))
                try:
                    return float(cleaned)
                except:
                    return 0.0
            
            # Parse key metrics
            initial_deposit = extract_number(metrics.get('Initial deposit', '0'))
            total_net_profit = extract_number(metrics.get('Total net profit', '0'))
            gross_profit = extract_number(metrics.get('Gross profit', '0'))
            gross_loss = extract_number(metrics.get('Gross loss', '0'))
            profit_factor = extract_number(metrics.get('Profit factor', '0'))
            expected_payoff = extract_number(metrics.get('Expected payoff', '0'))
            absolute_drawdown = extract_number(metrics.get('Absolute drawdown', '0'))
            maximal_drawdown = extract_number(metrics.get('Maximal drawdown', '0'))
            relative_drawdown_str = metrics.get('Relative drawdown', '0')
            relative_drawdown = extract_number(relative_drawdown_str.split('(')[0] if '(' in relative_drawdown_str else relative_drawdown_str)
            
            total_trades = int(extract_number(metrics.get('Total trades', '0')))
            short_positions = int(extract_number(metrics.get('Short positions (won %)', '0').split()[0]))
            long_positions = int(extract_number(metrics.get('Long positions (won %)', '0').split()[0]))
            profit_trades = int(extract_number(metrics.get('Profit trades (% of total)', '0').split()[0]))
            loss_trades = int(extract_number(metrics.get('Loss trades (% of total)', '0').split()[0]))
            
            # Calculate additional metrics
            sharpe_ratio = None
            recovery_factor = None
            if maximal_drawdown > 0:
                recovery_factor = total_net_profit / maximal_drawdown
            
            # Parse trades if available
            trades = []
            trades_table = soup.find('table', {'id': 'trades'}) or soup.find_all('table')[-1] if soup.find_all('table') else None
            
            if trades_table:
                trade_rows = trades_table.find_all('tr')[1:]  # Skip header
                for row in trade_rows:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        trade = {
                            'ticket': cols[0].text.strip(),
                            'time': cols[1].text.strip(),
                            'type': cols[2].text.strip(),
                            'size': extract_number(cols[3].text),
                            'symbol': cols[4].text.strip() if len(cols) > 4 else '',
                            'price': extract_number(cols[5].text) if len(cols) > 5 else 0,
                            'profit': extract_number(cols[6].text) if len(cols) > 6 else 0
                        }
                        trades.append(trade)
            
            report = BacktestReport(
                initial_deposit=initial_deposit,
                total_net_profit=total_net_profit,
                gross_profit=gross_profit,
                gross_loss=gross_loss,
                profit_factor=profit_factor,
                expected_payoff=expected_payoff,
                absolute_drawdown=absolute_drawdown,
                maximal_drawdown=maximal_drawdown,
                relative_drawdown=relative_drawdown,
                total_trades=total_trades,
                short_positions=short_positions,
                long_positions=long_positions,
                profit_trades=profit_trades,
                loss_trades=loss_trades,
                sharpe_ratio=sharpe_ratio,
                recovery_factor=recovery_factor,
                trades=trades
            )
            
            logger.info(f"Parsed backtest report with {len(trades)} trades")
            return report
            
        except Exception as e:
            logger.error(f"Failed to parse backtest report: {str(e)}")
            raise
    
    @staticmethod
    def find_best_parameters(
        optimization_results: List[OptimizationResult],
        forward_results: Optional[List[OptimizationResult]] = None,
        criteria: Dict[str, Any] = None
    ) -> List[OptimizationResult]:
        """
        Find best parameters based on optimization and forward test results
        
        Args:
            optimization_results: List of optimization results
            forward_results: Optional list of forward test results
            criteria: Dictionary of filtering criteria
            
        Returns:
            List of best performing parameter sets
        """
        logger.info(f"Finding best parameters from {len(optimization_results)} results")
        
        if not optimization_results:
            return []
        
        # Default criteria
        default_criteria = {
            'min_profit': 0,
            'min_profit_factor': 1.0,
            'min_trades': 10,
            'max_drawdown': None,
            'min_sharpe': None,
            'min_recovery': None,
            'top_n': 10
        }
        
        if criteria:
            default_criteria.update(criteria)
        
        # Filter by criteria
        filtered = []
        for result in optimization_results:
            if result.profit < default_criteria['min_profit']:
                continue
            if result.profit_factor and result.profit_factor < default_criteria['min_profit_factor']:
                continue
            if result.total_trades < default_criteria['min_trades']:
                continue
            if default_criteria['max_drawdown'] and result.drawdown_percent and result.drawdown_percent > default_criteria['max_drawdown']:
                continue
            if default_criteria['min_sharpe'] and result.sharpe_ratio and result.sharpe_ratio < default_criteria['min_sharpe']:
                continue
            if default_criteria['min_recovery'] and result.recovery_factor and result.recovery_factor < default_criteria['min_recovery']:
                continue
            
            filtered.append(result)
        
        # Sort by profit (can be customized)
        filtered.sort(key=lambda x: x.profit, reverse=True)
        
        # Take top N
        top_results = filtered[:default_criteria['top_n']]
        
        # If forward test results provided, validate against them
        if forward_results:
            # Match parameters and verify performance
            validated = []
            for opt_result in top_results:
                # Find matching forward test result
                for fwd_result in forward_results:
                    if opt_result.parameters == fwd_result.parameters:
                        # Check if forward test is also profitable
                        if fwd_result.profit > 0:
                            validated.append(opt_result)
                        break
            
            logger.info(f"Found {len(validated)} validated parameter sets")
            return validated
        
        logger.info(f"Found {len(top_results)} best parameter sets")
        return top_results
