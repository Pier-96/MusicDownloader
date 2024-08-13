import React, { useState } from "react";
import './App.css';

function App() {
  const [url, setUrl] = useState("");
  const [downloading, setDownloading] = useState(false);
  const [message, setMessage] = useState("");

  const handleDownload = async () => {
    if (!url) {
      setMessage("Por favor, ingresa una URL válida.");
      return;
    }

    setDownloading(true);
    setMessage("Descargando...");

    try {
      const response = await fetch("/api/download/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`Descarga completada: ${data.file}`);
      } else {
        setMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }

    setDownloading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Descargar MP3 de YouTube</h1>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Ingresa la URL del video de YouTube"
        />
        <button onClick={handleDownload} disabled={downloading}>
          {downloading ? "Descargando..." : "Descargar MP3"}
        </button>
        {message && <p>{message}</p>}
      </header>
    </div>
  );
}

export default App;