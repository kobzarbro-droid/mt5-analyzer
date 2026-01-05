// MT5 Portfolio Analyzer - Enhanced Frontend JavaScript

// Configuration
// Use relative URL for API when in production/Docker, or localhost for development
const API_BASE_URL = window.location.hostname === 'localhost' && window.location.port !== '8080' 
    ? 'http://localhost:5000' 
    : '';

// State management
let strategies = [];
let currentAnalysis = null;
let optimizationResults = [];
let forwardResults = [];
let bestParameters = [];
let selectedParameterSets = new Set();
let presets = [];
let selectedPresets = new Set();
let comparisonChart = null;

// Dashboard state
let dashboardData = null;
let expertsData = {};
let selectedExperts = new Set();
let expertCharts = {};
let overallChart = null;
let expertComparisonChart = null;

// DOM elements
let strategiesContainer, analyzeBtn, addStrategyBtn, loadSampleBtn;
let statusMessage, loadingSpinner, modal, analysisResult, closeModalBtn, exportBtn;

// New DOM elements for reports
let optimizationFile, forwardFile;
let uploadOptimizationBtn, uploadForwardBtn;
let optimizationStatus, forwardStatus;
let resultsSection, bestParametersSection, bestParametersList;
let applyFiltersBtn, getGptRecommendationBtn;

// Presets elements
let presetsListSection, presetsList, refreshPresetsBtn;
let comparisonSection, comparePresetsBtn, getGptComparisonBtn;

// Dashboard elements
let dashboardBacktestFile, uploadDashboardBacktestBtn, dashboardUploadStatus;
let dashboardFiltersPanel, magicFilter, symbolFilter, dateFrom, dateTo;
let applyDashboardFilters, clearDashboardFilters;
let dashboardSummary, totalProfit, expertsCount, overallWinRate, totalTrades;
let overallEquitySection, overallEquityChart;
let expertsSection, expertsContainer, expertSortBy, compareSelectedExperts;
let expertComparisonSection, closeComparison, comparisonMetrics;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    setupTabs();
    addStrategy(); // Add first strategy by default
});

function initializeElements() {
    // Original elements
    strategiesContainer = document.getElementById('strategiesContainer');
    analyzeBtn = document.getElementById('analyzeBtn');
    addStrategyBtn = document.getElementById('addStrategyBtn');
    loadSampleBtn = document.getElementById('loadSampleBtn');
    statusMessage = document.getElementById('statusMessage');
    loadingSpinner = document.getElementById('loadingSpinner');
    modal = document.getElementById('analysisModal');
    analysisResult = document.getElementById('analysisResult');
    closeModalBtn = document.getElementById('closeModalBtn');
    exportBtn = document.getElementById('exportBtn');
    
    // New elements
    optimizationFile = document.getElementById('optimizationFile');
    forwardFile = document.getElementById('forwardFile');
    uploadOptimizationBtn = document.getElementById('uploadOptimizationBtn');
    uploadForwardBtn = document.getElementById('uploadForwardBtn');
    optimizationStatus = document.getElementById('optimizationStatus');
    forwardStatus = document.getElementById('forwardStatus');
    resultsSection = document.getElementById('resultsSection');
    bestParametersSection = document.getElementById('bestParametersSection');
    bestParametersList = document.getElementById('bestParametersList');
    applyFiltersBtn = document.getElementById('applyFiltersBtn');
    getGptRecommendationBtn = document.getElementById('getGptRecommendationBtn');
    
    // Presets elements
    presetsListSection = document.getElementById('presetsListSection');
    presetsList = document.getElementById('presetsList');
    refreshPresetsBtn = document.getElementById('refreshPresetsBtn');
    comparisonSection = document.getElementById('comparisonSection');
    comparePresetsBtn = document.getElementById('comparePresetsBtn');
    getGptComparisonBtn = document.getElementById('getGptComparisonBtn');
    
    // Dashboard elements
    dashboardBacktestFile = document.getElementById('dashboardBacktestFile');
    uploadDashboardBacktestBtn = document.getElementById('uploadDashboardBacktestBtn');
    dashboardUploadStatus = document.getElementById('dashboardUploadStatus');
    dashboardFiltersPanel = document.getElementById('dashboardFiltersPanel');
    magicFilter = document.getElementById('magicFilter');
    symbolFilter = document.getElementById('symbolFilter');
    dateFrom = document.getElementById('dateFrom');
    dateTo = document.getElementById('dateTo');
    applyDashboardFilters = document.getElementById('applyDashboardFilters');
    clearDashboardFilters = document.getElementById('clearDashboardFilters');
    dashboardSummary = document.getElementById('dashboardSummary');
    totalProfit = document.getElementById('totalProfit');
    expertsCount = document.getElementById('expertsCount');
    overallWinRate = document.getElementById('overallWinRate');
    totalTrades = document.getElementById('totalTrades');
    overallEquitySection = document.getElementById('overallEquitySection');
    overallEquityChart = document.getElementById('overallEquityChart');
    expertsSection = document.getElementById('expertsSection');
    expertsContainer = document.getElementById('expertsContainer');
    expertSortBy = document.getElementById('expertSortBy');
    compareSelectedExperts = document.getElementById('compareSelectedExperts');
    expertComparisonSection = document.getElementById('expertComparisonSection');
    closeComparison = document.getElementById('closeComparison');
    comparisonMetrics = document.getElementById('comparisonMetrics');
}

