'use client';

export default function FinalReport({ report }) {
  if (!report) return null;

  const score = report.portfolio_health_score;
  const scoreColor =
    score > 70
      ? 'var(--accent-green)'
      : score > 40
      ? 'var(--accent-warning)'
      : 'var(--accent-danger)';

  return (
    <section className="panel report-panel">
      <div className="panel-header">
        <h2>
          <i className="fa-solid fa-clipboard-check"></i> Advisory Report
        </h2>
      </div>
      <div className="panel-body">
        <div className="score-display">
          <div className="score-circle" style={{ borderColor: scoreColor, color: scoreColor }}>
            {score}
          </div>
          <div>
            <h3 style={{ marginBottom: 4, fontSize: '1rem' }}>Portfolio Health Score</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Out of 100 — based on risk analysis &amp; anomalies
            </p>
          </div>
        </div>

        <p className="report-summary">{report.summary}</p>

        <div className="action-items">
          <h4>Recommended Actions</h4>
          <ul>
            {report.action_items.map((item, idx) => (
              <li key={idx}>
                <i className="fa-solid fa-arrow-right"></i>
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
