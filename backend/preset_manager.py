"""
Preset Manager for MT5 Analysis
Manages presets, backtest reports, and comparisons
"""

import logging
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Preset:
    """Trading strategy preset"""
    id: str
    name: str
    parameters: Dict[str, Any]
    optimization_metrics: Dict[str, Any]
    backtest_report: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class PresetManager:
    """Manages presets and their associated data"""
    
    def __init__(self):
        """Initialize preset manager"""
        self.presets: Dict[str, Preset] = {}
        logger.info("PresetManager initialized")
    
    def add_preset(
        self,
        name: str,
        parameters: Dict[str, Any],
        optimization_metrics: Dict[str, Any],
        preset_id: Optional[str] = None
    ) -> Preset:
        """
        Add a new preset
        
        Args:
            name: Preset name
            parameters: Trading parameters
            optimization_metrics: Metrics from optimization
            preset_id: Optional preset ID (generated if not provided)
            
        Returns:
            Created Preset object
        """
        if preset_id is None:
            preset_id = f"preset_{len(self.presets) + 1}_{int(datetime.now().timestamp())}"
        
        preset = Preset(
            id=preset_id,
            name=name,
            parameters=parameters,
            optimization_metrics=optimization_metrics
        )
        
        self.presets[preset_id] = preset
        logger.info(f"Added preset: {name} (ID: {preset_id})")
        
        return preset
    
    def update_preset_backtest(self, preset_id: str, backtest_report: Dict[str, Any]) -> bool:
        """
        Update preset with backtest report
        
        Args:
            preset_id: Preset ID
            backtest_report: Backtest report data
            
        Returns:
            True if successful, False otherwise
        """
        if preset_id not in self.presets:
            logger.warning(f"Preset not found: {preset_id}")
            return False
        
        self.presets[preset_id].backtest_report = backtest_report
        logger.info(f"Updated preset {preset_id} with backtest report")
        
        return True
    
    def get_preset(self, preset_id: str) -> Optional[Preset]:
        """Get preset by ID"""
        return self.presets.get(preset_id)
    
    def get_all_presets(self) -> List[Preset]:
        """Get all presets"""
        return list(self.presets.values())
    
    def get_presets_with_backtests(self) -> List[Preset]:
        """Get presets that have backtest reports"""
        return [p for p in self.presets.values() if p.backtest_report is not None]
    
    def delete_preset(self, preset_id: str) -> bool:
        """Delete a preset"""
        if preset_id in self.presets:
            del self.presets[preset_id]
            logger.info(f"Deleted preset: {preset_id}")
            return True
        return False
    
    def compare_presets(self, preset_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple presets
        
        Args:
            preset_ids: List of preset IDs to compare
            
        Returns:
            Comparison data including metrics and charts data
        """
        logger.info(f"Comparing {len(preset_ids)} presets")
        
        presets_data = []
        for preset_id in preset_ids:
            preset = self.get_preset(preset_id)
            if preset:
                presets_data.append(preset)
            else:
                logger.warning(f"Preset not found: {preset_id}")
        
        if not presets_data:
            return {"error": "No valid presets found"}
        
        # Prepare comparison data
        comparison = {
            "presets": [],
            "metrics_comparison": {},
            "chart_data": {
                "labels": [],
                "profit": [],
                "drawdown": [],
                "profit_factor": [],
                "sharpe_ratio": [],
                "recovery_factor": []
            }
        }
        
        for preset in presets_data:
            preset_info = {
                "id": preset.id,
                "name": preset.name,
                "parameters": preset.parameters,
                "optimization_metrics": preset.optimization_metrics
            }
            
            # Add backtest metrics if available
            if preset.backtest_report:
                preset_info["backtest_metrics"] = preset.backtest_report
                
                # Add to chart data
                comparison["chart_data"]["labels"].append(preset.name)
                comparison["chart_data"]["profit"].append(
                    preset.backtest_report.get("total_net_profit", 0)
                )
                comparison["chart_data"]["drawdown"].append(
                    preset.backtest_report.get("maximal_drawdown", 0)
                )
                comparison["chart_data"]["profit_factor"].append(
                    preset.backtest_report.get("profit_factor", 0)
                )
                comparison["chart_data"]["sharpe_ratio"].append(
                    preset.backtest_report.get("sharpe_ratio", 0)
                )
                comparison["chart_data"]["recovery_factor"].append(
                    preset.backtest_report.get("recovery_factor", 0)
                )
            
            comparison["presets"].append(preset_info)
        
        # Calculate metrics comparison
        comparison["metrics_comparison"] = self._calculate_metrics_comparison(presets_data)
        
        logger.info("Comparison completed")
        return comparison
    
    def _calculate_metrics_comparison(self, presets: List[Preset]) -> Dict[str, Any]:
        """Calculate comparative metrics"""
        metrics = {
            "best_profit": None,
            "best_sharpe": None,
            "best_recovery": None,
            "lowest_drawdown": None,
            "best_profit_factor": None
        }
        
        best_profit_value = float('-inf')
        best_sharpe_value = float('-inf')
        best_recovery_value = float('-inf')
        lowest_drawdown_value = float('inf')
        best_pf_value = float('-inf')
        
        for preset in presets:
            if preset.backtest_report:
                profit = preset.backtest_report.get("total_net_profit", 0)
                sharpe = preset.backtest_report.get("sharpe_ratio", 0)
                recovery = preset.backtest_report.get("recovery_factor", 0)
                drawdown = preset.backtest_report.get("maximal_drawdown", float('inf'))
                pf = preset.backtest_report.get("profit_factor", 0)
                
                if profit > best_profit_value:
                    best_profit_value = profit
                    metrics["best_profit"] = {"preset_id": preset.id, "name": preset.name, "value": profit}
                
                if sharpe and sharpe > best_sharpe_value:
                    best_sharpe_value = sharpe
                    metrics["best_sharpe"] = {"preset_id": preset.id, "name": preset.name, "value": sharpe}
                
                if recovery and recovery > best_recovery_value:
                    best_recovery_value = recovery
                    metrics["best_recovery"] = {"preset_id": preset.id, "name": preset.name, "value": recovery}
                
                if drawdown < lowest_drawdown_value:
                    lowest_drawdown_value = drawdown
                    metrics["lowest_drawdown"] = {"preset_id": preset.id, "name": preset.name, "value": drawdown}
                
                if pf > best_pf_value:
                    best_pf_value = pf
                    metrics["best_profit_factor"] = {"preset_id": preset.id, "name": preset.name, "value": pf}
        
        return metrics
    
    def export_presets(self) -> str:
        """Export all presets to JSON string"""
        data = {
            "exported_at": datetime.now().isoformat(),
            "presets": [p.to_dict() for p in self.presets.values()]
        }
        return json.dumps(data, indent=2)
    
    def import_presets(self, json_data: str) -> int:
        """Import presets from JSON string"""
        data = json.loads(json_data)
        count = 0
        
        for preset_data in data.get("presets", []):
            preset = Preset(**preset_data)
            self.presets[preset.id] = preset
            count += 1
        
        logger.info(f"Imported {count} presets")
        return count