function setupEventListeners() {
    // Original listeners
    if (analyzeBtn) analyzeBtn.addEventListener('click', analyzePortfolio);
    if (addStrategyBtn) addStrategyBtn.addEventListener('click', addStrategy);
    if (loadSampleBtn) loadSampleBtn.addEventListener('click', loadSampleData);
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if (exportBtn) exportBtn.addEventListener('click', exportAnalysis);
    
    // New listeners
    if (uploadOptimizationBtn) uploadOptimizationBtn.addEventListener('click', uploadOptimization);
    if (uploadForwardBtn) uploadForwardBtn.addEventListener('click', uploadForward);
    if (applyFiltersBtn) applyFiltersBtn.addEventListener('click', applyFilters);
    if (getGptRecommendationBtn) getGptRecommendationBtn.addEventListener('click', getGptRecommendation);
    
    // Presets listeners
    if (refreshPresetsBtn) refreshPresetsBtn.addEventListener('click', loadPresets);
    if (comparePresetsBtn) comparePresetsBtn.addEventListener('click', comparePresets);
    if (getGptComparisonBtn) getGptComparisonBtn.addEventListener('click', getGptComparison);
    
    // Dashboard listeners
    if (uploadDashboardBacktestBtn) uploadDashboardBacktestBtn.addEventListener('click', uploadDashboardBacktest);
    if (applyDashboardFilters) applyDashboardFilters.addEventListener('click', applyDashboardFiltersFunc);
    if (clearDashboardFilters) clearDashboardFilters.addEventListener('click', clearDashboardFiltersFunc);
    if (compareSelectedExperts) compareSelectedExperts.addEventListener('click', compareExpertsFunc);
    if (closeComparison) closeComparison.addEventListener('click', closeExpertComparison);
    if (expertSortBy) expertSortBy.addEventListener('change', sortExperts);
    
    // Modal listeners
    if (modal) {
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.classList.contains('show')) {
            closeModal();
        }
    });
    
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
}

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            btn.classList.add('active');
            const tabContent = document.getElementById(`${tabName}-tab`);
            if (tabContent) {
                tabContent.classList.add('active');
            }
            
            // Load presets when switching to presets tab
            if (tabName === 'presets') {
                loadPresets();
            }
        });
    });
}

// ===== ORIGINAL PORTFOLIO ANALYSIS FUNCTIONS =====

function addStrategy() {
    const strategyIndex = strategies.length + 1;
    
    if (strategyIndex > 5) {
        showStatus('Maximum 5 strategies allowed', 'error');
        return;
    }
    
    const strategyCard = document.createElement('div');
    strategyCard.className = 'strategy-card';
    strategyCard.dataset.index = strategyIndex;
    
    strategyCard.innerHTML = `
        <div class="strategy-header">
            <h3>Strategy ${strategyIndex}</h3>
            <button class="remove-btn" onclick="removeStrategy(${strategyIndex})">Remove</button>
        </div>
        <div class="strategy-inputs">
            <div class="input-group">
                <label>Name</label>
                <input type="text" class="strategy-name" placeholder="Strategy name" value="Strategy ${strategyIndex}">
            </div>
            <div class="input-group">
                <label>Equity</label>
                <input type="number" class="strategy-equity" placeholder="100000" step="1000">
            </div>
            <div class="input-group">
                <label>Drawdown (%)</label>
                <input type="number" class="strategy-drawdown" placeholder="-15.5" step="0.1">
            </div>
            <div class="input-group">
                <label>Correlation</label>
                <input type="number" class="strategy-correlation" placeholder="0.65" step="0.01" min="-1" max="1">
            </div>
            <div class="input-group">
                <label>Recovery Factor</label>
                <input type="number" class="strategy-recovery" placeholder="2.3" step="0.1">
            </div>
            <div class="input-group">
                <label>Profit (%)</label>
                <input type="number" class="strategy-profit" placeholder="45.2" step="0.1">
            </div>
        </div>
    `;
    
    strategiesContainer.appendChild(strategyCard);
    strategies.push(strategyIndex);
    
    if (strategies.length >= 5) {
        addStrategyBtn.disabled = true;
    }
}

function removeStrategy(index) {
    const strategyCard = document.querySelector(`[data-index="${index}"]`);
    if (strategyCard) {
        strategyCard.remove();
        strategies = strategies.filter(s => s !== index);
        
        if (strategies.length < 5) {
            addStrategyBtn.disabled = false;
        }
    }
}

function collectStrategyData() {
    const strategyCards = document.querySelectorAll('.strategy-card');
    const data = [];
    
    strategyCards.forEach(card => {
        const name = card.querySelector('.strategy-name').value;
        const equity = parseFloat(card.querySelector('.strategy-equity').value);
        const drawdown = parseFloat(card.querySelector('.strategy-drawdown').value);
        const correlation = parseFloat(card.querySelector('.strategy-correlation').value);
        const recovery = parseFloat(card.querySelector('.strategy-recovery').value);
        const profit = parseFloat(card.querySelector('.strategy-profit').value);
        
        if (!isNaN(equity) && !isNaN(drawdown) && !isNaN(correlation) && 
            !isNaN(recovery) && !isNaN(profit)) {
            data.push({
                name: name || 'Unnamed Strategy',
                equity: equity,
                drawdown: drawdown,
                correlation: correlation,
                recovery: recovery,
                profit: profit
            });
        }
    });
    
    return data;
}

