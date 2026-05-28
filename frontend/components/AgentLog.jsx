'use client';

export default function AgentLog({ logs, isActive }) {
  return (
    <section className="panel log-panel">
      <div className="panel-header">
        <h2>
          <i className="fa-solid fa-terminal"></i> Agent Thought Log
        </h2>
        <div className={`pulsing-dot ${isActive ? 'active' : ''}`}></div>
      </div>
      <div className="panel-body">
        <div className="log-container">
          {logs.map((log, idx) => (
            <div key={idx} className={`log-entry ${log.type}`}>
              <span className="log-timestamp">[{log.time}]</span>
              {log.message}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
