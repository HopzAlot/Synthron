## 🛠️ Synthron – Custom PC Recommendation Platform

**Synthron** is a full-stack web application that helps users intelligently build custom PC configurations based on their needs (gaming, editing, budget, etc.) using a combination of AI prompt parsing and real-time price scraping from trusted websites.

The system uses **React** for the frontend and **Django + Django REST Framework** on the backend, connected via REST APIs.**PostgreSQL** is used to store User's data and **Redis** acts as a cache system to temporarily store the results for faster accessibility. It uses an **LLM (LLaMA 3.2)** locally to interpret user prompts, and **Playwright** for dynamic scraping of part prices and availability.

> 🔍 Currently achieving **70–75% scraping predictability/accuracy**. Further improvements are planned.


---



## ✨ Features

- 🧠 **AI-driven prompt interpretation** (LLaMA 3.2)
- 🔍 **Real-time scraping** of PC parts from trusted e-commerce websites
- ⚙️ **Component agents**: CPU, GPU, RAM, Storage, Motherboard
- 🌐 **Region-aware pricing** and availability
- 🔐 **JWT-based authentication** with HttpOnly cookie storage
- 📦 **Build history**: Saved per user and fetchable later
- 🧪 **Compatibility checker**: Validates part compatibility (e.g., socket types)
- ⚡ Fast, modern UI using **React + Tailwind CSS**

---

## 📁 Folder Structure

```
ai-pc-builder/
├── backend/
│   ├── api/
│   │   ├── agents/
│   │   │   ├── cpu_agent.py
│   │   │   ├── gpu_agent.py
│   │   │   ├── ram_agent.py
│   │   │   ├── storage_agent.py
│   │   │   ├── motherboard_agent.py
│   │   │   ├── llama.py
│   │   │   ├── playwright_scraper.py
│   │   │   └── product_finder.py
│   │   ├── compatibility_checker.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   ├── settings.py
│   ├── manage.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api.js        
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── package.json
├── README.md
└── .gitignore
└── .env
└── .docker-compose.yml

```

---

## ⚙️ Backend – Django Setup

### 1. Clone and set up virtual environment:

```bash
git clone https://github.com/yourusername/ai-pc-builder.git
cd ai-pc-builder/backend

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

pip install -r requirements.txt
```

### 2. Create `.env` file:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=5432
```

### 3. Run migrations and start server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 📦 Backend Dependencies (`backend/requirements.txt`)

```
Django>=4.2
djangorestframework
python-dotenv
httpx
playwright
psycopg2-binary
```

To install Playwright browsers:

```bash
playwright install
```

---

## 🎨 Frontend – React Setup

### 1. Navigate to frontend directory:

```bash
cd ../frontend
```

### 2. Install dependencies:

```bash
npm install
```

### 3. Run development server:

```bash
npm run start
```
## 🐳 Docker Setup (Recommended)

Synthron is fully containerized. This is the fastest way to get the project running.

### 1. Environment Variables (`.env`)
Create a `.env` file in the project root:

```env
COMPOSE_PROJECT_NAME=synthron

# PostgreSQL
POSTGRES_DB=synthron
POSTGRES_USER=synthron
POSTGRES_PASSWORD=synthronpassword

# Django Backend
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=*

DATABASE_URL=postgres://synthron:synthronpassword@postgres:5432/synthron
REDIS_URL=redis://redis:6379/0
OLLAMA_BASE_URL=http://ollama:11434

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```
---
## ⚓ Docker-Compose File
   Make a docker-compose.yml file in your project directory and attach the code below.

   ``` dockercompose
version: "3.9"

services:
  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks: [synthron-net]

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks: [synthron-net]

  ollama:
    image: ollama/ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks: [synthron-net]

  backend:
    build: ./backend
    restart: unless-stopped
    env_file: [.env]
    depends_on:
      - postgres
      - redis
      - ollama
    ports:
      - "8000:8000"
    networks: [synthron-net]

  frontend:
    build: ./frontend
    restart: unless-stopped
    env_file: [.env]
    depends_on:
      - backend
    ports:
      - "3000:80"
    networks: [synthron-net]

volumes:
  postgres_data:
  ollama_data:

networks:
  synthron-net:
    driver: bridge
   ```
---


## ⚠️ LLaMA 3.2 Usage

Synthron uses **LLaMA 3.2 locally** for AI prompt parsing.  
   - **Docker Users**: Handled automatically via the ollama service.  
      
   - **Manual Users**: Install Ollama and run ollama pull llama3.2.

---


## 🔗 How It Works

1. **User Input**: "I want a gaming PC under $1000 in Usa and i prefer an AMD build."
2. **LLM** parses intent, budget, and region.
3. Each **component agent** (CPU, GPU, RAM, etc.) activates.
4. Agents create **product-specific search queries**.
5. **Serper** fetches urls off the web.
6. **Playwright** scrapes trusted e-commerce websites.
7. Components are selected and ranked by:
   - 🔄 Stock availability
   - 💰 Lowest price
   - 🙋 User preference
8. The **result** is rendered on the frontend with prices and product links.

---

## ✅ Trusted Sites Scraped

- [Amazon](https://amazon.com)
- [Newegg](https://newegg.com)
- [Microcenter](https://microcenter.com)
- [Scan UK](https://scan.co.uk)
- And more…

> 🗑️ `ScrapeGraph` API was removed due to limited free-tier usage. All scraping is now handled with Playwright.

---

## ⚠️ Known Limitations

- 🛒 Scraping accuracy is 70–75% — dynamic rendering and anti-bot measures may impact results.
- ❌ Not all product queries yield valid results (fallback logic is used).
- 🌍 Currency and regional detection are still basic.

---

## 🔮 Roadmap

- 🧠 Improve scraping reliability via AI heuristics
- 🔌 Add PSU and case suggestions
- 💸 Integrate Amazon Affiliate tracking
- 📊 Admin dashboard for scraping diagnostics
- 🔐 OAuth login support (Google, GitHub)
- 🛠️ Improving LLM integration and scraping engine.

---


## 🧠 What's Next?

I’ll be actively improving Synthron with:

- ✨ More exciting features and enhancements
- 🛠️ Integration of modern **DevOps tooling and workflows**
- ⚙️ Implementation of **CI/CD pipelines**
- 🚀 **Cloud deployment** on **AWS**


---

## 🤝 Want to Contribute?
Contact me on my email:
rehansaqib2006@gmail.com

**Feel free to open an issue or PR!**