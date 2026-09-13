import PriorityBadge from "./PriorityBadge";
import CategoryTag from "./CategoryTag";

const formatTime = (isoString) => {
  if (!isoString) return "";
  const d = new Date(isoString);
  return d.toLocaleString("en-IN", {
    day: "2-digit", month: "short",
    hour: "2-digit", minute: "2-digit", hour12: true,
  });
};

const HistoryPanel = ({ history, onSelect, selectedId }) => {
  if (!history || history.length === 0) {
    return (
      <div className="history-panel">
        <div className="history-panel__header">
          <h3>📂 History</h3>
          <span className="history-panel__count">0 requests</span>
        </div>
        <div className="history-panel__empty">
          <span>No requests yet</span>
        </div>
      </div>
    );
  }

  return (
    <div className="history-panel">
      <div className="history-panel__header">
        <h3>📂 History</h3>
        <span className="history-panel__count">{history.length} requests</span>
      </div>
      <ul className="history-panel__list">
        {history.map((item) => (
          <li
            key={item.id}
            className={`history-item ${selectedId === item.id ? "history-item--active" : ""}`}
            onClick={() => onSelect(item)}
          >
            <div className="history-item__top">
              <PriorityBadge priority={item.priority} />
              <CategoryTag category={item.category} />
            </div>
            <p className="history-item__summary">{item.summary}</p>
            <span className="history-item__time">{formatTime(item.created_at)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPanel;
