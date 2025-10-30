import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = "/api/traffic";

function App() {
  const [domain, setDomain] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState(null);

  // 1. Carica la configurazione del backend (per controllare la chiave API)
  useEffect(() => {
    axios.get("/api/config")
      .then(response => setConfig(response.data))
      .catch(err => console.error("Errore nel caricamento della configurazione:", err));
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!domain) return;

    setLoading(true);
    setError(null);
    setData(null);

    // Esempio di query Plausible per ottenere il traffico totale
    const plausibleQuery = {
      site_id: domain, // Il dominio è l'ID del sito in Plausible
      metrics: ["visitors", "pageviews", "bounce_rate", "visit_duration"],
      date_range: "30d",
      // Aggiungere altre query per i dati di dettaglio (es. fonti di traffico)
      // Per il momento, ci concentriamo sulla metrica principale
    };

    try {
      // Chiamata all'endpoint proxy Flask
      const response = await axios.post(`${API_BASE_URL}/proxy/plausible`, plausibleQuery, {
        headers: {
          // Plausible richiede il dominio nell'header Origin per la validazione
          'Origin': window.location.origin
        }
      });
      
      // La risposta è un array di risultati, ne prendiamo il primo per le metriche aggregate
      const result = response.data.results[0];
      setData({
        domain: domain,
        visitors: result.visitors.value,
        pageviews: result.pageviews.value,
        bounce_rate: result.bounce_rate.value,
        visit_duration: result.visit_duration.value,
        data_source: "Plausible Analytics (via Proxy Flask)",
        // Aggiungere qui altri dati come le serie temporali, se necessario
      });

    } catch (err) {
      console.error("Errore nell'analisi:", err);
      setError("Impossibile recuperare i dati. Verifica che il dominio sia corretto e che la chiave API Plausible sia configurata correttamente sul server.");
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      <header className="w-full max-w-4xl text-center py-6">
        <h1 className="text-4xl font-bold text-gray-800">Real Traffic Analyzer</h1>
        <p className="text-gray-600 mt-2">Analisi del traffico web tramite API Open Source (Plausible)</p>
      </header>

      <main className="w-full max-w-4xl bg-white shadow-lg rounded-xl p-8">
        <form onSubmit={handleAnalyze} className="flex flex-col sm:flex-row gap-4 mb-8">
          <input
            type="text"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            placeholder="Inserisci il dominio (es. example.com)"
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            required
          />
          <button
            type="submit"
            disabled={loading || !config?.plausible_api_key_configured}
            className="p-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition duration-150"
          >
            {loading ? "Analizzando..." : "Analizza Traffico"}
          </button>
        </form>

        {config && !config.plausible_api_key_configured && (
          <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4" role="alert">
            <p className="font-bold">Attenzione: Chiave API Plausible non configurata!</p>
            <p>L'analisi non funzionerà finché non imposti la variabile d'ambiente `PLAUSIBLE_API_KEY` sul server.</p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4" role="alert">
            <p className="font-bold">Errore di Analisi</p>
            <p>{error}</p>
          </div>
        )}

        {data && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-gray-700">Risultati per {data.domain}</h2>
            
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard title="Visitatori Unici" value={data.visitors.toLocaleString()} />
              <MetricCard title="Visualizzazioni Pagina" value={data.pageviews.toLocaleString()} />
              <MetricCard title="Frequenza di Rimbalzo" value={`${(data.bounce_rate * 100).toFixed(1)}%`} />
              <MetricCard title="Durata Media Visita" value={formatDuration(data.visit_duration)} />
            </div>

            <p className="text-sm text-gray-500 mt-4">Dati forniti da: {data.data_source}</p>
          </div>
        )}
      </main>
    </div>
  );
}

const MetricCard = ({ title, value }) => (
  <div className="bg-blue-50 p-5 rounded-lg shadow-md border border-blue-200">
    <p className="text-sm font-medium text-blue-600">{title}</p>
    <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
  </div>
);

export default App;
