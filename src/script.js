document.documentElement.classList.add('js');

const PANEL_WEIGHTS = {
  identity: 30,
  content: 20,
  tfa: 15,
  solvents: 15,
  endotoxin: 15,
  source: 5
};

const PANEL_LABELS = {
  identity: 'Identity',
  content: 'Content',
  tfa: 'TFA',
  solvents: 'Solvents',
  endotoxin: 'Endotoxin',
  source: 'Source'
};

const STATUS_POINTS = {
  verified: 1,
  partial: 0.55,
  source: 0.35,
  missing: 0,
  mismatch: 0
};

const STATUS_TEXT = {
  verified: 'Verified',
  partial: 'Partial',
  source: 'Source row',
  missing: 'No public proof',
  mismatch: 'Mismatch risk'
};

const DEFAULT_PANEL = {
  identity: {
    status: 'source',
    note: 'Vendor appears under this product in a public source row; batch identity still needs lab-level proof.'
  },
  content: {
    status: 'partial',
    note: 'Headline ranking implies assay/content relevance, but exact fill amount has not been extracted into CleanPep yet.'
  },
  tfa: {
    status: 'missing',
    note: 'No public TFA or counter-ion result found in CleanPep data yet.'
  },
  solvents: {
    status: 'missing',
    note: 'No public residual-solvent panel found in CleanPep data yet.'
  },
  endotoxin: {
    status: 'missing',
    note: 'No public endotoxin result found in CleanPep data yet.'
  },
  source: {
    status: 'verified',
    note: 'Included from a dated public source snapshot; verify live before relying on it.'
  }
};

const EVIDENCE_OVERRIDES = {
  // Add verified COA panels here as they are collected. Keep unknowns missing until there is a public lab source.
  // Example shape:
  // retatrutide: {
  //   'example vendor': {
  //     panels: {
  //       tfa: { status: 'verified', value: '0.08%', note: 'Batch COA, Janoshik report URL...' },
  //       solvents: { status: 'verified', value: 'Pass', note: 'Residual solvents panel attached to batch COA.' }
  //     }
  //   }
  // }
};

const revealItems = document.querySelectorAll('[data-reveal]');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}

document.querySelectorAll('[data-filter]').forEach((input) => {
  const selector = input.getAttribute('data-filter');
  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll(selector).forEach((item) => {
      const haystack = (item.getAttribute('data-search') || item.textContent || '').toLowerCase();
      item.classList.toggle('is-hidden', query.length > 0 && !haystack.includes(query));
    });
  });
});

