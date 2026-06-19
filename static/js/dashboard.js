/**
 * SpendWise — Dashboard Interactivity
 */

// ── Animated number counters on KPI cards ─────────────────
function animateCounter(el, target, prefix = '', decimals = 0) {
  const duration = 1200;
  const start    = performance.now();
  const from     = 0;

  function update(now) {
    const elapsed  = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
    const value    = from + (target - from) * eased;
    el.textContent = prefix + value.toLocaleString('en-IN', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

document.addEventListener('DOMContentLoaded', () => {
  // Animate all KPI values
  document.querySelectorAll('.kpi-value[data-value]').forEach(el => {
    const val     = parseFloat(el.dataset.value) || 0;
    const prefix  = el.dataset.prefix || '';
    const dec     = parseInt(el.dataset.decimals || '0');
    animateCounter(el, val, prefix, dec);
  });

  // Animate progress bars
  document.querySelectorAll('.progress-bar-fill[data-width]').forEach(el => {
    setTimeout(() => {
      el.style.width = el.dataset.width + '%';
    }, 200);
  });

  // Animate health ring stroke
  const ring = document.querySelector('.health-ring-stroke');
  if (ring) {
    const score       = parseFloat(ring.dataset.score) || 0;
    const circumference = 314.16;
    setTimeout(() => {
      ring.style.strokeDasharray = `${(score / 100) * circumference} ${circumference}`;
    }, 300);
  }
});

// ── Tooltip initializer (lightweight) ────────────────────
document.querySelectorAll('[data-tooltip]').forEach(el => {
  el.style.position = 'relative';
  el.addEventListener('mouseenter', () => {
    const tip = document.createElement('div');
    tip.className = '__tip';
    tip.textContent = el.dataset.tooltip;
    tip.style.cssText = `
      position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);
      background:rgba(10,10,20,0.95);border:1px solid rgba(168,85,247,0.3);
      color:#f0f0ff;padding:6px 12px;border-radius:8px;font-size:.75rem;
      white-space:nowrap;z-index:9999;pointer-events:none;
      box-shadow:0 4px 16px rgba(0,0,0,0.4);
    `;
    el.appendChild(tip);
  });
  el.addEventListener('mouseleave', () => {
    el.querySelector('.__tip')?.remove();
  });
});
