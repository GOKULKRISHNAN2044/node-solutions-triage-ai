import { useState } from "react";
import PriorityBadge from "./PriorityBadge";
import CategoryTag from "./CategoryTag";

const ROUTE_ICONS = {
  "Sales Team":     "💼",
  "Client Success": "🤝",
  "Finance":        "💰",
  "Engineering":    "⚙️",
};

const TriageCard = ({ result, loading, error }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result.data.draft_response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  /* ── Loading State ─────────────────────────────── */
  if (loading) {
    return (
      <div className="triage-card triage-card--loading">
        <div className="loading-pulse">
          <div className="loading-orb" />
          <p>AI is analyzing your request…</p>
          <span>Powered by Gemini</span>
        </div>
      </div>
    );
  }

  /* ── Error State ───────────────────────────────── */
  if (error) {
    return (
      <div className="triage-card triage-card--error">
        <div className="error-content">
          <span className="error-icon">⚠️</span>
          <h3>Something went wrong</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  /* ── Empty State ───────────────────────────────── */
  if (!result) {
    return (
      <div className="triage-card triage-card--empty">
        <div className="empty-content">
          <span className="empty-icon">🤖</span>
          <h3>Ready to Triage</h3>
          <p>Submit a request to see the AI analysis here</p>
        </div>
      </div>
    );
  }

  const data = result.data;
  const routeIcon = ROUTE_ICONS[data.route] || "📌";

  /* ── Result State ──────────────────────────────── */
  return (
    <div className="triage-card triage-card--result">

      {/* Header */}
      <div className="triage-card__header">
        <h3 className="triage-card__title">Triage Result</h3>
        <div className="triage-card__badges">
          <PriorityBadge priority={data.priority} />
          <CategoryTag category={data.category} />
        </div>
      </div>

      {/* Summary */}
      <div className="triage-field">
        <label className="triage-field__label">📝 Summary</label>
        <p className="triage-field__value">{data.summary}</p>
      </div>

      {/* Priority Reason */}
      <div className="triage-field">
        <label className="triage-field__label">⚡ Priority Reason</label>
        <p className="triage-field__value triage-field__value--muted">{data.priority_reason}</p>
      </div>

      {/* Route */}
      <div className="triage-field">
        <label className="triage-field__label">📍 Routed To</label>
        <div className="route-chip">
          <span>{routeIcon}</span>
          <span>{data.route}</span>
        </div>
      </div>

      {/* Draft Response */}
      <div className="triage-field">
        <div className="triage-field__row">
          <label className="triage-field__label">✉️ Draft Response</label>
          <button className="btn-copy" onClick={handleCopy}>
            {copied ? "✅ Copied!" : "📋 Copy"}
          </button>
        </div>
        <div className="draft-box">
          <p>{data.draft_response}</p>
        </div>
      </div>

    </div>
  );
};

export default TriageCard;
