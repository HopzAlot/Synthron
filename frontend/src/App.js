import React, { useState, useEffect } from "react";

const LoadingSpinner = () => (
  <div className="flex justify-center my-8">
    <svg
      className="animate-spin h-12 w-12 text-indigo-400"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      role="img"
      aria-label="Loading"
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

function ComponentCard({ title, component }) {
  if (!component || Object.keys(component).length === 0) {
    return (
      <div className="bg-gray-800 p-4 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-indigo-300">{title}</h3>
        <p className="text-gray-400 mt-2">No data available.</p>
      </div>
    );
  }

  if (Array.isArray(component)) {
    return (
      <div className="bg-gray-800 p-4 rounded-lg shadow-md space-y-4">
        <h3 className="text-lg font-semibold text-indigo-300">{title}</h3>
        {component.map((item, idx) => (
          <div
            key={idx}
            className="border border-indigo-600 rounded-md p-3 bg-gray-900"
          >
            <h4 className="text-indigo-400 font-semibold">
              {item.name || "Unnamed"}
            </h4>
            <ul className="text-gray-300 list-disc list-inside text-sm mt-1">
              {item.socket && <li>Socket: {item.socket}</li>}
              {item.ram_type && <li>RAM Type: {item.ram_type}</li>}
              {item.power_draw && <li>Power Draw: {item.power_draw}W</li>}
              {item.performance && <li>Performance: {item.performance}</li>}
              {item.vendor && <li>Vendor: {item.vendor}</li>}
              {typeof item.price === "number" && (
                <li>Price: {formatPrice(item.price)}</li>
              )}
              {item.url && (
                <li>
                  Link:{" "}
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-400 hover:underline"
                  >
                    View Product
                  </a>
                </li>
              )}
            </ul>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-indigo-300">{title}</h3>
      <ul className="text-gray-300 list-disc list-inside text-sm mt-2">
        {component.name && <li>Name: {component.name}</li>}
        {component.socket && <li>Socket: {component.socket}</li>}
        {component.ram_type && <li>RAM Type: {component.ram_type}</li>}
        {component.power_draw && <li>Power Draw: {component.power_draw}W</li>}
        {component.performance && <li>Performance: {component.performance}</li>}
        {component.vendor && <li>Vendor: {component.vendor}</li>}
        {typeof component.price === "number" && (
          <li>Price: {formatPrice(component.price)}</li>
        )}
        {component.url && (
          <li>
            Link:{" "}
            <a
              href={component.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-400 hover:underline"
            >
              View Product
            </a>
          </li>
        )}
      </ul>
    </div>
  );
}

function AuthForm({ onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const toggleMode = () => {
    setError("");
    setFormData({ username: "", password: "" });
    setIsRegister(!isRegister);
  };

  const handleChange = (e) => {
    setFormData((f) => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Username and Password are required");
      return;
    }
    setLoading(true);

    const url = isRegister
      ? "http://localhost:8000/api/register/"
      : "http://localhost:8000/api/login/";

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Something went wrong");
      } else {
        if (!isRegister) {
          onLoginSuccess();
        } else {
          setIsRegister(false);
          setError("Registration successful! Please login.");
        }
      }
    } catch {
      setError("Network error, please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md w-full bg-gray-800 p-8 rounded-lg shadow-lg text-gray-100">
      <h2 className="text-2xl font-semibold mb-6 text-indigo-400 text-center">
        {isRegister ? "Register" : "Login"}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          disabled={loading}
          className="w-full p-3 rounded bg-gray-900 border border-gray-700 focus:border-indigo-500 outline-none"
          autoComplete="username"
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          disabled={loading}
          className="w-full p-3 rounded bg-gray-900 border border-gray-700 focus:border-indigo-500 outline-none"
          autoComplete={isRegister ? "new-password" : "current-password"}
          required
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 py-3 rounded font-semibold transition disabled:opacity-50"
        >
          {loading ? (isRegister ? "Registering..." : "Logging in...") : isRegister ? "Register" : "Login"}
        </button>
      </form>
      <p className="mt-4 text-center text-gray-400">
        {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
        <button
          onClick={toggleMode}
          className="text-indigo-400 hover:underline font-semibold"
          disabled={loading}
        >
          {isRegister ? "Login" : "Register"}
        </button>
      </p>
    </div>
  );
}

export default function App() {
  // Auth states
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(true);

  // Generate build states
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [build, setBuild] = useState(null);
  const [total, setTotal] = useState(null);
  const [issues, setIssues] = useState([]);
  const [error, setError] = useState("");

  // History states
  const [activePage, setActivePage] = useState("builder"); // or 'history'
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Check persistent login on mount
  useEffect(() => {
    async function checkAuth() {
      try {
        setAuthLoading(true);
        const res = await fetch("http://localhost:8000/api/refresh/", {
          method: "POST",
          credentials: "include",
        });
        setIsAuthenticated(res.ok);
      } catch {
        setIsAuthenticated(false);
      } finally {
        setAuthLoading(false);
      }
    }
    checkAuth();
  }, []);

  // Fetch history only if authorized and activePage === 'history'
  useEffect(() => {
    if (activePage === "history" && isAuthenticated) {
      fetchHistory();
    }
  }, [activePage, isAuthenticated]);

  // Fetch build history
  async function fetchHistory() {
    setLoadingHistory(true);
    try {
      const res = await fetch("http://localhost:8000/api/history/", {
        method: "GET",
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      } else {
        setHistory([]);
      }
    } catch {
      setHistory([]);
    } finally {
      setLoadingHistory(false);
    }
  }

  // Logout handler
  const handleLogout = async () => {
    try {
      setAuthLoading(true);
      const res = await fetch("http://localhost:8000/api/logout/", {
        method: "POST",
        credentials: "include",
      });
      if (res.ok) {
        setIsAuthenticated(false);
        setUserInput("");
        setSummary("");
        setBuild(null);
        setTotal(null);
        setIssues([]);
        setError("");
        setActivePage("builder");
        setHistory([]);
      } else {
        setError("Logout failed");
      }
    } catch {
      setError("Logout failed");
    } finally {
      setAuthLoading(false);
    }
  };

  // Login success callback
  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    setError("");
  };

  // Generate build submit handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setLoading(true);
    setError("");
    setSummary("");
    setBuild(null);
    setTotal(null);
    setIssues([]);

    try {
      const response = await fetch("http://localhost:8000/api/configure/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userInput }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Unknown error occurred");
      } else {
        setSummary(data.summary || "");
        setBuild(data.build || null);

        if (typeof data.total === "number") {
          setTotal(data.total);
        } else if (data.build) {
          const prices = Object.values(data.build).flatMap((comp) =>
            Array.isArray(comp) ? comp.map((i) => i.price || 0) : [comp.price || 0]
          );
          const sum = prices.reduce((acc, val) => acc + val, 0);
          setTotal(sum);
        } else {
          setTotal(null);
        }

        setIssues(data.issues || []);
      }
    } catch (err) {
      setError("Failed to fetch suggestion. Please try again.");
      console.error("API error:", err);
    }

    setLoading(false);
  };

  // Loading spinner while checking auth
  if (authLoading) return <LoadingSpinner />;

  // Show login/register form if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
        <AuthForm onLoginSuccess={handleLoginSuccess} />
      </div>
    );
  }

  // Main UI when logged in
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex flex-col items-center p-6 text-gray-100">
      <div className="w-full max-w-3xl flex justify-between items-center mb-6">
        <h1 className="text-4xl font-extrabold select-none text-indigo-400 drop-shadow-lg">
          🤖 Synthron
        </h1>
        <button
          onClick={handleLogout}
          disabled={authLoading}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded font-semibold transition disabled:opacity-50"
        >
          Logout
        </button>
      </div>

      {/* Tabs */}
      <div className="w-full max-w-3xl flex gap-4 mb-6">
        <button
          onClick={() => setActivePage("builder")}
          className={`flex-1 py-2 rounded ${
            activePage === "builder" ? "bg-indigo-600" : "bg-gray-700"
          } font-semibold`}
        >
          Generator
        </button>
        <button
          onClick={() => setActivePage("history")}
          className={`flex-1 py-2 rounded ${
            activePage === "history" ? "bg-indigo-600" : "bg-gray-700"
          } font-semibold`}
        >
          History
        </button>
      </div>

      {/* Content */}
      {activePage === "builder" && (
        <>
          {/* Generate Build Form */}
          <form
            onSubmit={handleSubmit}
            className="w-full max-w-3xl bg-gray-800 rounded-xl shadow-lg p-8 flex flex-col gap-4"
          >
            <textarea
              className="resize-none p-4 rounded-lg border border-gray-700 bg-gray-900 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-600 transition outline-none text-lg text-gray-100"
              rows={5}
              placeholder="E.g., Build me a gaming PC for $1500 with Intel CPU, US region"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              disabled={loading}
              spellCheck={false}
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-indigo-600 text-white font-semibold py-3 rounded-lg shadow-md hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Building your PC..." : "Generate Build"}
            </button>
          </form>

          {loading && <LoadingSpinner />}

          {error && (
            <p className="mt-6 text-red-500 font-medium max-w-3xl text-center">
              {error}
            </p>
          )}

          {summary && !loading && (
            <section className="mt-10 max-w-3xl bg-gray-800 rounded-xl shadow-lg p-6 space-y-6">
              <h2 className="text-2xl font-semibold text-indigo-400">
                🧾 Build Summary
              </h2>
              <pre className="whitespace-pre-wrap text-gray-300 leading-relaxed">
                {summary}
              </pre>

              {total !== null && (
                <p className="text-indigo-300 font-bold text-lg">
                  💰 Total Cost:{" "}
                  <span className="text-indigo-100">{formatPrice(total)}</span>
                </p>
              )}

              {issues.length > 0 && (
                <div>
                  <h3 className="text-red-500 font-semibold mb-2">
                    ⚠️ Compatibility Issues
                  </h3>
                  <ul className="list-disc list-inside text-red-400 space-y-1">
                    {issues.map((issue, idx) => (
                      <li key={idx}>{issue}</li>
                    ))}
                  </ul>
                </div>
              )}

              {build && (
                <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-6">
                  {Object.entries(build).map(([componentName, componentData]) => (
                    <ComponentCard
                      key={componentName}
                      title={componentName}
                      component={componentData}
                    />
                  ))}
                </div>
              )}
            </section>
          )}
        </>
      )}

      {activePage === "history" && (
        <section className="w-full max-w-3xl bg-gray-800 rounded-xl shadow-lg p-6 space-y-4 min-h-[300px]">
          <h2 className="text-2xl font-semibold text-indigo-400 mb-4">
            📜 Build History
          </h2>

          {loadingHistory ? (
            <LoadingSpinner />
          ) : history.length === 0 ? (
            <p className="text-gray-400 text-center">No history found.</p>
          ) : (
            <ul className="space-y-4 max-h-[400px] overflow-y-auto">
              {history.map((entry) => (
                <li
                  key={entry.id}
                  className="border border-indigo-600 rounded-lg p-4 bg-gray-900"
                >
                  <p className="text-indigo-300 font-semibold">
                    {new Date(entry.created_at).toLocaleString()}
                  </p>
                  <pre className="whitespace-pre-wrap text-gray-300 mt-2">
                    {entry.summary || "No summary available."}
                  </pre>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  );
}