function normalizeText(value) {
  return (value || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}

function currentProductKey() {
  const file = window.location.pathname.split('/').pop().replace('.html', '');
  if (!file || file === 'index') return 'retatrutide';
  return file.replace('bpc157', 'bpc-157');
}

function clonePanel(panel) {
  return Object.fromEntries(Object.entries(panel).map(([key, value]) => [key, { ...value }]));
}

function getEvidence(product, vendor) {
  const base = clonePanel(DEFAULT_PANEL);
  const productOverrides = EVIDENCE_OVERRIDES[product] || {};
  const override = productOverrides[normalizeText(vendor)] || {};
  if (override.panels) {
    Object.entries(override.panels).forEach(([key, value]) => {
      base[key] = { ...base[key], ...value };
    });
  }
  return { panels: base, source: override.source || 'CleanPep public-source queue' };
}

function scoreEvidence(panels) {
  return Math.round(Object.entries(PANEL_WEIGHTS).reduce((sum, [key, weight]) => {
    const status = panels[key]?.status || 'missing';
    return sum + weight * (STATUS_POINTS[status] ?? 0);
  }, 0));
}

function scoreLabel(score) {
  if (score >= 80) return 'Deep panel';
  if (score >= 55) return 'Good coverage';
  if (score >= 35) return 'Needs review';
  return 'Purity-first only';
}

function panelMarkup(panels) {
  return Object.entries(PANEL_LABELS).map(([key, label]) => {
    const panel = panels[key] || { status: 'missing', note: 'No public proof found.' };
    const value = panel.value ? ` <strong>${escapeHtml(panel.value)}</strong>` : '';
    return `<span class="panel-chip ${panel.status}" title="${escapeHtml(panel.note || '')}">${label}${value}</span>`;
  }).join('');
}

function panelListMarkup(panels) {
  return Object.entries(PANEL_LABELS).map(([key, label]) => {
    const panel = panels[key] || { status: 'missing', note: 'No public proof found.' };
    const value = panel.value ? `: ${escapeHtml(panel.value)}` : '';
    return `<li><span>${label}</span><strong class="${panel.status}">${STATUS_TEXT[panel.status] || 'Unknown'}${value}</strong><small>${escapeHtml(panel.note || '')}</small></li>`;
  }).join('');
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function enhanceVendorCards() {
  const product = currentProductKey();
  document.querySelectorAll('.vendor-card').forEach((card) => {
    const vendor = card.querySelector('h3')?.textContent?.trim();
    if (!vendor || card.querySelector('.evidence-summary')) return;
    const evidence = getEvidence(product, vendor);
    const score = scoreEvidence(evidence.panels);
    card.insertAdjacentHTML('beforeend', `
      <div class="evidence-summary" tabindex="0" aria-label="Evidence depth for ${escapeHtml(vendor)}">
        <div class="evidence-score"><span>${score}</span><small>/100 ${scoreLabel(score)}</small></div>
        <div class="panel-strip">${panelMarkup(evidence.panels)}</div>
        <div class="evidence-popover" role="tooltip">
          <strong>Loaded public COA panels</strong>
          <ul>${panelListMarkup(evidence.panels)}</ul>
          <p>No green chip means CleanPep has not loaded public proof for that panel yet.</p>
        </div>
      </div>
    `);
  });
}

function enhanceTables() {
  const product = currentProductKey();
  document.querySelectorAll('table').forEach((table) => {
    if (table.dataset.evidenceEnhanced === 'true') return;
    const headerRow = table.querySelector('thead tr');
    if (!headerRow) return;
    headerRow.insertAdjacentHTML('beforeend', '<th>Panel depth</th>');
    table.querySelectorAll('tbody tr').forEach((row) => {
      const vendor = row.children[1]?.textContent?.trim();
      const evidence = getEvidence(product, vendor);
      const score = scoreEvidence(evidence.panels);
      row.insertAdjacentHTML('beforeend', `<td><div class="table-evidence"><strong>${score}/100</strong><span>${scoreLabel(score)}</span><div>${panelMarkup(evidence.panels)}</div></div></td>`);
      row.dataset.search = `${row.dataset.search || ''} ${scoreLabel(score)} ${Object.values(PANEL_LABELS).join(' ')}`.toLowerCase();
    });
    table.dataset.evidenceEnhanced = 'true';
  });
}

enhanceVendorCards();
enhanceTables();

function addPanelFinder() {
  const cards = Array.from(document.querySelectorAll('.vendor-card'));
  if (!cards.length || document.querySelector('[data-panel-finder]')) return;
  const firstSection = cards[0].closest('section');
  if (!firstSection) return;
  firstSection.insertAdjacentHTML('beforebegin', `
    <section class="data-section panel-finder" data-panel-finder data-reveal>
      <div class="section-heading">
        <div><p class="eyebrow">Find what actually passed</p><h2>Filter for loaded COA panels</h2></div>
        <button class="btn btn-outline" type="button" data-clear-panels>Clear</button>
      </div>
      <div class="panel-controls" role="group" aria-label="Required COA panels">
        <label><input type="checkbox" value="solvents"> Residual solvents</label>
        <label><input type="checkbox" value="tfa"> TFA</label>
        <label><input type="checkbox" value="endotoxin"> Endotoxin</label>
        <label><input type="checkbox" value="content"> Content/fill</label>
        <label><input type="checkbox" value="identity"> Identity match</label>
      </div>
      <div class="finder-result" data-panel-result>Pick a panel to find vendors with public proof loaded.</div>
    </section>
  `);

  const finder = document.querySelector('[data-panel-finder]');
  const inputs = Array.from(finder.querySelectorAll('input[type="checkbox"]'));
  const result = finder.querySelector('[data-panel-result]');
  const clear = finder.querySelector('[data-clear-panels]');
  const product = currentProductKey();

  function applyPanelFilter() {
    const required = inputs.filter((input) => input.checked).map((input) => input.value);
    let matches = 0;
    cards.forEach((card) => {
      const vendor = card.querySelector('h3')?.textContent?.trim();
      const evidence = getEvidence(product, vendor);
      const passes = required.length === 0 || required.every((key) => evidence.panels[key]?.status === 'verified');
      card.classList.toggle('panel-hidden', !passes);
      if (passes) matches += 1;
    });
    document.querySelectorAll('tbody tr').forEach((row) => {
      const vendor = row.children[1]?.textContent?.trim();
      const evidence = getEvidence(product, vendor);
      const passes = required.length === 0 || required.every((key) => evidence.panels[key]?.status === 'verified');
      row.classList.toggle('panel-hidden', !passes);
    });

    if (!required.length) {
      result.textContent = 'Pick a panel to find vendors with public proof loaded.';
    } else if (matches === 0) {
      const names = required.map((key) => PANEL_LABELS[key]).join(' + ');
      result.textContent = `No ${names} match is loaded yet for this product. Treat the visible vendors as a COA collection queue, not a clean-panel shortlist.`;
    } else {
      result.textContent = `${matches} vendor${matches === 1 ? '' : 's'} with public proof loaded for the selected panel${required.length === 1 ? '' : 's'}.`;
    }
  }

  inputs.forEach((input) => input.addEventListener('change', applyPanelFilter));
  clear.addEventListener('click', () => {
    inputs.forEach((input) => { input.checked = false; });
    applyPanelFilter();
  });
}

addPanelFinder();
