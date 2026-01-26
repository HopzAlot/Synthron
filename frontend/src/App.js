import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* ---------------------- CONFIG ---------------------- */
const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
/* --------------------------------------------------- */

const LoadingSpinner = () => (
  <div className="flex justify-center my-8">
    <svg
      className="animate-spin h-12 w-12 text-indigo-400"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>
  </div>
);

function formatPrice(price) {
  return `$${price?.toFixed(2) || "0.00"}`;
}

/* ====================== AUTH FORM ====================== */
function AuthForm({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch(
        `${BACKEND_URL}/api/${isRegister ? "register" : "login"}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Request failed");
      } else {
        if (!isRegister) {
          localStorage.setItem("access", data.access);
          localStorage.setItem("refresh", data.refresh);
          onLogin(data.access);
        } else {
          setIsRegister(false);
          setError("Registration successful. Please log in.");
        }
      }
    } catch {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 p-8 rounded-lg w-full max-w-md">
      <h2 className="text-2xl text-indigo-400 mb-4 text-center">
        {isRegister ? "Register" : "Login"}
      </h2>
      <form onSubmit={submit} className="space-y-4">
        <input
          className="w-full p-3 bg-gray-900 border border-gray-700 rounded"
          placeholder="Username"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />
        <input
          type="password"
          className="w-full p-3 bg-gray-900 border border-gray-700 rounded"
          placeholder="Password"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button
          disabled={loading}
          className="w-full bg-indigo-600 py-3 rounded font-semibold"
        >
          {loading ? "Please wait..." : isRegister ? "Register" : "Login"}
        </button>
      </form>
      <p className="text-center mt-4 text-gray-400">
        {isRegister ? "Have an account?" : "No account?"}{" "}
        <button
          onClick={() => setIsRegister(!isRegister)}
          className="text-indigo-400"
        >
          {isRegister ? "Login" : "Register"}
        </button>
      </p>
    </div>
  );
}

/* ====================== MAIN APP ====================== */
export default function App() {
  const [accessToken, setAccessToken] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [page, setPage] = useState("builder");

  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [build, setBuild] = useState(null);
  const [total, setTotal] = useState(null);
  const [issues, setIssues] = useState([]);
  const [history, setHistory] = useState([]);

  /* ---------- Restore session ---------- */
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) setAccessToken(token);
    setAuthLoading(false);
  }, []);

  /* ---------- Logout ---------- */
  const logout = () => {
    localStorage.clear();
    setAccessToken(null);
  };

  /* ---------- Generate Build ---------- */
  const generate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSummary("");
    setBuild(null);
    setIssues([]);

    try {
      const res = await fetch(`${BACKEND_URL}/api/configure/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error);
      }

      setSummary(data.summary);
      setBuild(data.build);
      setIssues(data.issues || []);
      setTotal(data.total);
    } catch (e) {
      alert(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  };

  /* ---------- Fetch History ---------- */
  const fetchHistory = async () => {
    const res = await fetch(`${BACKEND_URL}/api/history/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (res.ok) {
      setHistory(await res.json());
    }
  };

  useEffect(() => {
    if (page === "history" && accessToken) fetchHistory();
  }, [page, accessToken]);

  /* ---------- AUTH LOADING ---------- */
  if (authLoading) return <LoadingSpinner />;

  if (!accessToken) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <AuthForm onLogin={setAccessToken} />
      </div>
    );
  }

  /* ---------- MAIN UI ---------- */
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <div className="flex justify-between max-w-3xl mx-auto mb-6">
        <h1 className="text-3xl text-indigo-400 font-bold">Synthron</h1>
        <button onClick={logout} className="bg-red-600 px-4 py-2 rounded">
          Logout
        </button>
      </div>

      <div className="max-w-3xl mx-auto mb-4 flex gap-4">
        <button
          className={`flex-1 py-2 rounded ${
            page === "builder" ? "bg-indigo-600" : "bg-gray-700"
          }`}
          onClick={() => setPage("builder")}
        >
          Generator
        </button>
        <button
          className={`flex-1 py-2 rounded ${
            page === "history" ? "bg-indigo-600" : "bg-gray-700"
          }`}
          onClick={() => setPage("history")}
        >
          History
        </button>
      </div>

      {page === "builder" && (
        <form
          onSubmit={generate}
          className="max-w-3xl mx-auto bg-gray-800 p-6 rounded"
        >
          <textarea
            className="w-full p-4 bg-gray-900 rounded mb-4"
            rows={4}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Build me a gaming PC for $1500"
          />
          <button className="w-full bg-indigo-600 py-3 rounded">
            Generate
          </button>

          {loading && <LoadingSpinner />}

          {summary && (
            <div className="mt-6 prose prose-invert">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {summary}
              </ReactMarkdown>
            </div>
          )}
        </form>
      )}

      {page === "history" && (
        <div className="max-w-3xl mx-auto bg-gray-800 p-6 rounded">
          {history.length === 0 ? (
            <p>No history</p>
          ) : (
            history.map((h) => (
              <div key={h.id} className="mb-4">
                <p className="text-indigo-300">
                  {new Date(h.created_at).toLocaleString()}
                </p>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {h.summary}
                </ReactMarkdown>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
