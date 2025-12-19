"""
Test script for MT5 integration features
"""

import sys
from mt5_parser import MT5Parser, OptimizationResult
from set_file_generator import SetFileGenerator
from preset_manager import PresetManager

def test_optimization_parsing():
    """Test parsing optimization report"""
    print("Testing optimization report parsing...")
    
    # Sample XML optimization report
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<OptimizationReport>
    <Row Pass="1">
        <Parameter name="StopLoss">50</Parameter>
        <Parameter name="TakeProfit">100</Parameter>
        <Result>1250.50</Result>
        <Trades>45</Trades>
        <ProfitFactor>1.85</ProfitFactor>
        <ExpectedPayoff>27.79</ExpectedPayoff>
        <Drawdown>-250.00</Drawdown>
        <Sharpe>1.45</Sharpe>
    </Row>
    <Row Pass="2">
        <Parameter name="StopLoss">60</Parameter>
        <Parameter name="TakeProfit">120</Parameter>
        <Result>1450.75</Result>
        <Trades>52</Trades>
        <ProfitFactor>2.15</ProfitFactor>
        <ExpectedPayoff>27.90</ExpectedPayoff>
        <Drawdown>-180.00</Drawdown>
        <Sharpe>1.75</Sharpe>
    </Row>
</OptimizationReport>"""
    
    parser = MT5Parser()
    results = parser.parse_optimization_report(xml_content, 'xml')
    
    print(f"✓ Parsed {len(results)} optimization results")
    for result in results:
        print(f"  Pass {result.pass_number}: Profit=${result.profit}, Trades={result.total_trades}, PF={result.profit_factor}")
    
    return results

def test_best_parameters(results):
    """Test finding best parameters"""
    print("\nTesting best parameters finder...")
    
    parser = MT5Parser()
    best = parser.find_best_parameters(
        results,
        criteria={
            'min_profit': 1000,
            'min_profit_factor': 1.5,
            'min_trades': 40,
            'top_n': 5
        }
    )
    
    print(f"✓ Found {len(best)} best parameter sets")
    for result in best:
        print(f"  Pass {result.pass_number}: Profit=${result.profit}")
    
    return best

def test_set_file_generation():
    """Test .set file generation"""
    print("\nTesting .set file generation...")
    
    generator = SetFileGenerator()
    parameters = {
        'StopLoss': 50,
        'TakeProfit': 100,
        'LotSize': 0.1,
        'UseTrailingStop': True,
        'MagicNumber': 12345
    }
    
    content = generator.generate_set_file(parameters, 'TestPreset')
    print(f"✓ Generated .set file with {len(parameters)} parameters")
    print("Content preview:")
    print(content[:200] + "...")
    
    # Test parsing
    parsed = generator.parse_set_file(content)
    print(f"✓ Parsed .set file back with {len(parsed)} parameters")
    
    return content

def test_preset_manager():
    """Test preset manager"""
    print("\nTesting preset manager...")
    
    manager = PresetManager()
    
    # Add preset
    preset = manager.add_preset(
        name="Test Preset 1",
        parameters={'StopLoss': 50, 'TakeProfit': 100},
        optimization_metrics={'profit': 1250.50, 'total_trades': 45}
    )
    print(f"✓ Created preset: {preset.name} (ID: {preset.id})")
    
    # Add another preset
    preset2 = manager.add_preset(
        name="Test Preset 2",
        parameters={'StopLoss': 60, 'TakeProfit': 120},
        optimization_metrics={'profit': 1450.75, 'total_trades': 52}
    )
    print(f"✓ Created preset: {preset2.name} (ID: {preset2.id})")
    
    # Update with backtest
    backtest_data = {
        'total_net_profit': 1500.00,
        'profit_factor': 2.0,
        'maximal_drawdown': 200.00,
        'sharpe_ratio': 1.8,
        'recovery_factor': 7.5,
        'total_trades': 50
    }
    manager.update_preset_backtest(preset.id, backtest_data)
    print(f"✓ Updated preset with backtest data")
    
    # Get all presets
    all_presets = manager.get_all_presets()
    print(f"✓ Retrieved {len(all_presets)} presets")
    
    # Compare presets
    comparison = manager.compare_presets([preset.id, preset2.id])
    print(f"✓ Compared {len(comparison['presets'])} presets")
    if comparison['metrics_comparison']['best_profit']:
        print(f"  Best profit: {comparison['metrics_comparison']['best_profit']['name']}")
    
    return manager

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("MT5 Integration Tests")
    print("=" * 60)
    
    try:
        # Test 1: Parsing
        results = test_optimization_parsing()
        
        # Test 2: Finding best parameters
        best = test_best_parameters(results)
        
        # Test 3: .set file generation
        set_content = test_set_file_generation()
        
        # Test 4: Preset manager
        manager = test_preset_manager()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
        return True
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Test failed: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
