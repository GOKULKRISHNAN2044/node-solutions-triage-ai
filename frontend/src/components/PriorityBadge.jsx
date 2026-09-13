const PRIORITY_CONFIG = {
  Urgent: { color: "#ef4444", bg: "rgba(239,68,68,0.15)", icon: "🔴", label: "Urgent" },
  High:   { color: "#f97316", bg: "rgba(249,115,22,0.15)", icon: "🟠", label: "High"   },
  Medium: { color: "#eab308", bg: "rgba(234,179,8,0.15)",  icon: "🟡", label: "Medium" },
  Low:    { color: "#22c55e", bg: "rgba(34,197,94,0.15)",  icon: "🟢", label: "Low"    },
};

const PriorityBadge = ({ priority }) => {
  const config = PRIORITY_CONFIG[priority] || PRIORITY_CONFIG.Low;
  return (
    <span
      className="priority-badge"
      style={{ color: config.color, background: config.bg, border: `1px solid ${config.color}40` }}
    >
      {config.icon} {config.label}
    </span>
  );
};

export default PriorityBadge;
