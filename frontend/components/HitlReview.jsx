'use client';

export default function HitlReview({ anomalies, decisions, onDecision, onSubmit }) {
  const allDecided = anomalies.every((a) => decisions[a.transaction_id] !== undefined);

  return (
    <div className="hitl-review">
      <div className="hitl-header">
        <h3>
          <i className="fa-solid fa-triangle-exclamation"></i> Human Review Required
        </h3>
        <p>The Analyzer Agent flagged anomalies that require your approval before proceeding.</p>
      </div>

      <div className="anomaly-list">
        {anomalies.map((anomaly) => (
          <div key={anomaly.transaction_id} className="anomaly-card">
            <span className={`severity-badge severity-${anomaly.severity}`}>
              {anomaly.severity} Risk
            </span>
            <p>
              <strong>Txn {anomaly.transaction_id}:</strong> {anomaly.reason}
            </p>
            <div className="decision-group">
              <button
                className={`decision-btn approve ${
                  decisions[anomaly.transaction_id] === true ? 'selected' : ''
                }`}
                onClick={() => onDecision(anomaly.transaction_id, true)}
              >
                <i className="fa-solid fa-check"></i> Approve
              </button>
              <button
                className={`decision-btn reject ${
                  decisions[anomaly.transaction_id] === false ? 'selected' : ''
                }`}
                onClick={() => onDecision(anomaly.transaction_id, false)}
              >
                <i className="fa-solid fa-xmark"></i> Override (Reject)
              </button>
            </div>
          </div>
        ))}
      </div>

      <button className="btn btn-warning" onClick={onSubmit} disabled={!allDecided}>
        {allDecided
          ? 'Submit Decisions & Continue'
          : `Decide all ${anomalies.length} anomalies to continue`}
      </button>
    </div>
  );
}
