import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Badge({ action }) {
  const isFreeze = action === "FREEZE";
  return (
    <span className={`badge ${isFreeze ? "badge-freeze" : "badge-unfreeze"}`}>
      {isFreeze ? "FREEZE" : "UNFREEZE"}
    </span>
  );
}

function Field({ label, value }) {
  if (value === null || value === undefined || value === "") return null;
  return (
    <div className="field">
      <span className="field-label">{label}</span>
      <span className="field-value">{String(value)}</span>
    </div>
  );
}

function ConfidenceBar({ value }) {
  const pct = Math.round((value || 0) * 100);
  const color = pct >= 90 ? "#22c55e" : pct >= 70 ? "#f59e0b" : "#ef4444";
  return (
    <div className="confidence">
      <span className="field-label">AI Confidence</span>
      <div className="confidence-row">
        <div className="confidence-track">
          <div className="confidence-fill" style={{ width: `${pct}%`, background: color }} />
        </div>
        <span className="confidence-pct" style={{ color }}>{pct}%</span>
      </div>
    </div>
  );
}

function Result({ data }) {
  return (
    <div className={`result-card ${data.action === "FREEZE" ? "card-freeze" : "card-unfreeze"}`}>
      <div className="result-header">
        <Badge action={data.action} />
        <span className="filename">{data.filename}</span>
      </div>

      <div className="section">
        <div className="section-title">Subject</div>
        <Field label="Full Name" value={data.subject?.full_name} />
        <Field label="Emirates ID" value={data.subject?.emirates_id} />
        <Field label="Passport" value={data.subject?.passport_number} />
        {data.subject?.other_ids?.map((id, i) => (
          <Field key={i} label="Other ID" value={id} />
        ))}
      </div>

      <div className="section">
        <div className="section-title">Court Details</div>
        <Field label="Court" value={data.court?.name} />
        <Field label="Emirate" value={data.court?.emirate} />
        <Field label="Case Reference" value={data.case_reference} />
        <Field label="Date Issued" value={data.issued_date} />
        <Field label="Recipient" value={data.recipient} />
      </div>

      <div className="section">
        <div className="section-title">Instructions</div>
        <p className="instructions">{data.instructions}</p>
        <Field label="Effective Immediately" value={data.effective_immediately ? "Yes" : "No"} />
      </div>

      {data.raw_notes && (
        <div className="section">
          <div className="section-title">Notes</div>
          <p className="notes">{data.raw_notes}</p>
        </div>
      )}

      <ConfidenceBar value={data.confidence} />

      <details className="raw-json">
        <summary>View Raw JSON</summary>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </details>
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [fileUrl, setFileUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [showPdf, setShowPdf] = useState(false);
  const inputRef = useRef();

  useEffect(() => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    setFileUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function handleFile(f) {
    if (!f) return;
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      return;
    }
    setFile(f);
    setResult(null);
    setError(null);
    setShowPdf(false);
  }

  async function handleSubmit() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/api/extract`, { method: "POST", body: form });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server error ${res.status}`);
      }
      setResult(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo-mark">UAE</div>
        <div>
          <div className="header-title">Court Order OCR</div>
          <div className="header-sub">AI-Powered Asset Freeze / Unfreeze Extraction</div>
        </div>
      </header>

      <main className="main">
        <div
          className={`upload-zone ${dragging ? "dragging" : ""} ${file ? "has-file" : ""}`}
          onClick={() => !loading && inputRef.current.click()}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            handleFile(e.dataTransfer.files[0]);
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            style={{ display: "none" }}
            onChange={(e) => handleFile(e.target.files[0])}
          />
          <div className="upload-icon">{file ? "📄" : "⬆️"}</div>
          <div className="upload-text">
            {file ? file.name : "Tap to upload or drag & drop"}
          </div>
          <div className="upload-hint">
            {file ? `${(file.size / 1024).toFixed(1)} KB` : "PDF court orders only"}
          </div>
        </div>

        {error && <div className="error-box">{error}</div>}

        <button
          className="btn-extract"
          onClick={handleSubmit}
          disabled={!file || loading}
        >
          {loading ? (
            <>
              <span className="spinner" />
              Extracting...
            </>
          ) : (
            "Extract Document"
          )}
        </button>

        {result && <Result data={result} />}

        {result && fileUrl && (
          <div className="pdf-viewer-section">
            <button
              className="btn-toggle-pdf"
              onClick={() => setShowPdf((v) => !v)}
            >
              {showPdf ? "Hide Original PDF" : "View Original PDF"}
            </button>
            {showPdf && (
              <iframe
                className="pdf-iframe"
                src={fileUrl}
                title="Original PDF"
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}
