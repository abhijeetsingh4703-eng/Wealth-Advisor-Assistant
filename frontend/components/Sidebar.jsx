'use client';

export default function Sidebar({ clients, selectedClientId, onSelectClient }) {
  return (
    <aside className="sidebar">
      <div className="logo">
        <i className="fa-solid fa-gem"></i>
        <span>Aegis Wealth</span>
      </div>
      <div className="nav-section">
        <h3>Clients</h3>
        <ul className="client-list">
          {clients.length === 0 && (
            <li style={{ padding: '0 24px', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
              Loading clients...
            </li>
          )}
          {clients.map((client) => (
            <li
              key={client.client_id}
              className={selectedClientId === client.client_id ? 'active' : ''}
              onClick={() => onSelectClient(client)}
            >
              {client.name}
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}
