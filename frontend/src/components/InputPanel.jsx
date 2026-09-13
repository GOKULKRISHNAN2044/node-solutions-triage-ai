import { useState } from "react";

const MAX_CHARS = 2000;

const InputPanel = ({ onSubmit, loading }) => {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim().length >= 10 && !loading) onSubmit(text.trim());
  };

  const remaining = MAX_CHARS - text.length;
  const isValid = text.trim().length >= 10;

  return (
    <form className="input-panel" onSubmit={handleSubmit}>
      <div className="input-panel__header">
        <h2 className="input-panel__title">
          <span className="input-panel__icon">📨</span>
          Submit a Request
        </h2>
        <p className="input-panel__subtitle">
          Paste or type any incoming business request below
        </p>
      </div>

      <div className="input-panel__field">
        <textarea
          className="input-panel__textarea"
          value={text}
          onChange={(e) => setText(e.target.value.slice(0, MAX_CHARS))}
          placeholder="e.g. The client portal has been unavailable since this morning and our staff cannot access active customer records. Please help as soon as possible."
          rows={7}
          disabled={loading}
        />
        <div className="input-panel__meta">
          <span className={`input-panel__counter ${remaining < 100 ? "warn" : ""}`}>
            {remaining} characters remaining
          </span>
          {!isValid && text.length > 0 && (
            <span className="input-panel__hint">Minimum 10 characters</span>
          )}
        </div>
      </div>

      <button
        type="submit"
        className={`btn-primary ${loading ? "btn-loading" : ""}`}
        disabled={!isValid || loading}
      >
        {loading ? (
          <>
            <span className="spinner" /> Analyzing with AI…
          </>
        ) : (
          <>⚡ Analyze Request</>
        )}
      </button>
    </form>
  );
};

export default InputPanel;
