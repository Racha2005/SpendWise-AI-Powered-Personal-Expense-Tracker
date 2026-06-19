/**
 * SpendWise Chart Library
 * All Chart.js chart initializers with dark neon theme
 */

// ── Global Chart Defaults ──────────────────────────────────
Chart.defaults.color          = '#8b8ba7';
Chart.defaults.borderColor    = 'rgba(255,255,255,0.06)';
Chart.defaults.font.family    = 'Inter, sans-serif';
Chart.defaults.font.size      = 11;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding       = 16;
Chart.defaults.plugins.tooltip.backgroundColor     = 'rgba(10,10,20,0.95)';
Chart.defaults.plugins.tooltip.borderColor         = 'rgba(168,85,247,0.3)';
Chart.defaults.plugins.tooltip.borderWidth         = 1;
Chart.defaults.plugins.tooltip.padding             = 12;
Chart.defaults.plugins.tooltip.titleColor          = '#f0f0ff';
Chart.defaults.plugins.tooltip.bodyColor           = '#8b8ba7';
Chart.defaults.plugins.tooltip.cornerRadius        = 10;

const NEON = {
  purple: '#a855f7', blue:   '#3b82f6', cyan:   '#06b6d4',
  green:  '#22c55e', pink:   '#ec4899', orange: '#f97316',
  yellow: '#eab308', red:    '#ef4444',
};

function rgba(hex, alpha) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${alpha})`;
}

// ── Area Chart (Monthly Trend) ─────────────────────────────
function initAreaChart(canvasId, labels, data, label, color) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label,
        data,
        borderColor:     color,
        backgroundColor: rgba(color, 0.12),
        borderWidth:     2.5,
        fill:            true,
        tension:         0.4,
        pointBackgroundColor: color,
        pointBorderColor:     'rgba(10,10,20,0.8)',
        pointBorderWidth:     2,
        pointRadius:          4,
        pointHoverRadius:     7,
      }]
    },
    options: {
      responsive: true,
      interaction: { intersect: false, mode: 'index' },
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' }, beginAtZero: true },
      }
    }
  });
}

// ── Bar Chart ──────────────────────────────────────────────
function initBarChart(canvasId, labels, data, label) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  const colors = [NEON.purple, NEON.blue, NEON.cyan, NEON.green, NEON.pink, NEON.orange, NEON.yellow];

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label,
        data,
        backgroundColor: labels.map((_, i) => rgba(colors[i % colors.length], 0.7)),
        borderColor:     labels.map((_, i) => colors[i % colors.length]),
        borderWidth:     2,
        borderRadius:    8,
        borderSkipped:   false,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#55556a' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' }, beginAtZero: true },
      }
    }
  });
}

// ── Donut Chart ────────────────────────────────────────────
function initDonutChart(canvasId, labels, data, colors) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  const fallbackColors = Object.values(NEON);
  const bgColors = colors && colors.length ? colors : labels.map((_, i) => fallbackColors[i % fallbackColors.length]);

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: bgColors.map(c => c ? rgba(c.startsWith('#') ? c : '#a855f7', 0.8) : rgba(NEON.purple, 0.8)),
        borderColor:     bgColors.map(c => c || NEON.purple),
        borderWidth:     2,
        hoverOffset:     8,
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#8b8ba7', padding: 10, font: { size: 11 } }
        },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed.toLocaleString()}`
          }
        }
      }
    }
  });
}

// ── Pie Chart ──────────────────────────────────────────────
function initPieChart(canvasId, labels, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  const colors = Object.values(NEON);

  return new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: labels.map((_, i) => rgba(colors[i % colors.length], 0.75)),
        borderColor:     labels.map((_, i) => colors[i % colors.length]),
        borderWidth: 2,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#8b8ba7', padding: 12 } }
      }
    }
  });
}

// ── YoY Comparison Chart ───────────────────────────────────
function initYoYChart(canvasId, labels, currentData, prevData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'This Year',
          data: currentData,
          backgroundColor: rgba(NEON.purple, 0.7),
          borderColor:     NEON.purple,
          borderWidth: 2,
          borderRadius: 5,
        },
        {
          label: 'Last Year',
          data: prevData,
          backgroundColor: rgba(NEON.blue, 0.4),
          borderColor:     NEON.blue,
          borderWidth: 2,
          borderRadius: 5,
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { labels: { color: '#8b8ba7' } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#55556a' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' }, beginAtZero: true }
      }
    }
  });
}

// ── Forecast Chart ─────────────────────────────────────────
function initForecastChart(canvasId, labels, histData, futureData, splitIndex) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  // Combine: fill future part with null for hist dataset and vice versa
  const histFull   = [...histData, ...futureData.map(() => null)];
  const futureFull = [...histData.map(() => null), ...futureData];

  // Bridge point: last hist into future
  if (splitIndex > 0 && histData.length > 0) {
    futureFull[splitIndex - 1] = histData[histData.length - 1];
  }

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Historical',
          data:  histFull,
          borderColor:     NEON.cyan,
          backgroundColor: rgba(NEON.cyan, 0.08),
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointRadius:      histFull.map((v, i) => v !== null ? 4 : 0),
          pointBackgroundColor: NEON.cyan,
          spanGaps: false,
        },
        {
          label: 'AI Forecast',
          data:  futureFull,
          borderColor:     NEON.purple,
          backgroundColor: rgba(NEON.purple, 0.1),
          borderWidth:  2.5,
          borderDash:   [8, 4],
          fill: true,
          tension: 0.4,
          pointRadius:      futureFull.map((v, i) => v !== null ? 5 : 0),
          pointBackgroundColor: NEON.purple,
          pointBorderColor:     'rgba(10,10,20,0.8)',
          pointBorderWidth:     2,
          spanGaps: false,
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { labels: { color: '#8b8ba7' } },
        tooltip: {
          callbacks: {
            afterTitle: items => items.some(i => i.datasetIndex === 1) ? '🤖 AI Prediction' : ''
          }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#55556a' }, beginAtZero: true }
      }
    }
  });
}
