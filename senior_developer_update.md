# Technical Update: Portfolio System Integrations (v2.1)

## 1. Quba AI Assistant — "Neural Terminal"
Transformed the generic chat module into a bespoke, high-end AI concierge using a **Neural Terminal** architecture.

- **UI/UX Core**: Implemented a sci-fi HUD aesthetic. Key elements include an animated **Neural Orb** trigger (CSS-animated orbiting rings), terminal-style monospace message blocks, and a **Waveform Typing Indicator** (5-bar oscillating SVG).
- **Intelligence Layer**: Upgraded to **Gemini 2.0 Flash** via the `google-genai` SDK.
- **RAG Architecture**: Implemented a localized knowledge retrieval system. The AI queries a `github_knowledge.json` matrix generated dynamically from the owner's GitHub metadata.
- **Context-Aware Prompting**: Replaced static response templates with a **12-rule system prompt** that enables the agent to differentiate between casual greetings, technical skill inquiries, and project deep-dives, avoiding unsolicited "project dumping."
- **Deployment Fix**: Resolved a `ModuleNotFoundError` on Render by implementing a dynamic `sys.path` resolution in the extraction script and standardizing `PYTHONPATH` in `build.sh`.

## 2. GitHub Integration — "Live Pulse"
Created a real-time bridge between the portfolio and GitHub.

- **Activity Feed**: Backend integration (`github_api.py`) fetches and caches the latest public events (commits, pushes) to display a "Live Pulse" in the HUD.
- **Knowledge Matrix Extraction**: Developed `portfolio/scripts/extract_knowledge.py` which aggregates metadata (Description, Tech Stack, Stars, Forks) for 30+ repositories. This data is flattened into JSON for the AI's RAG system.

## 3. Medium Integration — "Blog Sync"
Automated technical content delivery.

- **RSS Pipeline**: Built a robust parsing system (`medium_api.py`) using `feedparser` and `BeautifulSoup4` to ingest articles from the Medium RSS feed.
- **Dynamic Ingestion**: Articles are automatically fetched and mapped to the portfolio's "Articles" section on page load, eliminating manual blog updates.

## 4. Architecture & Build System
- **Node-Optional Stack**: Utilized a standalone Tailwind CLI to maintain a high-end UI without requiring a persistent Node.js runtime.
- **Django Monolith**: Centralized all logic into a Django 5.0 core, utilizing Alpine.js for lightweight frontend reactivity and GSAP for scroll-triggered "reveal" animations.
- **CI/CD Readiness**: Optimized `render.yaml` and `build.sh` for one-click deployment, including automated static collection, database migrations, and knowledge matrix refreshing.

---
**Status**: All integrations live and verified on Render (Django-Backend branch).
**Lead Dev**: Ragul M
**System Architect**: Antigravity AI
