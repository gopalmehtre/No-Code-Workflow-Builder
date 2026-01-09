# FlowAI Studio 🚀

A powerful **No-Code Workflow Builder** for creating AI-powered document processing workflows. Build custom workflows to upload PDFs, extract knowledge, and chat with your documents using drag-and-drop interface and advanced AI models.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-19.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

---

## ✨ Key Features

### Implemented
- **Visual Workflow Builder** - Drag-and-drop components, real-time validation
- **Document Processing** - PDF upload, text extraction, automatic chunking
- **Vector Search** - Semantic search with ChromaDB embeddings
- **AI Chat** - Context-aware responses using Google Gemini AI
- **RESTful API** - FastAPI with automatic OpenAPI documentation
- **Database** - PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Docker Ready** - Complete containerization with docker-compose

---

## 🛠️ Tech Stack

**Frontend:** React 19.2 • React Flow 11.11 • Zustand 5.0 • Tailwind CSS 3.4 • Vite 7.2

**Backend:** FastAPI 0.109 • Python 3.11 • Uvicorn • SQLAlchemy 2.0 • Pydantic 2.5

**Database:** PostgreSQL 15 • ChromaDB 0.4 • Alembic 1.13

**AI/ML:** Google Gemini AI • OpenAI SDK • PyPDF 4.0

**DevOps:** Docker • Docker Compose • Nginx

---

## 📦 Prerequisites

**For Docker (Recommended):**
- Docker 20.10+ & Docker Compose 2.0+
- 4GB RAM minimum

📘 **Complete Docker guide:** [DOCKER.md](DOCKER.md)

**For Local Development:**
- Python 3.11+ • Node.js 18+ • PostgreSQL 15+
- 8GB RAM recommended

---

## 🚀 Quick Start (Docker)

```bash
# 1. Clone and navigate
git clone <repository-url>

# 2. Configure environment (create backend/.env)
Create `backend/.env`:

```bash
GEMINI_API_KEY=your_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/workflow_db
CHROMA_HOST=localhost  # Use 'chromadb' for Docker
CHROMA_PORT=8000
LLM_PROVIDER=gemini
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
MAX_UPLOAD_SIZE=10485760  # 10MB
```

# 3. Build and start
docker-compose build
docker-compose up -d

# 4. Initialize database
docker-compose exec backend alembic stamp head

# 5. Access
# Frontend: http://localhost
# API Docs: http://localhost:8080/docs

---

## 💻 Local Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Create .env with DATABASE_URL and GEMINI_API_KEY
alembic upgrade head
uvicorn app.main:app --reload --port 8080
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Databases:**
- Install PostgreSQL 15 and create `workflow_db`
- Start ChromaDB: `chroma run --path ./chroma_data --port 8000`

---

## 📖 Usage

1. **Create Workflow** - Navigate to http://localhost, click "Create New Workflow"
2. **Add Components** - Drag User Query, Knowledge Base, LLM Engine, and Output nodes
3. **Connect Nodes** - Click and drag between node ports
4. **Configure** - Click gear icon on Knowledge Base to upload PDF
5. **Save** - Click "Save" button and name your workflow
6. **Chat** - Click chat icon and ask questions about your PDF

**API Documentation:** http://localhost:8080/docs

---

## 🚧 Future Enhancements

### 🔐 Authentication & Security
- User registration and JWT-based authentication
- Role-based access control (Admin, User, Viewer)
- Workflow sharing and collaboration
- API key management

### 📊 Analytics & Monitoring
- Execution analytics dashboard
- Usage statistics and cost tracking
- Response time and error monitoring
- Activity logs

### ⚡ Enhanced Workflows
- Conditional logic (if/else branches)
- Loops and iterations
- Variables and data transformation
- Sub-workflows and templates
- Parallel execution
- Version control for workflows

### 🤖 AI Improvements
- Multi-model support (Claude, GPT-4, Llama)
- Model comparison mode
- Advanced RAG (hybrid search, re-ranking, query expansion)
- Fine-tuning capabilities
- Agent features with tool use

### 📁 Document Management
- Support for Word, Excel, PowerPoint files
- OCR for scanned documents and images
- Web page import (URL)
- Batch upload and processing
- Document versioning
- Collections and grouping

### 🎨 UI/UX Enhancements
- Dark mode
- Mobile responsive design
- Drag-and-drop file upload
- Keyboard shortcuts
- Workflow minimap
- Multi-language support
- Accessibility (WCAG 2.1 AA)

### 🔗 Integrations
- Webhooks for external triggers
- REST API calls from workflows
- Slack integration
- Email processing
- Google Drive and Dropbox sync
- Zapier/Make connectors
- Export results (CSV, JSON, PDF)

### 🧪 Testing & Quality
- Unit and integration tests
- E2E tests with Playwright
- Load testing
- Code coverage
- CI/CD pipeline

### 📈 Scalability
- Redis caching
- Celery background tasks
- Message queue (RabbitMQ)
- Kubernetes deployment
- CDN integration
- Database replicas

### 🛡️ Security Hardening
- Rate limiting
- Input sanitization
- Security headers
- Penetration testing
- GDPR/HIPAA compliance

---

## Troubleshooting

**Docker Issues:** See [DOCKER.md#troubleshooting](DOCKER.md#troubleshooting)

**Common Fixes:**
```bash
# Rebuild everything
docker-compose down -v && docker-compose build --no-cache && docker-compose up -d

# View logs
docker-compose logs -f backend
```

**API Errors:**
- **429 Quota Exceeded**: Wait or use different Gemini API key
- **PDF Upload Fails**: Check file size < 10MB, text-based PDF
- **Collection Not Found**: Re-upload PDF in Knowledge Base node

---

## Author

- Gopal Mehtre.
