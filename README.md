# 🌌 Astral Architect IO - Portfolio System

A high-performance, developer portfolio built with **Django 5.0**, **Three.js**, and **Gemini 2.0 Flash**. This project features a cutting-edge **Quba AI Assistant** and seamless automation for GitHub and Medium integrations.

![Portfolio Preview](https://github.com/ragulhm/Portfolio-io___Ragul/raw/Django-Backend/static/images/hero_preview.webp)

## 🚀 Live Demo
(https://portfolio-io-ragul.onrender.com/)

## ✨ Unique Features

### 🤖 Quba AI Assistant (New)
- **Premium AI Concierge**: Built with **Gemini-2.5-flash-lite** via the `google-genai` SDK.
- **Context Aware**: Automatically analyzes your GitHub projects to suggest the best repositories to visitors.
- **Structured Interaction**: Delivers structured, point-based answers with Markdown support for a high-end chat experience.
- **Auto-Engagement**: Automatically opens after 3 seconds to greet new visitors.

### 🎨 Design & Interaction
- **Astral System UI**: Luxury glassmorphic interface with interactive 3D elements powered by Three.js.
- **Motion Orchestration**: Seamless animations using GSAP and ScrollTrigger.
- **Bento Grid Layout**: Modern, responsive masonry layout for project showcases.

### ⚙️ Automation
- **GitHub Pulse**: Real-time integration showcasing the latest commits and open-source activities.
- **Medium Sync**: Automated blog ingestion via the Medium RSS API.

## 🛠️ Technology Stack
- **Backend**: Django 5.0 (Python 3.11)
- **AI Engine**: Google Gemini 2.0 Flash (`google-genai` SDK)
- **Frontend**: Alpine.js, Tailwind CSS
- **3D Graphics**: Three.js (WebGL Globe)
- **Styling**: Vanilla CSS (Custom Glassmorphism Tokens)
- **Deployment**: Render, Gunicorn, WhiteNoise

## 📦 Local Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/ragulhm/Portfolio-io___Ragul.git
   cd django_portfolio
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   GITHUB_TOKEN=your_github_pat
   GOOGLE_API_KEY=your_gemini_api_key
   ```

3. **Launch**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 🤝 Contributing
Developed by **[Ragul M](https://github.com/ragulhm)** - AI & Python Developer.
