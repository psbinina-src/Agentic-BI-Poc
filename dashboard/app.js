const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 });
const compactCurrency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 });

const kpiContainer = document.getElementById('kpis');
const semanticView = document.getElementById('semantic-view');
const inventoryTable = document.getElementById('inventory-table');

const startDateInput = document.getElementById('start-date');
const endDateInput = document.getElementById('end-date');
const productFilter = document.getElementById('product-filter');
const customerFilter = document.getElementById('customer-filter');
const resetButton = document.getElementById('reset-filters');
let dashboardData = null;

function toDateValue(value) {
  if (!value) return null;
  return new Date(value + 'T00:00:00');
}

function applyFilters(rows, state) {
  return rows.filter((row) => {
    const rowDate = toDateValue(row.order_date);
    const startDate = toDateValue(state.startDate);
    const endDate = toDateValue(state.endDate);

    if (startDate && rowDate < startDate) return false;
    if (endDate && rowDate > endDate) return false;
    if (state.product && row.product_name !== state.product) return false;
    if (state.customer && row.customer_id !== state.customer) return false;
    return true;
  });
}

function buildSummary(rows) {
  const totalNet = rows.reduce((sum, row) => sum + Number(row.net_sales_amount || 0), 0);
  const totalGross = rows.reduce((sum, row) => sum + Number(row.gross_sales_amount || 0), 0);
  const totalUnits = rows.reduce((sum, row) => sum + Number(row.quantity || 0), 0);
  const totalOrders = new Set(rows.map((row) => row.order_id)).size;
  const avgOrder = totalOrders ? totalNet / totalOrders : 0;

  return {
    net_sales: totalNet,
    gross_sales: totalGross,
    units_sold: totalUnits,
    total_orders: totalOrders,
    avg_order_value: avgOrder,
  };
}

function buildRegionSeries(rows) {
  const map = new Map();
  for (const row of rows) {
    const label = row.region || 'Unknown';
    map.set(label, (map.get(label) || 0) + Number(row.net_sales_amount || 0));
  }
  return Array.from(map, ([label, value]) => ({ label, value }));
}

function buildChannelSeries(rows) {
  const map = new Map();
  for (const row of rows) {
    const label = row.channel || 'Unknown';
    map.set(label, (map.get(label) || 0) + Number(row.net_sales_amount || 0));
  }
  return Array.from(map, ([label, value]) => ({ label, value }));
}

function buildTrendSeries(rows) {
  const map = new Map();
  for (const row of rows) {
    const label = row.order_date;
    map.set(label, (map.get(label) || 0) + Number(row.net_sales_amount || 0));
  }
  return Array.from(map, ([label, value]) => ({ label, value })).sort((a, b) => new Date(a.label) - new Date(b.label));
}

function renderKpis(summary) {
  const cards = [
    { label: 'Net sales', value: currency.format(summary.net_sales) },
    { label: 'Gross sales', value: currency.format(summary.gross_sales) },
    { label: 'Units sold', value: Intl.NumberFormat('en-US').format(summary.units_sold) },
    { label: 'Orders', value: Intl.NumberFormat('en-US').format(summary.total_orders) },
    { label: 'Avg order value', value: currency.format(summary.avg_order_value) },
  ];

  kpiContainer.innerHTML = cards.map((card) => `
    <div class="kpi-card">
      <div class="kpi-label">${card.label}</div>
      <div class="kpi-value">${card.value}</div>
    </div>
  `).join('');
}

function renderSemanticView(tableDefs) {
  semanticView.innerHTML = tableDefs.map((table) => `
    <article class="semantic-card">
      <h3>${table.table}</h3>
      <p>${table.description}</p>
      <p><strong>Key fields:</strong> ${table.key_fields.join(', ')}</p>
      <p><strong>Dimensions:</strong> ${table.dimensions.join(', ') || '—'}</p>
      <ul>
        ${table.measures.length ? table.measures.map((measure) => `<li>${measure}</li>`).join('') : '<li>No derived measures defined</li>'}
      </ul>
    </article>
  `).join('');
}

function renderTable(data) {
  inventoryTable.innerHTML = data.map((row) => `
    <tr>
      <td>${row.product_name}</td>
      <td>${row.inventory_on_hand}</td>
      <td>${row.sales_velocity.toFixed(3)}</td>
      <td>${row.stock_coverage_days.toFixed(1)}</td>
      <td>
        <span class="status ${row.low_stock_flag ? 'low' : 'safe'}">
          ${row.low_stock_flag ? 'Low stock' : 'Healthy'}
        </span>
      </td>
    </tr>
  `).join('');
}

