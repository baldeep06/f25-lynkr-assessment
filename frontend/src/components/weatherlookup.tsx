"use client";

import { useState } from "react";

export function WeatherLookup() {
  const [id, setId] = useState("");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    setError("");
    setData(null);
    try {
      const res = await fetch(`http://localhost:8000/weather/${id}`);
      if (!res.ok) throw new Error("Invalid ID or server error");
      const result = await res.json();
      setData(result);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    }
  };

  return (
    <div className="w-full max-w-md space-y-4">
      <input
        type="text"
        placeholder="Enter Weather ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
        className="w-full px-4 py-2 border rounded text-black"
      />
      <button
        onClick={handleFetch}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
      >
        Fetch Weather Data
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {data && (
        <div className="mt-4 p-4 border rounded bg-gray-100 dark:bg-gray-800 text-sm">
          <p><strong>Date:</strong> {data.date}</p>
          <p><strong>Location:</strong> {data.location}</p>
          <p><strong>Notes:</strong> {data.notes}</p>
          <p><strong>Temperature:</strong> {data.weather.temperature}°C</p>
          <p><strong>Condition:</strong> {data.weather.weather_descriptions?.join(", ")}</p>
          <p><strong>Humidity:</strong> {data.weather.humidity}%</p>
        </div>
      )}
    </div>
  );
}