'use client';

export default function AgentStep({ icon, title, status, statusText, showSpinner }) {
  return (
    <div className={`agent-step ${status}`}>
      <div className="step-icon">
        <i className={`fa-solid ${icon}`}></i>
      </div>
      <div className="step-info">
        <h4>{title}</h4>
        <p className="step-status">{statusText}</p>
      </div>
      <div className="step-spinner">
        {showSpinner && <i className="fa-solid fa-circle-notch fa-spin"></i>}
      </div>
    </div>
  );
}