function renderChart(canvasId, labels, values, colorSet, type = 'bar') {
  const ctx = document.getElementById(canvasId);
  if (ctx.chart) ctx.chart.destroy();
  const isTrend = canvasId === 'trendChart';
  const trendFill = ctx.getContext('2d').createLinearGradient(0, 0, 0, 250);
  trendFill.addColorStop(0, 'rgba(46, 108, 243, 0.22)');
  trendFill.addColorStop(1, 'rgba(46, 108, 243, 0.01)');

  ctx.chart = new Chart(ctx, {
    type,
    data: {
      labels,
      datasets: [{
        label: canvasId.includes('trend') ? 'Daily sales' : 'Net sales',
        data: values,
        borderColor: colorSet[0],
        backgroundColor: isTrend ? trendFill : colorSet,
        fill: isTrend ? 'origin' : type !== 'doughnut',
        borderWidth: isTrend ? 2.5 : 1,
        pointRadius: isTrend ? 0 : undefined,
        pointHoverRadius: isTrend ? 4 : undefined,
        pointHitRadius: isTrend ? 8 : undefined,
        tension: isTrend ? 0.25 : 0,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false } },
      scales: type === 'doughnut' ? {} : {
        x: {
          grid: { display: !isTrend, color: 'rgba(31, 42, 55, 0.06)' },
          ticks: {
            color: '#5a687a',
            maxTicksLimit: isTrend ? 8 : undefined,
            maxRotation: 0,
            callback: isTrend
              ? function (value) {
                return new Date(`${this.getLabelForValue(value)}T00:00:00`).toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
              }
              : undefined,
          },
        },
        y: {
          grid: { color: 'rgba(31, 42, 55, 0.08)' },
          ticks: {
            color: '#5a687a',
            callback: (value) => compactCurrency.format(Number(value)),
          },
        },
      },
    },
  });
}

function populateFilters() {
  const filters = dashboardData.filters;
  const productValues = ['All products', ...filters.products];
  const customerValues = ['All customers', ...filters.customers];

  productFilter.innerHTML = productValues.map((item) => `<option value="${item === 'All products' ? '' : item}">${item}</option>`).join('');
  customerFilter.innerHTML = customerValues.map((item) => `<option value="${item === 'All customers' ? '' : item}">${item}</option>`).join('');

  startDateInput.min = filters.date_min;
  startDateInput.max = filters.date_max;
  endDateInput.min = filters.date_min;
  endDateInput.max = filters.date_max;
  startDateInput.value = filters.date_min;
  endDateInput.value = filters.date_max;
}

function renderDashboard() {
  const state = {
    startDate: startDateInput.value || dashboardData.filters.date_min,
    endDate: endDateInput.value || dashboardData.filters.date_max,
    product: productFilter.value || '',
    customer: customerFilter.value || '',
  };

  const filteredRows = applyFilters(dashboardData.sales_rows, state);
  const summary = buildSummary(filteredRows);
  const regionSeries = buildRegionSeries(filteredRows);
  const channelSeries = buildChannelSeries(filteredRows);
  const trendSeries = buildTrendSeries(filteredRows);

  const inventoryFiltered = dashboardData.inventory_risk.filter((row) => {
    if (state.product && row.product_name !== state.product) return false;
    return true;
  });

  document.getElementById('dashboard-title').textContent = dashboardData.dashboard_title;
  renderKpis(summary);
  renderTable(inventoryFiltered.slice(0, 10));

  renderChart(
    'regionChart',
    regionSeries.map((item) => item.label),
    regionSeries.map((item) => item.value),
    ['#2e6cf3', '#4facfe', '#14b8a6', '#34d399', '#f59e0b'],
    'bar'
  );

  renderChart(
    'channelChart',
    channelSeries.map((item) => item.label),
    channelSeries.map((item) => item.value),
    ['#14b8a6', '#2e6cf3', '#f59e0b', '#ef4444'],
    'doughnut'
  );

  renderChart(
    'trendChart',
    trendSeries.map((item) => item.label),
    trendSeries.map((item) => item.value),
    ['#2e6cf3'],
    'line'
  );
}

function resetFilters() {
  startDateInput.value = dashboardData.filters.date_min;
  endDateInput.value = dashboardData.filters.date_max;
  productFilter.value = '';
  customerFilter.value = '';
  renderDashboard();
}

fetch('data.json')
  .then((response) => response.json())
  .then((payload) => {
    dashboardData = payload;
    populateFilters();
    renderDashboard();

    [startDateInput, endDateInput, productFilter, customerFilter].forEach((element) => {
      element.addEventListener('change', renderDashboard);
    });
    resetButton.addEventListener('click', resetFilters);
    renderSemanticView(payload.semantic_view);
  })
  .catch((error) => {
    const root = document.querySelector('main');
    root.innerHTML = `<div class="panel"><h2>Dashboard data unavailable</h2><p>${error.message}</p></div>`;
  });
