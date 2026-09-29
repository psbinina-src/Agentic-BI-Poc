const questionInput = document.getElementById('question');
const askButton = document.getElementById('ask-button');
const status = document.getElementById('status');
const result = document.getElementById('result');
const chartCard = document.getElementById('chart-card');
const chartContainer = document.getElementById('chart');

async function askQuestion(question) {
  if (!question.trim()) {
    questionInput.focus();
    return;
  }

  askButton.disabled = true;
  askButton.innerHTML = '<span>Analyzing…</span><span class="spinner" aria-hidden="true"></span>';
  status.textContent = 'Discovering Gold data and preparing your analysis…';
  status.classList.add('visible');
  result.classList.add('hidden');
  chartCard.classList.add('hidden');
  chartContainer.replaceChildren();

  try {
    const response = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'The analytics request could not be completed.');

    document.getElementById('answer').textContent = payload.answer;
    document.getElementById('insight').textContent = payload.insight;
    renderTable(payload.data);
    result.classList.remove('hidden');

    if (payload.chart) {
      chartCard.classList.remove('hidden');
      await vegaEmbed(chartContainer, payload.chart, { actions: false, renderer: 'canvas' });
    }
    status.textContent = '';
    status.classList.remove('visible');
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (error) {
    status.textContent = error.message;
    status.classList.add('error');
  } finally {
    askButton.disabled = false;
    askButton.innerHTML = '<span>Analyze</span><span aria-hidden="true">↗</span>';
  }
}

function renderTable(data) {
  const head = document.getElementById('data-head');
  const body = document.getElementById('data-body');
  head.replaceChildren();
  body.replaceChildren();
  if (!data || !Array.isArray(data.columns) || !Array.isArray(data.rows)) return;

  const headingRow = document.createElement('tr');
  data.columns.forEach((column) => {
    const th = document.createElement('th');
    th.textContent = column;
    headingRow.appendChild(th);
  });
  head.appendChild(headingRow);

  data.rows.forEach((row) => {
    const tr = document.createElement('tr');
    data.columns.forEach((column) => {
      const td = document.createElement('td');
      const value = row[column];
      td.textContent = typeof value === 'number' ? new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 }).format(value) : String(value ?? '—');
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
}

askButton.addEventListener('click', () => askQuestion(questionInput.value));
questionInput.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') askQuestion(questionInput.value);
});
document.querySelectorAll('.suggestion').forEach((button) => {
  button.addEventListener('click', () => {
    questionInput.value = button.textContent;
    askQuestion(button.textContent);
  });
});
document.getElementById('clear-button').addEventListener('click', () => {
  result.classList.add('hidden');
  status.textContent = '';
  questionInput.focus();
});

fetch('/health')
  .then((response) => response.json())
  .then((health) => {
    const label = document.getElementById('connection-label');
    label.textContent = health.openai_configured ? 'Connected to local Gold API' : 'Set OPENAI_API_KEY to enable analysis';
    if (!health.openai_configured) label.classList.add('connection-warning');
  })
  .catch(() => {
    document.getElementById('connection-label').textContent = 'Agent service unavailable';
  });
