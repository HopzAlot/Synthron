# 🛠️ Synthron – Custom PC Recommendation Platform

**Synthron** is a full-stack web application that helps users intelligently build custom PC configurations based on their needs (gaming, editing, budget, etc.) using a combination of AI prompt parsing and real-time price scraping from trusted websites.

The system uses **React** for the frontend and **Django + Django REST Framework** on the backend, connected via REST APIs. It uses an **LLM (LLaMA 3.2)** locally to interpret user prompts, and **Playwright** for dynamic scraping of part prices and availability.

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
DATABASE_URL=postgres://username:password@localhost:5432/pcbuilder
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

---

## ⚠️ LLaMA 3.2 Usage

Synthron uses **LLaMA 3.2 locally** for AI prompt parsing.  
To fully use the project, you'll need to **download and run the LLaMA 3.2 model** locally.  
Refer to the `llama.py` script for how it's integrated, and ensure your machine meets the requirements for running LLaMA models.

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
- 🐳 **Containerization** using Docker
- ⚙️ Implementation of **CI/CD pipelines**
- 🚀 **Cloud deployment** on **AWS**


---

## 🤝 Want to Contribute?
Contact me on my email:
rehansaqib2006@gmail.com

Feel free to open an issue or PR!
