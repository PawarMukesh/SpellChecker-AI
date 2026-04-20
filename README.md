# SpellChecker-AI

# Enterprise Writing Assistant

Enterprise Writing Assistant is a full-stack writing support application with a FastAPI backend and a React frontend. It provides:

- real-time spelling suggestions
- grammar guidance
- next-word prediction
- text rewriting in `rephrase`, `formal`, and `informal` modes

The application is structured so that deterministic language utilities run inside the backend, while generative AI features are delegated to a configurable Qwen-compatible model endpoint.

## Full Architecture

### High-Level Flow

```text
Frontend (React + Vite)
    |
    | HTTP /api/suggest, /api/rewrite
    v
Backend (FastAPI)
    |
    |-- Suggestion orchestrator
    |     |-- spell_service
    |     |-- grammar_service
    |     |-- autocomplete_service
    |             |
    |             | HTTP completion request
    |             v
    |       Qwen-compatible model endpoint
    |
    |-- rewrite_service
          |
          | HTTP completion request
          v
      Qwen-compatible model endpoint
```

### Backend Architecture

The backend follows a layered service-oriented structure:

- `app/main.py`
  Initializes FastAPI, CORS, request logging middleware, exception handling, and route registration.

- `app/api/routes/`
  Exposes the HTTP API:
  - `POST /api/suggest`
  - `POST /api/rewrite`

- `app/services/`
  Contains application logic:
  - `spell_service.py`: dictionary-based spelling correction
  - `grammar_service.py`: lightweight rule-based grammar checks
  - `autocomplete_service.py`: calls the AI model endpoint for next-word prediction
  - `rewrite_service.py`: calls the AI model endpoint for rewrite operations
  - `llm_client.py`: shared HTTP client for the model endpoint
  - `orchestrator.py`: combines spelling, grammar, and autocomplete into one suggestion response

- `app/models/`
  Pydantic request and response contracts for API consistency.

- `app/core/`
  Centralized configuration and logging setup.

### Frontend Architecture

The frontend is a Vite React application with a component-driven UI:

- `src/App.jsx`
  Composes the page shell, state management, and interaction flow.

- `src/components/Editor.jsx`
  Captures typing, debounces suggestion requests, and shows inline correction highlighting.

- `src/components/SuggestionBox.jsx`
  Displays next-word predictions, spelling guidance, and grammar guidance.

- `src/components/Toolbar.jsx`
  Triggers rewrite operations by mode.

- `src/services/api.js`
  Encapsulates Axios calls to backend APIs.

## Models Used

### Primary Model

- `Qwen/Qwen2.5-0.5B-Instruct`

This is the default model name configured in the backend environment settings. The application does not currently ship a bundled model server. Instead, it expects a Qwen-compatible completions endpoint configured through `MODEL_SERVER_URL`.

### Why This Model

`Qwen/Qwen2.5-0.5B-Instruct` is a small instruct-tuned model that is more practical than larger models for constrained environments. It is intended here as the default rewrite and autocomplete model because it is relatively lightweight compared with larger instruction models.

## What This Model Does

The Qwen model is used only for generative tasks.

### Used For

- rewrite text into a formal tone
- rewrite text into an informal tone
- rephrase text without changing meaning
- predict the next likely words during typing

### Not Used For

- rule-based spelling correction
- rule-based grammar checks
- HTTP orchestration
- UI rendering

Those responsibilities remain in deterministic backend logic.

## Current Approach

### Suggestion API

For `POST /api/suggest`, the backend does the following:

1. applies dictionary-based spell correction
2. runs lightweight grammar checks
3. sends the corrected typing context to the Qwen endpoint for next-word prediction
4. returns a unified suggestion payload

### Rewrite API

For `POST /api/rewrite`, the backend does the following:

1. selects a prompt template based on mode
2. sends the prompt to the Qwen endpoint
3. returns the generated rewritten text

## Is This Enterprise Level?

### Short Answer

It is an enterprise-oriented application scaffold, not a fully hardened enterprise platform yet.

### Why It Is Enterprise-Oriented

The current design already includes several correct architectural choices:

- backend and frontend are cleanly separated
- API contracts are explicit through Pydantic models
- services are modular and independently replaceable
- configuration is centralized
- logging and middleware are present
- AI calls are isolated behind a client abstraction
- UI and backend can scale independently

### Why It Is Not Yet Fully Enterprise-Ready

For a real enterprise deployment, the project still needs:

- authentication and authorization
- role-based access control
- persistent storage for users, history, and audit data
- request throttling and abuse protection
- retries, circuit breaking, and model health monitoring
- structured observability with metrics and tracing
- automated tests at unit, integration, and end-to-end levels
- CI/CD pipelines
- secret management
- environment-specific configuration strategy
- deployment manifests and production infrastructure automation

So the correct assessment is:

- architecture direction: good
- code organization: good
- production hardening: incomplete

## Can We Deploy This Application?

### Yes, With Conditions

Yes, the application can be deployed, but only if a live Qwen-compatible model endpoint is available.

### Deployable Parts Today

- FastAPI backend
- React frontend
- rule-based spell correction
- rule-based grammar checks

### External Dependency Required

The rewrite and autocomplete features depend on:

- `MODEL_SERVER_URL`
- a reachable endpoint that accepts completion-style requests and returns `choices[0].text`

Without that endpoint:

- rewrite falls back to returning the original text
- next-word prediction returns an empty list

### Deployment Recommendation

For production deployment, the best approach is:

1. deploy the frontend separately as a static web application
2. deploy the FastAPI backend as an API service
3. connect the backend to a dedicated Qwen-serving layer
4. monitor latency, failures, and model quality

## Project Structure

```text
backend/
  app/
    api/routes/
    core/
    models/
    services/
    main.py
  .env.example
  requirements.txt

frontend/
  src/
    components/
    services/
    App.jsx
    index.css
    main.jsx
  .env.example
  package.json
  vite.config.js

scripts/
  start-windows.ps1
```

## Run Notes

### Backend

The startup script already launches the backend from the correct directory. If you run it manually, use the `backend` directory as the working directory.

Example:

```powershell
Set-Location .\backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
Set-Location .\frontend
npm install
npm run dev
```

### Model Endpoint

Set `MODEL_SERVER_URL` in `backend/.env` to your running Qwen-compatible endpoint.

Example:

```env
MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
MODEL_SERVER_URL=http://your-qwen-server:8001/v1/completions
MODEL_TIMEOUT_SECONDS=15
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
```

## Final Assessment

This project is a solid enterprise-style foundation for an AI writing assistant. It is deployable as an application stack, but it is not yet a complete enterprise product until operational concerns and a real model-serving dependency are handled properly.
