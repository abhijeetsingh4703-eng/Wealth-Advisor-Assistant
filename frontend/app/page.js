'use client';

import { useState, useEffect, useRef } from 'react';
import Sidebar from '@/components/Sidebar';
import AgentStep from '@/components/AgentStep';
import HitlReview from '@/components/HitlReview';
import AgentLog from '@/components/AgentLog';
import FinalReport from '@/components/FinalReport';

const API_BASE = 'http://localhost:8000/api';

const INITIAL_STEPS = {
  orchestrator: { status: 'pending', text: 'Waiting...' },
  data: { status: 'pending', text: 'Pending' },
  analyzer: { status: 'pending', text: 'Pending' },
  report: { status: 'pending', text: 'Pending' },
};

function getTime() {
  return new Date().toLocaleTimeString([], { hour12: false });
}

export default function Home() {
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [workflowStatus, setWorkflowStatus] = useState('idle');
  const [steps, setSteps] = useState(INITIAL_STEPS);
  const [sessionId, setSessionId] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [decisions, setDecisions] = useState({});
  const [report, setReport] = useState(null);
  const [logs, setLogs] = useState([]);
  const logRef = useRef(null);


  useEffect(() => {
    setLogs([{ type: 'system', time: getTime(), message: 'System initialized. Select a client to begin.' }]);
    fetch(`${API_BASE}/clients`)
      .then((r) => r.json())
      .then(setClients)
      .catch(() => addLog('Failed to connect to API. Is the backend running?', 'system'));
  }, []);


  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [logs]);

  function addLog(message, type = 'agent') {
    setLogs((prev) => [...prev, { type, time: getTime(), message }]);
  }

  function setStep(name, status, text) {
    setSteps((prev) => ({ ...prev, [name]: { status, text } }));
  }

  function selectClient(client) {
    setSelectedClient(client);
    resetDashboard();
    addLog(`Client selected: ${client.name}`, 'system');
  }

  function resetDashboard() {
    setWorkflowStatus('idle');
    setSteps(INITIAL_STEPS);
    setSessionId(null);
    setAnomalies([]);
    setDecisions({});
    setReport(null);
    setLogs([{ type: 'system', time: getTime(), message: 'Ready. Click "Run Agent Analysis" to begin.' }]);
  }

  async function startAnalysis() {
    if (!selectedClient) return;

    setWorkflowStatus('running');
    setReport(null);
    setAnomalies([]);
    setDecisions({});

    addLog('Initializing Orchestrator Agent...', 'system');
    setStep('orchestrator', 'active', 'Routing tasks...');
    setStep('data', 'pending', 'Pending');
    setStep('analyzer', 'pending', 'Pending');
    setStep('report', 'pending', 'Pending');

    try {
      await delay(600);
      addLog('[Orchestrator] Starting orchestration workflow');
      setStep('data', 'active', 'Fetching data...');

      await delay(700);
      addLog('[DataFetcher] Fetching profile and transactions from CRM');

      const res = await fetch(`${API_BASE}/analyze/${selectedClient.client_id}`, { method: 'POST' });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Server error');

      setSessionId(data.session_id);

      addLog('[DataFetcher] Successfully fetched profile and transactions');
      setStep('data', 'completed', 'Completed ✓');

      await delay(400);
      setStep('analyzer', 'active', 'Detecting anomalies...');
      addLog('[Analyzer] Running anomaly detection algorithms');
      await delay(600);

      if (data.status === 'awaiting_review') {
        addLog(`[Analyzer] Detected ${data.anomalies.length} anomaly(s) — HITL checkpoint reached`);
        addLog('[Orchestrator] Paused. Waiting for human review...', 'system');

        setStep('analyzer', 'completed', `Found ${data.anomalies.length} anomaly(s) ✓`);
        setStep('orchestrator', 'hitl', 'Paused — awaiting review');

        setAnomalies(data.anomalies);
        setWorkflowStatus('awaiting_review');
      } else if (data.status === 'completed') {
        await completeWorkflow(data.report);
      }
    } catch (err) {
      addLog(`Error: ${err.message}`, 'system');
      setWorkflowStatus('error');
      setStep('orchestrator', 'pending', 'Error ✗');
    }
  }

  function handleDecision(txnId, approved) {
    setDecisions((prev) => ({ ...prev, [txnId]: approved }));
  }

  async function submitHitlDecisions() {
    const payload = Object.entries(decisions).map(([txnId, approved]) => ({
      session_id: sessionId,
      transaction_id: txnId,
      is_approved: approved,
    }));

    addLog('Submitting HITL decisions to Orchestrator...', 'system');
    setWorkflowStatus('generating');
    setStep('orchestrator', 'active', 'Resuming workflow...');
    setStep('report', 'active', 'Generating report...');

    try {
      const res = await fetch(`${API_BASE}/hitl/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Server error');

      addLog('[Orchestrator] Decisions received. Resuming workflow.');
      addLog('[ReportGenerator] Compiling final advisory report...');

      await delay(500);
      await completeWorkflow(data.report);
    } catch (err) {
      addLog(`Error submitting decisions: ${err.message}`, 'system');
      setWorkflowStatus('error');
    }
  }

  async function completeWorkflow(finalReport) {
    await delay(300);
    setStep('orchestrator', 'completed', 'Completed ✓');
    setStep('data', 'completed', 'Completed ✓');
    setStep('analyzer', 'completed', 'Completed ✓');
    setStep('report', 'completed', 'Completed ✓');

    addLog('[ReportGenerator] Report generation complete.');
    addLog('[Orchestrator] Workflow finished. Saved to long-term memory.', 'system');

    setReport(finalReport);
    setWorkflowStatus('completed');
  }

  function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  const isRunning = ['running', 'generating'].includes(workflowStatus);

  return (
    <div className="app-container">
      <Sidebar
        clients={clients}
        selectedClientId={selectedClient?.client_id}
        onSelectClient={selectClient}
      />

      <main className="main-content">
        <header className="top-bar">
          <h1>{selectedClient ? selectedClient.name : 'Select a Client'}</h1>
          <div className="user-profile">
            <img
              src="https://ui-avatars.com/api/?name=Advisor&background=0D8ABC&color=fff"
              alt="Advisor"
              className="avatar"
            />
          </div>
        </header>

        <div className="dashboard-grid">
          <section className="panel action-panel">
            <div className="panel-header">
              <h2><i className="fa-solid fa-robot"></i> Agent Workflow</h2>
            </div>
            <div className="panel-body">

              {!selectedClient && (
                <div className="state-message">
                  <i className="fa-solid fa-arrow-left"></i>
                  <p>Select a client from the sidebar to begin analysis.</p>
                </div>
              )}
              {selectedClient && workflowStatus === 'idle' && (
                <div className="state-message">
                  <button className="btn btn-primary btn-large" onClick={startAnalysis}>
                    <i className="fa-solid fa-robot"></i> Run Agent Analysis
                  </button>
                </div>
              )}
              {selectedClient && workflowStatus !== 'idle' && (
                <div className="workflow-visualizer">
                  <AgentStep
                    icon="fa-sitemap"
                    title="Orchestrator"
                    status={steps.orchestrator.status}
                    statusText={steps.orchestrator.text}
                    showSpinner={steps.orchestrator.status === 'active'}
                  />
                  <div className="connector"></div>
                  <AgentStep
                    icon="fa-database"
                    title="Data Fetcher"
                    status={steps.data.status}
                    statusText={steps.data.text}
                    showSpinner={steps.data.status === 'active'}
                  />
                  <div className="connector"></div>
                  <AgentStep
                    icon="fa-chart-line"
                    title="Analyzer"
                    status={steps.analyzer.status}
                    statusText={steps.analyzer.text}
                    showSpinner={steps.analyzer.status === 'active'}
                  />
                  <div className="connector"></div>
                  <AgentStep
                    icon="fa-file-invoice"
                    title="Report Generator"
                    status={steps.report.status}
                    statusText={steps.report.text}
                    showSpinner={steps.report.status === 'active'}
                  />
                  {workflowStatus === 'awaiting_review' && (
                    <HitlReview
                      anomalies={anomalies}
                      decisions={decisions}
                      onDecision={handleDecision}
                      onSubmit={submitHitlDecisions}
                    />
                  )}
                  {workflowStatus === 'completed' && (
                    <div style={{ marginTop: 20, textAlign: 'center' }}>
                      <button className="btn btn-primary" onClick={startAnalysis}>
                        <i className="fa-solid fa-rotate-right"></i> Run Again
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>
          <div className="right-column">
            {report && <FinalReport report={report} />}
            <AgentLog logs={logs} isActive={isRunning} />
          </div>
        </div>
      </main>
    </div>
  );
}
