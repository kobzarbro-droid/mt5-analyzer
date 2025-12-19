// MT5 Portfolio Analyzer - Frontend JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// State management
let strategies = [];
let currentAnalysis = null;

// DOM elements
let strategiesContainer;
let analyzeBtn;
let addStrategyBtn;
let loadSampleBtn;
let statusMessage;
let loadingSpinner;
let modal;
let analysisResult;
let closeModalBtn;
let exportBtn;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    addStrategy(); // Add first strategy by default
});

function initializeElements() {
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
}

function setupEventListeners() {
    analyzeBtn.addEventListener('click', analyzePortfolio);
    addStrategyBtn.addEventListener('click', addStrategy);
    loadSampleBtn.addEventListener('click', loadSampleData);
    closeModalBtn.addEventListener('click', closeModal);
    exportBtn.addEventListener('click', exportAnalysis);
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    
    // Close modal with ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
    
    // Close modal with close button
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
}

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
    
    // Disable add button if at max strategies
    if (strategies.length >= 5) {
        addStrategyBtn.disabled = true;
    }
}

function removeStrategy(index) {
    const strategyCard = document.querySelector(`[data-index="${index}"]`);
    if (strategyCard) {
        strategyCard.remove();
        strategies = strategies.filter(s => s !== index);
        
        // Re-enable add button if below max
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
    
    // Show loading state
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
    
    // Format the analysis text with proper HTML
    let formattedAnalysis = result.full_analysis;
    
    // Convert markdown-style formatting to HTML
    formattedAnalysis = formattedAnalysis
        // Bold text
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        // Headers
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        // Lists (simple conversion)
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
    
    // Wrap in paragraph tags
    formattedAnalysis = '<p>' + formattedAnalysis + '</p>';
    
    // Clean up list items
    formattedAnalysis = formattedAnalysis.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    formattedAnalysis = formattedAnalysis.replace(/<\/ul>\s*<ul>/g, '');
    
    const metaInfo = `
        <div style="background: var(--background); padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
            <p><strong>Strategies Analyzed:</strong> ${result.strategies_count}</p>
            <p><strong>AI Model:</strong> ${result.model}</p>
        </div>
    `;
    
    analysisResult.innerHTML = metaInfo + formattedAnalysis;
    
    // Show modal
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
}

function exportAnalysis() {
    if (!currentAnalysis) {
        showStatus('No analysis to export', 'error');
        return;
    }
    
    const exportData = {
        timestamp: new Date().toISOString(),
        strategies_count: currentAnalysis.strategies_count,
        model: currentAnalysis.model,
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
    // Clear existing strategies
    strategiesContainer.innerHTML = '';
    strategies = [];
    
    // Sample data
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
        },
        {
            name: 'Grid Trading Strategy',
            equity: 88000,
            drawdown: -22.5,
            correlation: 0.28,
            recovery: 1.5,
            profit: -12.0
        },
        {
            name: 'Scalping Strategy',
            equity: 115000,
            drawdown: -15.8,
            correlation: 0.38,
            recovery: 2.1,
            profit: 15.0
        }
    ];
    
    // Add strategies with data
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

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 5000);
}

function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}
