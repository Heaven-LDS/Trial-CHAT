## ChatGPT-like App (React + FastAPI)

This project is a simple ChatGPT-style web app with:

- **Frontend**: React (TypeScript, Vite-style structure)
- **Backend**: FastAPI (Python)
- **LLM Provider**: GitHub API (based on DeepSeek) — **not wired by default** so the code runs without a key.

---

## Project Structure

- `backend/`
  - `main.py` – FastAPI app exposing `/api/chat`
  - `requirements.txt` – Python dependencies
- `frontend/`
  - `package.json` – Frontend dependencies and scripts
  - `src/App.tsx` – Chat UI

You can adjust or reorganize as needed.

---

## Backend Setup (FastAPI)

From `backend/`:

```bash
python -m venv .venv
.venv\Scripts\activate  # on Windows

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Configuration:**

The `/api/chat` endpoint:

- Accepts JSON: `{ "message": "hello" }`
- Returns JSON: `{ "reply": "..." }`
- If `OPENAI_API_KEY` is **not** set, returns a mock response: `"(mock) You said: ..."`
- **Automatic queueing**: Requests are automatically queued to respect GitHub API rate limits (1 request/minute)
- Multiple rapid requests will be processed sequentially with proper delays

**Environment Variables:**

Create a `.env` file in `backend/` directory:

```env
OPENAI_API_KEY=your_github_pat_token
OPENAI_BASE_URL=https://models.inference.ai.azure.com
OPENAI_MODEL=DeepSeek-V3-0324
```

> ⚠️ **Security Note**: The `.env` file is ignored by `.gitignore`. Never commit it to version control!

Alternatively, you can set environment variables directly:

- `OPENAI_API_KEY` – your GitHub API key (DeepSeek models)
- `OPENAI_MODEL` – e.g. `DeepSeek-V3-0324`
- `OPENAI_BASE_URL` – GitHub API base URL: `https://models.inference.ai.azure.com`

---

## Frontend Setup (React)

From `frontend/`:

```bash
npm install
npm run dev
```

The React app:

- Shows a simple chat window (user vs assistant bubbles)
- Sends input to `http://localhost:8000/api/chat`
- Displays the reply from the backend

You can later replace the minimal styling with a component library (e.g. Tailwind, MUI, etc.).

---

## 🚀 Deployment

### Quick Deployment (Free & Easy)

We recommend deploying to:
- **Frontend**: Vercel (free, global CDN, auto HTTPS)
- **Backend**: Render (free, auto restart)

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### One-Line Deploy
```bash
# Backend to Render
# Follow: https://render.com/docs/deploy-node-express-app

# Frontend to Vercel
# Follow: https://vercel.com/docs/deployments/overview
```

---

## Next Steps / Ideas

- **Wire real LLM**: uncomment and configure the GitHub API (DeepSeek models) call in the backend.
- **Add chat history**: send message history to the backend instead of only the last message.
- **Streaming responses**: use Server-Sent Events (SSE) or WebSockets for token-by-token streaming.
- **Authentication**: add login, rate-limiting, etc. for real users.

