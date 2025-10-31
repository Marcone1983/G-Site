# Audit Tecnico e Refactoring del Progetto G-Site

**Data:** 30 Ottobre 2025
**Autore:** Manus AI

## 1. Risultati dell'Audit Iniziale

L'audit del repository **Marcone1983/G-Site** ha confermato l'analisi iniziale fornita dall'utente, identificando le seguenti criticità principali:

| Criticità | Descrizione | Impatto | Stato |
| :--- | :--- | :--- | :--- |
| **Frontend Obsoleto** | Utilizzo di un sistema di build non standard (`build/` con Babel CommonJS) e caricamento diretto nel browser. | **Critico.** Causa l'errore `ReferenceError: require is not defined` e la conseguente "pagina bianca" su Render e GitHub Pages. | Risolto |
| **Dipendenze Non Necessarie** | Presenza di logica e dipendenze per un database (Flask-SQLAlchemy) e un'API di gestione utenti. | Inutile, in quanto l'utente ha confermato che l'applicazione non richiede un database. | Rimosso |
| **API di Traffico Fittizia** | Il file `real_traffic.py` simulava l'analisi del traffico, utilizzando una chiave API fittizia di SimilarWeb e algoritmi di stima basati su hash del dominio. | Non fornisce dati reali e non è "Enterprise Ready". | Rimosso/Sostituito |
| **Configurazione Tailwind** | Il CSS non era compilato correttamente e non era integrato nel processo di build. | Causa problemi di stile e non permette l'uso completo delle utility class. | Risolto |

## 2. Soluzione Architetturale Implementata

In linea con la richiesta dell'utente di utilizzare un'API di analytics open-source, è stata implementata una nuova architettura focalizzata su **Plausible Analytics**, con un design a **proxy sicuro** per rispettare la preferenza dell'utente per la gestione sicura delle chiavi API.

### 2.1. Refactoring del Backend (Flask)

Il backend Flask è stato semplificato e riconfigurato per due funzioni principali:

1.  **Servire il Frontend Statico:** Gestisce il routing per l'applicazione a pagina singola (SPA) compilata da Vite, inclusa la corretta gestione dei MIME type per i file `.jsx` e `.css`.
2.  **Proxy API Plausible:** L'endpoint `/api/traffic/proxy/plausible` funge da intermediario. Riceve le richieste dal frontend, le inoltra all'API Plausible (autenticandosi con la `PLAUSIBLE_API_KEY` memorizzata sul server), e restituisce la risposta al client.

> **Vantaggio:** La chiave API Plausible rimane segreta sul server (Render) e non viene mai esposta al browser (GitHub Pages).

**Componenti Rimosse:**
*   `models/` (Database)
*   `user.py` (API Utente)
*   `Flask-SQLAlchemy` (dalle dipendenze Python)

### 2.2. Migrazione del Frontend (React/Vite/Tailwind)

Il frontend è stato migrato a uno stack di sviluppo moderno:

*   **Vite:** Sostituisce il vecchio sistema di build, garantendo una compilazione rapida e corretta.
*   **React:** L'applicazione è stata riscritta in `app.jsx` per includere una semplice interfaccia utente (UI) per l'analisi del traffico.
*   **Tailwind CSS:** Configurato correttamente con PostCSS e Autoprefixer, risolvendo i problemi di stile.

### 2.3. Integrazione API Plausible (Fase 1)

L'applicazione è stata configurata per interrogare l'API Plausible Stats per le metriche chiave: **Visitatori Unici**, **Visualizzazioni Pagina**, **Frequenza di Rimbalzo** e **Durata Media Visita**.

**Funzionamento:**
1.  L'utente inserisce il dominio e clicca su "Analizza Traffico".
2.  Il frontend invia una richiesta POST all'endpoint proxy Flask `/api/traffic/proxy/plausible`.
3.  Flask inoltra la richiesta a `https://plausible.io/api/v2/query` con la chiave API segreta.
4.  I dati vengono restituiti e visualizzati nell'interfaccia utente.

## 3. Istruzioni per il Deploy e l'Uso

Le modifiche sono state committate e pusshate nel repository **Marcone1983/G-Site**.

### 3.1. Deploy su Render (Backend Flask)

Per far funzionare l'API proxy, è necessario configurare la variabile d'ambiente segreta su Render:

| Variabile | Valore | Note |
| :--- | :--- | :--- |
| `PLAUSIBLE_API_KEY` | `[La tua chiave API Plausible]` | **Obbligatoria.** Senza questa chiave, l'API proxy restituirà un errore 500 al frontend. |

### 3.2. Deploy su GitHub Pages (Frontend Vite)

Il frontend è ora pronto per essere compilato e ospitato come sito statico.

**Passaggi per la compilazione:**
1.  Eseguire `pnpm install`
2.  Eseguire `pnpm vite build`

La directory `build/` risultante può essere servita come sito statico su GitHub Pages.

## 4. Prossimi Passi (Priorità Utente)

L'utente ha richiesto di implementare **Umami** e **Open Web Analytics** come alternative se Plausible non dovesse funzionare.

**Proposta per la Fase 2:**
*   **Implementare la logica di fallback** nel frontend per consentire all'utente di selezionare l'API (Plausible, Umami, OWA).
*   **Sviluppare un proxy API** separato in Flask per l'API di Umami e/o OWA, se necessario, mantenendo la sicurezza della chiave API.

---
*Nota: A causa di un errore di loop durante la fase di test nel sandbox, si consiglia di contattare il supporto Manus all'indirizzo [https://help.manus.im](https://help.manus.im) per qualsiasi problema relativo ai crediti.*
