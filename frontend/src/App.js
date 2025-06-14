import React, { useState } from "react";

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

export default function App() {
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [build, setBuild] = useState(null);
  const [total, setTotal] = useState(null);
  const [issues, setIssues] = useState([]);
  const [error, setError] = useState("");

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex flex-col items-center p-6 text-gray-100">
      <h1 className="text-4xl font-extrabold mb-8 select-none text-indigo-400 drop-shadow-lg">
        🤖 AI PC Builder
      </h1>

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
        <p className="mt-6 text-red-500 font-medium max-w-3xl text-center">{error}</p>
      )}

      {summary && !loading && (
        <section className="mt-10 max-w-3xl bg-gray-800 rounded-xl shadow-lg p-6 space-y-6">
          <h2 className="text-2xl font-semibold text-indigo-400">🧾 Build Summary</h2>
          <pre className="whitespace-pre-wrap text-gray-300 leading-relaxed">{summary}</pre>

          {total !== null && (
            <p className="text-indigo-300 font-bold text-lg">
              💰 Total Cost: <span className="text-indigo-100">{formatPrice(total)}</span>
            </p>
          )}

          {issues.length > 0 && (
            <div>
              <h3 className="text-red-500 font-semibold mb-2">⚠️ Compatibility Issues</h3>
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
    </div>
  );
}
