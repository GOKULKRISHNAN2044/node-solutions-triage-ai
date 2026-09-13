import { useState, useEffect, useCallback } from "react";
import InputPanel from "../components/InputPanel";
import TriageCard from "../components/TriageCard";
import HistoryPanel from "../components/HistoryPanel";
import { triageRequest, getHistory } from "../services/api";

const Dashboard = () => {
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);
  const [history, setHistory]     = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  const fetchHistory = useCallback(async () => {
    try {
      const res = await getHistory();
      setHistory(res.data || []);
    } catch {
      // silent — history is non-critical
    }
  }, []);

  useEffect(() => { fetchHistory(); }, [fetchHistory]);

  const handleSubmit = async (text) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedId(null);
    try {
      const res = await triageRequest(text);
      setResult(res);
      setSelectedId(res.data?.id);
      await fetchHistory();
    } catch (err) {
      const msg = err?.response?.data?.message || err?.message || "Unexpected error. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectHistory = (item) => {
    setSelectedId(item.id);
    setError(null);
    // Wrap in APIResponse shape so TriageCard works consistently
    setResult({ data: item, message: "From history", status_code: 200 });
  };

  return (
    <div className="dashboard">

      {/* ── Sidebar ── */}
      <aside className="dashboard__sidebar">
        <HistoryPanel
          history={history}
          onSelect={handleSelectHistory}
          selectedId={selectedId}
        />
      </aside>

      {/* ── Main ── */}
      <main className="dashboard__main">

        {/* Header */}
        <header className="dashboard__header">
          <div className="dashboard__brand">
            <img
              src="/node-solutions-logo.svg"
              alt="Node Solutions"
              className="dashboard__logo"
            />
            <div className="dashboard__brand-divider" />
            <div>
              <div className="dashboard__brand-label">AI Request Triage</div>
              <div className="dashboard__brand-sub">Powered by Gemini 3.5 Flash Lite</div>
            </div>
          </div>
          <div className="dashboard__stats">
            <div className="stat-chip">
              <span className="stat-chip__value">{history.length}</span>
              <span className="stat-chip__label">Requests</span>
            </div>
          </div>
        </header>

        {/* Content */}
        <div className="dashboard__content">
          <section className="dashboard__input-section">
            <InputPanel onSubmit={handleSubmit} loading={loading} />
          </section>
          <section className="dashboard__result-section">
            <TriageCard result={result} loading={loading} error={error} />
          </section>
        </div>

      </main>
    </div>
  );
};

export default Dashboard;