async function analyzePortfolio() {
    const strategyData = collectStrategyData();
    
    if (strategyData.length === 0) {
        showStatus('Please enter data for at least one strategy', 'error');
        return;
    }
    
    analyzeBtn.disabled = true;
    showLoading(true);
    showStatus('Analyzing portfolio with AI...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/portfolio/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                strategies: strategyData
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentAnalysis = result;
            showStatus('Analysis complete!', 'success');
            displayAnalysis(result);
        } else {
            showStatus(`Analysis failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Connection error: ${error.message}`, 'error');
        console.error('Error:', error);
    } finally {
        analyzeBtn.disabled = false;
        showLoading(false);
    }
}

function displayAnalysis(result) {
    if (!result || !result.full_analysis) {
        analysisResult.innerHTML = '<p class="error">No analysis data available</p>';
        return;
    }
    
    let formattedAnalysis = result.full_analysis;
    
    formattedAnalysis = formattedAnalysis
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
    
    formattedAnalysis = '<p>' + formattedAnalysis + '</p>';
    formattedAnalysis = formattedAnalysis.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    formattedAnalysis = formattedAnalysis.replace(/<\/ul>\s*<ul>/g, '');
    
    let timestampText = '';
    if (result.timestamp) {
        const date = new Date(result.timestamp);
        timestampText = `<p><strong>Analysis Date:</strong> ${date.toLocaleString()}</p>`;
    }
    
    let processingTimeText = '';
    if (result.processing_time) {
        processingTimeText = `<p><strong>Processing Time:</strong> ${result.processing_time.toFixed(2)} seconds</p>`;
    }
    
    const metaInfo = `
        <div style="background: var(--background); padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
            <p><strong>Strategies Analyzed:</strong> ${result.strategies_count}</p>
            <p><strong>AI Model:</strong> ${result.model}</p>
            ${timestampText}
            ${processingTimeText}
        </div>
    `;
    
    analysisResult.innerHTML = metaInfo + formattedAnalysis;
    modal.classList.add('show');
}

function closeModal() {
    if (modal) modal.classList.remove('show');
}

