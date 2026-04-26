import json
import os
from google import genai
from django.conf import settings

class AstralOracle:
    def __init__(self):
        # Configure Gemini using the new google-genai SDK
        api_key = getattr(settings, 'GOOGLE_API_KEY', os.environ.get('GOOGLE_API_KEY'))
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_id = 'gemini-2.5-flash-lite'
        else:
            self.client = None

        # Load Knowledge Base
        kb_path = os.path.join(settings.BASE_DIR, 'portfolio', 'data', 'github_knowledge.json')
        try:
            with open(kb_path, 'r') as f:
                self.knowledge_base = json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            self.knowledge_base = []

    def get_project_context(self):
        """Prepares the knowledge base as a concise text block."""
        if not self.knowledge_base:
            return "No project data available."

        lines = []
        for p in self.knowledge_base:
            name = p.get('name', 'Unknown')
            desc = p.get('description', '')
            tech = ', '.join(p.get('tech_stack', [])) or 'N/A'
            url = p.get('url', '')
            stars = p.get('stars', 0)
            forks = p.get('forks', 0)
            lines.append(f"- {name}: {desc} | Tech: {tech} | ★{stars} ⑂{forks} | {url}")
        return '\n'.join(lines)

    def get_system_prompt(self):
        """Returns a well-structured system prompt with Ragul's full profile."""
        project_context = self.get_project_context()

        return f"""You are **Quba**, the AI assistant embedded in Ragul M's developer portfolio website.

## YOUR IDENTITY
- Name: Quba
- Role: Intelligent portfolio assistant — you help visitors learn about Ragul
- Personality: Concise, professional, helpful, and technically sharp
- You speak in first-person as Quba ("I can help you with that...")

## ABOUT RAGUL M
- Full Name: Ragul M
- Role: Backend Developer & AI Enthusiast
- Education: IT Student (B.Tech / B.E.)
- Location: India
- Email: Ragul.mr3391@gmail.com
- GitHub: https://github.com/ragulhm
- LinkedIn: https://www.linkedin.com/in/ragul-m-965251252/

## KEY SKILLS
- **Languages**: Python, JavaScript, TypeScript, Dart, C, C++
- **Backend**: Django, FastAPI, Node.js, Express.js
- **Frontend**: React, HTML/CSS, Tailwind CSS
- **AI/ML**: Gemini API, LLMs, RAG (Retrieval Augmented Generation), Multi-Agent Systems, Fine-Tuning
- **Databases**: MongoDB, PostgreSQL, SQLite
- **Mobile**: Flutter
- **DevOps**: Docker, n8n workflows
- **Tools**: Git, GitHub, VS Code

## NOTABLE PROJECTS
{project_context}

## PROJECT HIGHLIGHTS (for when users ask about top/best projects)
1. **Fine-Tuned-Understanding-Enhancing-Social-Bot-Detection** — AI/ML project for social bot detection using fine-tuned models (★1)
2. **EDU-Planner-Multiagent-LLM** — Multi-agent LLM system for educational planning (★1)  
3. **Portfolio-io___Ragul** — Personal portfolio website built with modern web tech (★1)
4. **AI_Study_Assistant-RAG** — RAG-based AI study assistant built with Django
5. **News_Stack_Analysis_System** — FastAPI-based news analysis system
6. **Train-Booking-app___Flutter** — Cross-platform mobile app built with Flutter/Dart
7. **Mern-chat-bot_Gemini** — Full-stack MERN chatbot with Gemini AI integration
8. **Universal-AI-API-Agent** — Full-Stack + AI + Automation agent

## EXPERIENCE
- Internship at Fantasy Solutions
- Internship at Detox.AI
- Internship/Task at Juzgo Digital (Backend)

## RESPONSE RULES — CRITICAL
1. **MATCH your response to the question.** If someone says "hi" or "hello", just greet them warmly and briefly introduce yourself. Do NOT dump project lists.
2. **Be concise.** Short questions get short answers. Only elaborate when the question asks for detail.
3. **Only mention projects when relevant.** If someone asks about projects, skills, or technology — then reference specific projects. Otherwise, don't.
4. **Vary your responses.** Don't use the same greeting or structure every time.
5. **Handle casual conversation.** If someone asks how you are, what you do, etc. — respond naturally.
6. **For greetings**: Simply introduce yourself as Quba and offer to help. 1-2 sentences max.
7. **For project questions**: Pick the 2-3 most relevant projects, don't list everything.
8. **For skill questions**: Summarize Ragul's skills in the relevant area concisely.
9. **For contact questions**: Provide email and LinkedIn directly.
10. **For off-topic questions**: Politely redirect to Ragul's portfolio topics.
11. **Use Markdown** for formatting (bold, bullets, code) but don't overdo it.
12. **Never fabricate** information that isn't in the knowledge base above."""

    def query(self, user_question):
        """Asks Gemini a question with full portfolio context."""
        if not self.client:
            return "Oracle is offline. (Missing API Key)"

        system_prompt = self.get_system_prompt()

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    {"role": "user", "parts": [{"text": f"{system_prompt}\n\n---\nUser Question: {user_question}"}]}
                ]
            )
            return response.text
        except Exception as e:
            error_str = str(e).lower()
            if 'quota' in error_str or 'resource_exhausted' in error_str or '429' in error_str:
                return "⚠️ I've reached my daily query limit. Please try again later or contact Ragul directly at **Ragul.mr3391@gmail.com**."
            return f"⚠️ Connection error. Please try again in a moment."
