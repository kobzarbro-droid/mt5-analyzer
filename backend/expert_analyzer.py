"""
Expert Analyzer Module
Analyzes trading expert performance by magic number
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from mt5_parser import Trade, EquityPoint, BacktestReport

logger = logging.getLogger(__name__)


@dataclass
class ExpertMetrics:
    """Comprehensive metrics for a single expert (magic number)"""
    magic_number: int
    name: str
    total_trades: int
    profit_trades: int
    loss_trades: int
    total_profit: float
    total_loss: float
    net_profit: float
    win_rate: float
    profit_factor: float
    average_profit: float
    average_loss: float
    average_profit_per_trade: float
    max_drawdown: float
    max_drawdown_percent: float
    recovery_factor: float
    sharpe_ratio: Optional[float] = None
    average_trade_duration: Optional[float] = None
    symbols: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'magic_number': self.magic_number,
            'name': self.name,
            'total_trades': self.total_trades,
            'profit_trades': self.profit_trades,
            'loss_trades': self.loss_trades,
            'total_profit': self.total_profit,
            'total_loss': self.total_loss,
            'net_profit': self.net_profit,
            'win_rate': self.win_rate,
            'profit_factor': self.profit_factor,
            'average_profit': self.average_profit,
            'average_loss': self.average_loss,
            'average_profit_per_trade': self.average_profit_per_trade,
            'max_drawdown': self.max_drawdown,
            'max_drawdown_percent': self.max_drawdown_percent,
            'recovery_factor': self.recovery_factor,
            'sharpe_ratio': self.sharpe_ratio,
            'average_trade_duration': self.average_trade_duration,
            'symbols': self.symbols
        }


@dataclass
class ComparisonResult:
    """Results of comparing multiple experts"""
    experts: List[int]
    best_performer: int
    best_by_profit: int
    best_by_winrate: int
    best_by_profit_factor: int
    best_by_recovery: int
    comparison_data: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'experts': self.experts,
            'best_performer': self.best_performer,
            'best_by_profit': self.best_by_profit,
            'best_by_winrate': self.best_by_winrate,
            'best_by_profit_factor': self.best_by_profit_factor,
            'best_by_recovery': self.best_by_recovery,
            'comparison_data': self.comparison_data
        }


class ExpertAnalyzer:
    """Analyze trading expert performance by magic number"""
    
    def __init__(self):
        self.experts_cache: Dict[int, ExpertMetrics] = {}
        
    def group_by_magic(self, trades: List[Trade]) -> Dict[int, List[Trade]]:
        """
        Group trades by magic number
        
        Args:
            trades: List of Trade objects
            
        Returns:
            Dictionary mapping magic_number to list of trades
        """
        logger.info(f"Grouping {len(trades)} trades by magic number")
        
        grouped: Dict[int, List[Trade]] = {}
        
        for trade in trades:
            magic = trade.magic_number
            if magic not in grouped:
                grouped[magic] = []
            grouped[magic].append(trade)
        
        logger.info(f"Grouped into {len(grouped)} experts")
        return grouped
    
    def group_by_magic_from_dict(self, trades: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """
        Group trade dictionaries by magic number
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Dictionary mapping magic_number to list of trade dicts
        """
        logger.info(f"Grouping {len(trades)} trade dicts by magic number")
        
        grouped: Dict[int, List[Dict[str, Any]]] = {}
        
        for trade in trades:
            magic = trade.get('magic_number', 0)
            if magic not in grouped:
                grouped[magic] = []
            grouped[magic].append(trade)
        
        logger.info(f"Grouped into {len(grouped)} experts")
        return grouped
    
    def calculate_metrics_by_expert(
        self, 
        trades_by_magic: Dict[int, List[Trade]], 
        initial_balance: float = 10000.0
    ) -> Dict[int, ExpertMetrics]:
        """
        Calculate comprehensive metrics for each expert
        
        Args:
            trades_by_magic: Dictionary of trades grouped by magic number
            initial_balance: Initial account balance for calculations
            
        Returns:
            Dictionary mapping magic_number to ExpertMetrics
        """
        logger.info(f"Calculating metrics for {len(trades_by_magic)} experts")
        
        metrics_by_expert: Dict[int, ExpertMetrics] = {}
        
        for magic_number, trades in trades_by_magic.items():
            if not trades:
                continue
            
            # Basic counts
            total_trades = len(trades)
            profit_trades = sum(1 for t in trades if t.profit > 0)
            loss_trades = sum(1 for t in trades if t.profit < 0)
            
            # Profit calculations
            total_profit = sum(t.profit for t in trades if t.profit > 0)
            total_loss = abs(sum(t.profit for t in trades if t.profit < 0))
            net_profit = sum(t.profit for t in trades)
            
            # Ratios
            win_rate = (profit_trades / total_trades * 100) if total_trades > 0 else 0.0
            profit_factor = (total_profit / total_loss) if total_loss > 0 else 0.0
            average_profit = (total_profit / profit_trades) if profit_trades > 0 else 0.0
            average_loss = (total_loss / loss_trades) if loss_trades > 0 else 0.0
            average_profit_per_trade = net_profit / total_trades if total_trades > 0 else 0.0
            
            # Drawdown calculation
            max_drawdown, max_drawdown_percent = self._calculate_drawdown(trades, initial_balance)
            
            # Recovery factor
            recovery_factor = (net_profit / max_drawdown) if max_drawdown > 0 else 0.0
            
            # Sharpe ratio (simplified - would need more data for accurate calculation)
            sharpe_ratio = self._calculate_sharpe_ratio(trades)
            
            # Get unique symbols
            symbols = list(set(t.symbol for t in trades if t.symbol))
            
            # Create metrics object
            metrics = ExpertMetrics(
                magic_number=magic_number,
                name=f"Expert {magic_number}",
                total_trades=total_trades,
                profit_trades=profit_trades,
                loss_trades=loss_trades,
                total_profit=total_profit,
                total_loss=total_loss,
                net_profit=net_profit,
                win_rate=win_rate,
                profit_factor=profit_factor,
                average_profit=average_profit,
                average_loss=average_loss,
                average_profit_per_trade=average_profit_per_trade,
                max_drawdown=max_drawdown,
                max_drawdown_percent=max_drawdown_percent,
                recovery_factor=recovery_factor,
                sharpe_ratio=sharpe_ratio,
                symbols=symbols
            )
            
            metrics_by_expert[magic_number] = metrics
            self.experts_cache[magic_number] = metrics
        
        logger.info(f"Calculated metrics for {len(metrics_by_expert)} experts")
        return metrics_by_expert
    
    def calculate_metrics_from_dict(
        self, 
        trades_by_magic: Dict[int, List[Dict[str, Any]]], 
        initial_balance: float = 10000.0
    ) -> Dict[int, ExpertMetrics]:
        """
        Calculate metrics from trade dictionaries
        
        Args:
            trades_by_magic: Dictionary of trade dicts grouped by magic number
            initial_balance: Initial account balance
            
        Returns:
            Dictionary mapping magic_number to ExpertMetrics
        """
        # Convert dicts to Trade objects
        trades_obj_by_magic: Dict[int, List[Trade]] = {}
        
        for magic, trade_dicts in trades_by_magic.items():
            trades_obj = []
            for td in trade_dicts:
                trade = Trade(
                    ticket=td.get('ticket', ''),
                    magic_number=td.get('magic_number', 0),
                    time=td.get('time', ''),
                    symbol=td.get('symbol', ''),
                    type=td.get('type', ''),
                    volume=td.get('volume', 0.0),
                    price=td.get('price', 0.0),
                    sl=td.get('sl', 0.0),
                    tp=td.get('tp', 0.0),
                    profit=td.get('profit', 0.0)
                )
                trades_obj.append(trade)
            trades_obj_by_magic[magic] = trades_obj
        
        return self.calculate_metrics_by_expert(trades_obj_by_magic, initial_balance)
    
    def calculate_equity_curves(
        self, 
        trades_by_magic: Dict[int, List[Trade]], 
        initial_balance: float = 10000.0
    ) -> Dict[int, List[EquityPoint]]:
        """
        Calculate equity curves for each expert
        
        Args:
            trades_by_magic: Dictionary of trades grouped by magic number
            initial_balance: Initial account balance
            
        Returns:
            Dictionary mapping magic_number to equity curve
        """
        logger.info(f"Calculating equity curves for {len(trades_by_magic)} experts")
        
        from mt5_parser import MT5Parser
        
        equity_curves: Dict[int, List[EquityPoint]] = {}
        
        for magic_number, trades in trades_by_magic.items():
            if not trades:
                continue
            
            equity_curve = MT5Parser.calculate_equity_curve(trades, initial_balance)
            equity_curves[magic_number] = equity_curve
        
        logger.info(f"Calculated {len(equity_curves)} equity curves")
        return equity_curves
    
    def compare_experts(self, expert_ids: List[int]) -> ComparisonResult:
        """
        Compare multiple experts
        
        Args:
            expert_ids: List of magic numbers to compare
            
        Returns:
            ComparisonResult with comparison data
        """
        logger.info(f"Comparing {len(expert_ids)} experts")
        
        if not expert_ids:
            raise ValueError("No experts to compare")
        
        # Get metrics for each expert
        comparison_data: Dict[int, Dict[str, Any]] = {}
        
        for expert_id in expert_ids:
            if expert_id in self.experts_cache:
                metrics = self.experts_cache[expert_id]
                comparison_data[expert_id] = metrics.to_dict()
        
        # Find best performers
        best_by_profit = max(expert_ids, key=lambda x: comparison_data.get(x, {}).get('net_profit', 0))
        best_by_winrate = max(expert_ids, key=lambda x: comparison_data.get(x, {}).get('win_rate', 0))
        best_by_profit_factor = max(expert_ids, key=lambda x: comparison_data.get(x, {}).get('profit_factor', 0))
        best_by_recovery = max(expert_ids, key=lambda x: comparison_data.get(x, {}).get('recovery_factor', 0))
        
        # Overall best performer (by net profit)
        best_performer = best_by_profit
        
        result = ComparisonResult(
            experts=expert_ids,
            best_performer=best_performer,
            best_by_profit=best_by_profit,
            best_by_winrate=best_by_winrate,
            best_by_profit_factor=best_by_profit_factor,
            best_by_recovery=best_by_recovery,
            comparison_data=comparison_data
        )
        
        logger.info(f"Comparison complete. Best performer: Expert {best_performer}")
        return result
    
    def _calculate_drawdown(self, trades: List[Trade], initial_balance: float) -> tuple[float, float]:
        """Calculate maximum drawdown in dollars and percentage"""
        if not trades:
            return 0.0, 0.0
        
        # Sort trades by time
        sorted_trades = sorted(trades, key=lambda t: t.time)
        
        peak_balance = initial_balance
        max_drawdown = 0.0
        current_balance = initial_balance
        
        for trade in sorted_trades:
            current_balance += trade.profit
            
            if current_balance > peak_balance:
                peak_balance = current_balance
            
            drawdown = peak_balance - current_balance
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        max_drawdown_percent = (max_drawdown / peak_balance * 100) if peak_balance > 0 else 0.0
        
        return max_drawdown, max_drawdown_percent
    
    def _calculate_sharpe_ratio(self, trades: List[Trade]) -> Optional[float]:
        """Calculate simplified Sharpe ratio"""
        if not trades or len(trades) < 2:
            return None
        
        # Calculate returns
        returns = [t.profit for t in trades]
        
        # Calculate mean and std
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return None
        
        # Simplified Sharpe (assuming risk-free rate = 0)
        sharpe = mean_return / std_dev
        
        return sharpe
