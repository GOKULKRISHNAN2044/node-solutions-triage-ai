const CATEGORY_CONFIG = {
  Sales:     { icon: "💼", color: "#6366f1" },
  Support:   { icon: "🛟", color: "#0ea5e9" },
  Billing:   { icon: "💳", color: "#a855f7" },
  Technical: { icon: "⚙️", color: "#14b8a6" },
  Other:     { icon: "📋", color: "#94a3b8" },
};

const CategoryTag = ({ category }) => {
  const config = CATEGORY_CONFIG[category] || CATEGORY_CONFIG.Other;
  return (
    <span
      className="category-tag"
      style={{ color: config.color, background: `${config.color}18`, border: `1px solid ${config.color}40` }}
    >
      {config.icon} {category}
    </span>
  );
};

export default CategoryTag;