function exportAnalysis() {
    if (!currentAnalysis) {
        showStatus('No analysis to export', 'error');
        return;
    }
    
    const exportData = {
        export_timestamp: new Date().toISOString(),
        analysis_timestamp: currentAnalysis.timestamp,
        strategies_count: currentAnalysis.strategies_count,
        model: currentAnalysis.model,
        processing_time: currentAnalysis.processing_time,
        analysis: currentAnalysis.full_analysis
    };
    
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `portfolio-analysis-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showStatus('Analysis exported successfully', 'success');
}

function loadSampleData() {
    strategiesContainer.innerHTML = '';
    strategies = [];
    
    const sampleStrategies = [
        {
            name: 'Trend Following Strategy',
            equity: 125000,
            drawdown: -12.5,
            correlation: 0.45,
            recovery: 2.8,
            profit: 25.0
        },
        {
            name: 'Mean Reversion Strategy',
            equity: 98000,
            drawdown: -18.2,
            correlation: 0.32,
            recovery: 1.9,
            profit: -2.0
        },
        {
            name: 'Breakout Strategy',
            equity: 142000,
            drawdown: -10.1,
            correlation: 0.55,
            recovery: 3.2,
            profit: 42.0
        }
    ];
    
    sampleStrategies.forEach((strategyData, index) => {
        addStrategy();
        const card = document.querySelector(`[data-index="${index + 1}"]`);
        if (card) {
            card.querySelector('.strategy-name').value = strategyData.name;
            card.querySelector('.strategy-equity').value = strategyData.equity;
            card.querySelector('.strategy-drawdown').value = strategyData.drawdown;
            card.querySelector('.strategy-correlation').value = strategyData.correlation;
            card.querySelector('.strategy-recovery').value = strategyData.recovery;
            card.querySelector('.strategy-profit').value = strategyData.profit;
        }
    });
    
    showStatus('Sample data loaded successfully', 'success');
}

// ===== NEW MT5 REPORT FUNCTIONS =====

async function uploadOptimization() {
    if (!optimizationFile.files || optimizationFile.files.length === 0) {
        showStatus('Please select an optimization report file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', optimizationFile.files[0]);
    
    showLoading(true);
    optimizationStatus.textContent = 'Uploading...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/upload/optimization`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            optimizationResults = result.results;
            optimizationStatus.textContent = `✓ Loaded ${result.results_count} optimization results`;
            optimizationStatus.className = 'upload-status success';
            showStatus('Optimization report loaded successfully', 'success');
            
            if (optimizationResults.length > 0) {
                resultsSection.classList.remove('hidden');
            }
        } else {
            optimizationStatus.textContent = `✗ Error: ${result.error}`;
            optimizationStatus.className = 'upload-status error';
            showStatus(`Upload failed: ${result.error}`, 'error');
        }
    } catch (error) {
        optimizationStatus.textContent = `✗ Connection error`;
        optimizationStatus.className = 'upload-status error';
        showStatus(`Upload failed: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

async function uploadForward() {
    if (!forwardFile.files || forwardFile.files.length === 0) {
        showStatus('Please select a forward test report file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', forwardFile.files[0]);
    
    showLoading(true);
    forwardStatus.textContent = 'Uploading...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/upload/forward`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            forwardResults = result.results;
            forwardStatus.textContent = `✓ Loaded ${result.results_count} forward test results`;
            forwardStatus.className = 'upload-status success';
            showStatus('Forward test report loaded successfully', 'success');
        } else {
            forwardStatus.textContent = `✗ Error: ${result.error}`;
            forwardStatus.className = 'upload-status error';
            showStatus(`Upload failed: ${result.error}`, 'error');
        }
    } catch (error) {
        forwardStatus.textContent = `✗ Connection error`;
        forwardStatus.className = 'upload-status error';
        showStatus(`Upload failed: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

async function applyFilters() {
    if (optimizationResults.length === 0) {
        showStatus('Please upload optimization report first', 'error');
        return;
    }
    
    const criteria = {
        min_profit: parseFloat(document.getElementById('minProfit').value) || 0,
        min_profit_factor: parseFloat(document.getElementById('minProfitFactor').value) || 1.0,
        min_trades: parseInt(document.getElementById('minTrades').value) || 10,
        max_drawdown: document.getElementById('maxDrawdown').value ? parseFloat(document.getElementById('maxDrawdown').value) : null,
        top_n: parseInt(document.getElementById('topN').value) || 10
    };
    
    showLoading(true);
    showStatus('Finding best parameters...', 'info');
    
    try {
        const payload = {
            optimization_results: optimizationResults,
            criteria: criteria
        };
        
        if (forwardResults.length > 0) {
            payload.forward_results = forwardResults;
        }
        
        const response = await fetch(`${API_BASE_URL}/api/analyze/best-parameters`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bestParameters = result.best_results;
            displayBestParameters(bestParameters);
            showStatus(`Found ${bestParameters.length} best parameter sets`, 'success');
        } else {
            showStatus(`Analysis failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayBestParameters(parameters) {
    if (!bestParametersList) return;
    
    bestParametersList.innerHTML = '';
    selectedParameterSets.clear();
    
    parameters.forEach((param, index) => {
        const paramDiv = document.createElement('div');
        paramDiv.className = 'parameter-set';
        paramDiv.dataset.index = index;
        
        const metricsHtml = `
            <div class="metric">Profit: <strong>$${param.profit.toFixed(2)}</strong></div>
            <div class="metric">Trades: <strong>${param.total_trades}</strong></div>
            <div class="metric">PF: <strong>${param.profit_factor ? param.profit_factor.toFixed(2) : 'N/A'}</strong></div>
            <div class="metric">DD: <strong>${param.drawdown ? param.drawdown.toFixed(2) : 'N/A'}</strong></div>
            <div class="metric">Sharpe: <strong>${param.sharpe_ratio ? param.sharpe_ratio.toFixed(2) : 'N/A'}</strong></div>
        `;
        
        paramDiv.innerHTML = `
            <h5>
                <span>Parameter Set #${param.pass_number}</span>
                <input type="checkbox" onchange="toggleParameterSelection(${index})">
            </h5>
            <div class="metrics">${metricsHtml}</div>
            <details style="margin-top: 0.5rem;">
                <summary style="cursor: pointer; color: var(--primary-color);">View Parameters</summary>
                <pre style="background: var(--surface); padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem; font-size: 0.85rem;">${JSON.stringify(param.parameters, null, 2)}</pre>
            </details>
            <div class="actions">
                <button class="btn btn-primary btn-small" onclick="saveAsPreset(${index})">💾 Save as Preset</button>
            </div>
        `;
        
        bestParametersList.appendChild(paramDiv);
    });
    
    bestParametersSection.classList.remove('hidden');
}

function toggleParameterSelection(index) {
    const paramDiv = bestParametersList.querySelector(`[data-index="${index}"]`);
    if (selectedParameterSets.has(index)) {
        selectedParameterSets.delete(index);
        paramDiv.classList.remove('selected');
    } else {
        selectedParameterSets.add(index);
        paramDiv.classList.add('selected');
    }
}

async function getGptRecommendation() {
    if (selectedParameterSets.size === 0) {
        showStatus('Please select at least one parameter set', 'error');
        return;
    }
    
    const selectedParams = Array.from(selectedParameterSets).map(index => bestParameters[index]);
    
    showLoading(true);
    showStatus('Getting GPT recommendations...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gpt/recommend-parameters`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                parameter_sets: selectedParams
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayGptRecommendation(result.recommendations);
            showStatus('GPT recommendations received', 'success');
        } else {
            showStatus(`Failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayGptRecommendation(recommendations) {
    analysisResult.innerHTML = `
        <h3>🤖 GPT Parameter Recommendations</h3>
        ${formatAnalysisText(recommendations)}
    `;
    modal.classList.add('show');
}

async function saveAsPreset(index) {
    const param = bestParameters[index];
    const presetName = prompt('Enter a name for this preset:', `Preset ${Date.now()}`);
    
    if (!presetName) return;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/preset/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: presetName,
                parameters: param.parameters,
                optimization_metrics: {
                    profit: param.profit,
                    total_trades: param.total_trades,
                    profit_factor: param.profit_factor,
                    drawdown: param.drawdown,
                    sharpe_ratio: param.sharpe_ratio,
                    recovery_factor: param.recovery_factor
                }
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus(`Preset "${presetName}" saved successfully`, 'success');
        } else {
            showStatus(`Failed to save preset: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// ===== PRESETS FUNCTIONS =====

async function loadPresets() {
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/preset/list`);
        const result = await response.json();
        
        if (result.success) {
            presets = result.presets;
            displayPresets(presets);
        } else {
            showStatus(`Failed to load presets: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayPresets(presetsArray) {
    if (!presetsListSection) return;
    
    // Use the global presetsList DOM element
    if (!presetsList) return;
    
    presetsList.innerHTML = '';
    selectedPresets.clear();
    
    if (presets.length === 0) {
        presetsList.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No presets yet. Create presets from the MT5 Reports tab.</p>';
        return;
    }
    
    presets.forEach(preset => {
        const presetCard = document.createElement('div');
        presetCard.className = 'preset-card';
        presetCard.dataset.id = preset.id;
        
        const hasBacktest = preset.backtest_report !== null;
        const badgeHtml = hasBacktest 
            ? '<span class="badge success">With Backtest</span>' 
            : '<span class="badge warning">No Backtest</span>';
        
        let metricsHtml = '';
        if (preset.optimization_metrics) {
            metricsHtml = `
                <div class="preset-metrics">
                    <div class="metric">Profit: <strong>$${preset.optimization_metrics.profit?.toFixed(2) || 'N/A'}</strong></div>
                    <div class="metric">Trades: <strong>${preset.optimization_metrics.total_trades || 'N/A'}</strong></div>
                    <div class="metric">PF: <strong>${preset.optimization_metrics.profit_factor?.toFixed(2) || 'N/A'}</strong></div>
                </div>
            `;
        }
        
        presetCard.innerHTML = `
            <h4>
                <span>${preset.name} ${badgeHtml}</span>
                <input type="checkbox" onchange="togglePresetSelection('${preset.id}')">
            </h4>
            <div class="preset-info">
                <div>Created: ${new Date(preset.created_at).toLocaleString()}</div>
                <div>ID: ${preset.id}</div>
            </div>
            ${metricsHtml}
            <div class="actions">
                <button class="btn btn-primary btn-small" onclick="downloadSetFile('${preset.id}')">⬇️ Download .set</button>
                <button class="btn btn-secondary btn-small" onclick="uploadBacktest('${preset.id}')">📊 Upload Backtest</button>
                <button class="btn btn-secondary btn-small" onclick="deletePreset('${preset.id}')">🗑️ Delete</button>
            </div>
        `;
        
        presetsList.appendChild(presetCard);
    });
    
    comparisonSection.classList.remove('hidden');
}

function togglePresetSelection(presetId) {
    const presetCard = presetsList.querySelector(`[data-id="${presetId}"]`);
    if (selectedPresets.has(presetId)) {
        selectedPresets.delete(presetId);
        presetCard.classList.remove('selected');
    } else {
        selectedPresets.add(presetId);
        presetCard.classList.add('selected');
    }
}

async function downloadSetFile(presetId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/preset/${presetId}/download`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `preset_${presetId}.set`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            showStatus('.set file downloaded successfully', 'success');
        } else {
            showStatus('Failed to download .set file', 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function uploadBacktest(presetId) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.html,.htm';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('preset_id', presetId);
        
        showLoading(true);
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/upload/backtest`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                showStatus('Backtest report uploaded successfully', 'success');
                loadPresets(); // Reload to show updated status
            } else {
                showStatus(`Upload failed: ${result.error}`, 'error');
            }
        } catch (error) {
            showStatus(`Error: ${error.message}`, 'error');
        } finally {
            showLoading(false);
        }
    };
    input.click();
}

async function deletePreset(presetId) {
    if (!confirm('Are you sure you want to delete this preset?')) return;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/preset/${presetId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showStatus('Preset deleted successfully', 'success');
            loadPresets(); // Reload list
        } else {
            showStatus(`Delete failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

async function comparePresets() {
    if (selectedPresets.size < 2) {
        showStatus('Please select at least 2 presets to compare', 'error');
        return;
    }
    
    showLoading(true);
    showStatus('Comparing presets...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/preset/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                preset_ids: Array.from(selectedPresets)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayComparison(result.comparison);
            showStatus('Comparison complete', 'success');
        } else {
            showStatus(`Comparison failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayComparison(comparison) {
    const resultsDiv = document.getElementById('comparisonResults');
    if (!resultsDiv) return;
    
    let html = '<div class="comparison-metrics">';
    
    const metrics = comparison.metrics_comparison;
    if (metrics.best_profit) {
        html += `
            <div class="metric-card">
                <h5>Best Profit</h5>
                <div class="value">$${metrics.best_profit.value.toFixed(2)}</div>
                <div class="preset-name">${metrics.best_profit.name}</div>
            </div>
        `;
    }
    
    if (metrics.best_sharpe) {
        html += `
            <div class="metric-card">
                <h5>Best Sharpe Ratio</h5>
                <div class="value">${metrics.best_sharpe.value.toFixed(2)}</div>
                <div class="preset-name">${metrics.best_sharpe.name}</div>
            </div>
        `;
    }
    
    if (metrics.lowest_drawdown) {
        html += `
            <div class="metric-card">
                <h5>Lowest Drawdown</h5>
                <div class="value">$${metrics.lowest_drawdown.value.toFixed(2)}</div>
                <div class="preset-name">${metrics.lowest_drawdown.name}</div>
            </div>
        `;
    }
    
    if (metrics.best_profit_factor) {
        html += `
            <div class="metric-card">
                <h5>Best Profit Factor</h5>
                <div class="value">${metrics.best_profit_factor.value.toFixed(2)}</div>
                <div class="preset-name">${metrics.best_profit_factor.name}</div>
            </div>
        `;
    }
    
    html += '</div>';
    
    resultsDiv.innerHTML = html;
    
    // Display chart
    displayComparisonChart(comparison.chart_data);
}

function displayComparisonChart(chartData) {
    const canvas = document.getElementById('comparisonChart');
    if (!canvas) return;
    
    // Destroy existing chart if any
    if (comparisonChart) {
        comparisonChart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: 'Net Profit',
                    data: chartData.profit,
                    backgroundColor: 'rgba(37, 99, 235, 0.7)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Profit Factor',
                    data: chartData.profit_factor,
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function getGptComparison() {
    if (selectedPresets.size < 2) {
        showStatus('Please select at least 2 presets to compare', 'error');
        return;
    }
    
    showLoading(true);
    showStatus('Getting GPT comparative analysis...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/gpt/compare-presets`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                preset_ids: Array.from(selectedPresets)
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayGptComparison(result.gpt_analysis, result.comparison_data);
            showStatus('GPT analysis received', 'success');
        } else {
            showStatus(`Failed: ${result.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayGptComparison(analysis, comparisonData) {
    analysisResult.innerHTML = `
        <h3>🤖 GPT Comparative Analysis</h3>
        ${formatAnalysisText(analysis)}
    `;
    modal.classList.add('show');
}

// ===== UTILITY FUNCTIONS =====

function formatAnalysisText(text) {
    let formatted = text
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
    
    formatted = '<p>' + formatted + '</p>';
    formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    formatted = formatted.replace(/<\/ul>\s*<ul>/g, '');
    
    return formatted;
}

function showStatus(message, type) {
    if (!statusMessage) return;
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
    
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 5000);
}

function showLoading(show) {
    if (!loadingSpinner) return;
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

// ==================== Expert Dashboard Functions ====================

async function uploadDashboardBacktest() {
    if (!dashboardBacktestFile || !dashboardBacktestFile.files[0]) {
        showStatus('Please select a backtest report file', 'error');
        return;
    }
    
    const file = dashboardBacktestFile.files[0];
    
    try {
        showLoading(true);
        dashboardUploadStatus.textContent = 'Uploading and analyzing...';
        
        // Read file content
        const content = await readFileAsText(file);
        
        // Send to expert analysis endpoint
        const response = await fetch(`${API_BASE_URL}/api/experts/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                backtest_report: content,
                group_by: 'magic_number',
                calculate_equity: true,
                initial_balance: 10000
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            dashboardData = data;
            expertsData = data.experts;
            
            dashboardUploadStatus.textContent = `✓ Analyzed ${data.overall.experts_count} experts`;
            dashboardUploadStatus.style.color = 'var(--success-color)';
            
            // Show dashboard sections
            dashboardFiltersPanel.classList.remove('hidden');
            dashboardSummary.classList.remove('hidden');
            overallEquitySection.classList.remove('hidden');
            expertsSection.classList.remove('hidden');
            
            // Populate filters
            populateDashboardFilters();
            
            // Display dashboard
            displayDashboardSummary();
            displayOverallEquityCurve();
            displayExperts();
            
            showStatus('Dashboard loaded successfully!', 'success');
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Dashboard upload error:', error);
        dashboardUploadStatus.textContent = `✗ Error: ${error.message}`;
        dashboardUploadStatus.style.color = 'var(--error-color)';
        showStatus(`Failed to analyze: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsText(file);
    });
}

function populateDashboardFilters() {
    if (!dashboardData) return;
    
    // Populate magic number filter
    magicFilter.innerHTML = '';
    const magicNumbers = Object.keys(expertsData);
    magicNumbers.forEach(magic => {
        const option = document.createElement('option');
        option.value = magic;
        option.textContent = `Expert ${magic}`;
        option.selected = true;
        magicFilter.appendChild(option);
    });
    
    // Populate symbol filter
    const symbols = new Set();
    Object.values(expertsData).forEach(expert => {
        if (expert.metrics && expert.metrics.symbols) {
            expert.metrics.symbols.forEach(s => symbols.add(s));
        }
    });
    
    symbolFilter.innerHTML = '<option value="">All Symbols</option>';
    Array.from(symbols).sort().forEach(symbol => {
        const option = document.createElement('option');
        option.value = symbol;
        option.textContent = symbol;
        symbolFilter.appendChild(option);
    });
}

function displayDashboardSummary() {
    if (!dashboardData) return;
    
    const overall = dashboardData.overall;
    
    // Calculate overall metrics
    let totalProfit_val = 0;
    let totalTrades_val = 0;
    let totalWinningTrades = 0;
    
    Object.values(expertsData).forEach(expert => {
        const metrics = expert.metrics;
        totalProfit_val += metrics.net_profit || 0;
        totalTrades_val += metrics.total_trades || 0;
        totalWinningTrades += metrics.profit_trades || 0;
    });
    
    const overallWinRate_val = totalTrades_val > 0 ? (totalWinningTrades / totalTrades_val * 100).toFixed(2) : 0;
    
    // Update summary cards
    totalProfit.textContent = `$${totalProfit_val.toFixed(2)}`;
    totalProfit.style.color = totalProfit_val >= 0 ? 'var(--success-color)' : 'var(--error-color)';
    
    expertsCount.textContent = overall.experts_count || Object.keys(expertsData).length;
    overallWinRate.textContent = `${overallWinRate_val}%`;
    totalTrades.textContent = totalTrades_val;
}

function displayOverallEquityCurve() {
    if (!dashboardData || !dashboardData.overall || !dashboardData.overall.equity_curve) return;
    
    const equityCurve = dashboardData.overall.equity_curve;
    
    if (equityCurve.length === 0) return;
    
    // Prepare chart data
    const labels = equityCurve.map(point => {
        const date = new Date(point.timestamp);
        return date.toLocaleDateString();
    });
    
    const data = equityCurve.map(point => point.balance);
    
    // Destroy previous chart
    if (overallChart) {
        overallChart.destroy();
    }
    
    // Create new chart
    const ctx = overallEquityChart.getContext('2d');
    overallChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Overall Equity',
                data: data,
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return `Equity: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function displayExperts() {
    if (!expertsData) return;
    
    expertsContainer.innerHTML = '';
    
    // Convert to array for sorting
    const expertsArray = Object.entries(expertsData).map(([magic, data]) => ({
        magic: parseInt(magic),
        data: data
    }));
    
    // Sort experts
    sortExpertsArray(expertsArray);
    
    // Create expert cards
    expertsArray.forEach(({ magic, data }) => {
        const card = createExpertCard(magic, data);
        expertsContainer.appendChild(card);
    });
}

function createExpertCard(magic, expertData) {
    const metrics = expertData.metrics;
    const equityCurve = expertData.equity_curve || [];
    
    const card = document.createElement('div');
    card.className = 'expert-card';
    card.dataset.magic = magic;
    
    // Header
    const header = document.createElement('div');
    header.className = 'expert-card-header';
    header.innerHTML = `
        <h4>${expertData.name || `Expert ${magic}`}</h4>
        <input type="checkbox" class="expert-select-checkbox" 
               onchange="toggleExpertSelection(${magic})" 
               ${selectedExperts.has(magic) ? 'checked' : ''}>
    `;
    card.appendChild(header);
    
    // Metrics
    const metricsDiv = document.createElement('div');
    metricsDiv.className = 'expert-metrics';
    
    const profitClass = metrics.net_profit >= 0 ? 'positive' : 'negative';
    
    metricsDiv.innerHTML = `
        <div class="expert-metric">
            <span class="expert-metric-label">Net Profit</span>
            <span class="expert-metric-value ${profitClass}">$${metrics.net_profit.toFixed(2)}</span>
        </div>
        <div class="expert-metric">
            <span class="expert-metric-label">Win Rate</span>
            <span class="expert-metric-value">${metrics.win_rate.toFixed(2)}%</span>
        </div>
        <div class="expert-metric">
            <span class="expert-metric-label">Profit Factor</span>
            <span class="expert-metric-value">${metrics.profit_factor.toFixed(2)}</span>
        </div>
        <div class="expert-metric">
            <span class="expert-metric-label">Total Trades</span>
            <span class="expert-metric-value">${metrics.total_trades}</span>
        </div>
        <div class="expert-metric">
            <span class="expert-metric-label">Max Drawdown</span>
            <span class="expert-metric-value negative">${metrics.max_drawdown_percent.toFixed(2)}%</span>
        </div>
        <div class="expert-metric">
            <span class="expert-metric-label">Recovery Factor</span>
            <span class="expert-metric-value">${metrics.recovery_factor.toFixed(2)}</span>
        </div>
    `;
    card.appendChild(metricsDiv);
    
    // Mini equity chart
    if (equityCurve.length > 0) {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'expert-chart-container';
        
        const canvas = document.createElement('canvas');
        canvas.id = `expertChart_${magic}`;
        chartContainer.appendChild(canvas);
        card.appendChild(chartContainer);
        
        // Create chart after DOM update
        setTimeout(() => createExpertMiniChart(magic, equityCurve), 0);
    }
    
    return card;
}

function createExpertMiniChart(magic, equityCurve) {
    const canvas = document.getElementById(`expertChart_${magic}`);
    if (!canvas) return;
    
    const labels = equityCurve.map((point, idx) => idx);
    const data = equityCurve.map(point => point.balance);
    
    // Destroy previous chart if exists
    if (expertCharts[magic]) {
        expertCharts[magic].destroy();
    }
    
    const ctx = canvas.getContext('2d');
    expertCharts[magic] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 1.5,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
}

function toggleExpertSelection(magic) {
    if (selectedExperts.has(magic)) {
        selectedExperts.delete(magic);
    } else {
        selectedExperts.add(magic);
    }
    
    // Update card styling
    const card = document.querySelector(`.expert-card[data-magic="${magic}"]`);
    if (card) {
        if (selectedExperts.has(magic)) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    }
}

function sortExperts() {
    displayExperts();
}

function sortExpertsArray(expertsArray) {
    const sortBy = expertSortBy ? expertSortBy.value : 'profit';
    
    expertsArray.sort((a, b) => {
        const metricsA = a.data.metrics;
        const metricsB = b.data.metrics;
        
        switch (sortBy) {
            case 'profit':
                return metricsB.net_profit - metricsA.net_profit;
            case 'winrate':
                return metricsB.win_rate - metricsA.win_rate;
            case 'trades':
                return metricsB.total_trades - metricsA.total_trades;
            case 'profit_factor':
                return metricsB.profit_factor - metricsA.profit_factor;
            case 'recovery':
                return metricsB.recovery_factor - metricsA.recovery_factor;
            default:
                return 0;
        }
    });
}

async function compareExpertsFunc() {
    if (selectedExperts.size < 2) {
        showStatus('Please select at least 2 experts to compare', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        // Prepare data for comparison chart
        const datasets = [];
        const colors = [
            'rgb(37, 99, 235)',
            'rgb(16, 185, 129)',
            'rgb(245, 158, 11)',
            'rgb(239, 68, 68)',
            'rgb(139, 92, 246)',
            'rgb(236, 72, 153)'
        ];
        
        let maxLength = 0;
        const selectedArray = Array.from(selectedExperts);
        
        selectedArray.forEach((magic, idx) => {
            const expertData = expertsData[magic];
            if (!expertData || !expertData.equity_curve) return;
            
            const equityCurve = expertData.equity_curve;
            if (equityCurve.length > maxLength) {
                maxLength = equityCurve.length;
            }
            
            const data = equityCurve.map(point => point.balance);
            const color = colors[idx % colors.length];
            
            datasets.push({
                label: expertData.name || `Expert ${magic}`,
                data: data,
                borderColor: color,
                backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
                borderWidth: 2,
                fill: false,
                tension: 0.4
            });
        });
        
        // Create labels
        const labels = Array.from({ length: maxLength }, (_, i) => i);
        
        // Show comparison section
        expertComparisonSection.classList.remove('hidden');
        
        // Destroy previous chart
        if (expertComparisonChart) {
            expertComparisonChart.destroy();
        }
        
        // Create comparison chart
        const ctx = document.getElementById('expertComparisonChart').getContext('2d');
        expertComparisonChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(0);
                            }
                        }
                    }
                }
            }
        });
        
        // Display comparison metrics
        displayComparisonMetrics(selectedArray);
        
        showStatus('Experts compared successfully', 'success');
    } catch (error) {
        console.error('Comparison error:', error);
        showStatus(`Failed to compare: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function displayComparisonMetrics(expertIds) {
    if (!comparisonMetrics) return;
    
    comparisonMetrics.innerHTML = '';
    
    expertIds.forEach(magic => {
        const expertData = expertsData[magic];
        if (!expertData) return;
        
        const metrics = expertData.metrics;
        
        const card = document.createElement('div');
        card.className = 'comparison-metric-card';
        card.innerHTML = `
            <h5>${expertData.name || `Expert ${magic}`}</h5>
            <div class="value">Profit: $${metrics.net_profit.toFixed(2)}</div>
            <div>Win Rate: ${metrics.win_rate.toFixed(2)}%</div>
            <div>Profit Factor: ${metrics.profit_factor.toFixed(2)}</div>
            <div>Recovery: ${metrics.recovery_factor.toFixed(2)}</div>
            <div>Trades: ${metrics.total_trades}</div>
        `;
        
        comparisonMetrics.appendChild(card);
    });
}

function closeExpertComparison() {
    if (expertComparisonSection) {
        expertComparisonSection.classList.add('hidden');
    }
    
    if (expertComparisonChart) {
        expertComparisonChart.destroy();
        expertComparisonChart = null;
    }
}

function applyDashboardFiltersFunc() {
    // This would filter the displayed experts based on selected filters
    // For now, just show a message
    showStatus('Filters applied (functionality to be enhanced)', 'info');
}

function clearDashboardFiltersFunc() {
    // Clear all filters
    if (magicFilter) {
        Array.from(magicFilter.options).forEach(opt => opt.selected = true);
    }
    if (symbolFilter) symbolFilter.value = '';
    if (dateFrom) dateFrom.value = '';
    if (dateTo) dateTo.value = '';
    
    showStatus('Filters cleared', 'info');
}

// Export functions to global scope for inline event handlers
// Using a namespace to avoid pollution
window.MT5Analyzer = {
    removeStrategy,
    toggleParameterSelection,
    saveAsPreset,
    togglePresetSelection,
    downloadSetFile,
    uploadBacktest,
    deletePreset,
    toggleExpertSelection
};

// For backward compatibility with inline handlers
window.removeStrategy = removeStrategy;
window.toggleParameterSelection = toggleParameterSelection;
window.saveAsPreset = saveAsPreset;
window.togglePresetSelection = togglePresetSelection;
window.downloadSetFile = downloadSetFile;
window.uploadBacktest = uploadBacktest;
window.deletePreset = deletePreset;
window.toggleExpertSelection = toggleExpertSelection;
