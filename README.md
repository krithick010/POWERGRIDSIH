# POWERGRID AI Ticketing System

An AI-powered centralized IT ticketing system built with FastAPI, React, and Hugging Face models.

## Features

- **AI Chatbot Interface** - Natural language ticket creation with intelligent responses
- **Automatic Classification** - AI-powered category and priority detection using Hugging Face models
- **Knowledge Base Search** - Semantic search for self-service support
- **Ticket Dashboard** - Real-time ticket tracking and management
- **Email & SMS Alerts** - Automated notifications for ticket updates
- **Auto-Resolution** - Common issues resolved automatically with KB suggestions
- **SSO Ready** - Placeholder for corporate authentication
- **Responsive Design** - Works seamlessly on desktop and mobile devices

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database with vector support
- **Hugging Face Transformers** - BART for zero-shot classification
- **Sentence Transformers** - all-MiniLM-L6-v2 for semantic search
- **SMTP & Twilio** - Email and SMS notifications

### Frontend
- **Next.js 15** - React framework with App Router
- **Tailwind CSS v4** - Utility-first styling
- **shadcn/ui** - High-quality UI components
- **TypeScript** - Type-safe development

### AI/ML
- **facebook/bart-large-mnli** - Zero-shot text classification
- **sentence-transformers/all-MiniLM-L6-v2** - Sentence embeddings for KB search

## Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker (Recommended)

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd powergrid-ticketing
   \`\`\`

2. **Configure environment variables**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

3. **Start all services**
   \`\`\`bash
   docker-compose up -d
   \`\`\`

4. **Wait for services to be healthy**
   \`\`\`bash
   docker-compose ps
   \`\`\`

5. **Generate knowledge base embeddings**
   \`\`\`bash
   docker-compose exec backend python scripts/04-generate-embeddings.py
   \`\`\`

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend

\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/powergrid_tickets

# Run the server
uvicorn main:app --reload
\`\`\`

#### Frontend

\`\`\`bash
npm install
npm run dev
\`\`\`

## Database Setup

The database schema and seed data are automatically loaded when the PostgreSQL container starts.

### Manual Database Setup

\`\`\`bash
# Connect to the database
docker-compose exec db psql -U postgres -d powergrid_tickets

# Or run scripts manually
docker-compose exec db psql -U postgres -d powergrid_tickets -f /docker-entrypoint-initdb.d/01-create-schema.sql
docker-compose exec db psql -U postgres -d powergrid_tickets -f /docker-entrypoint-initdb.d/02-seed-knowledge-base.sql
docker-compose exec db psql -U postgres -d powergrid_tickets -f /docker-entrypoint-initdb.d/03-seed-sample-tickets.sql
\`\`\`

### Generate Embeddings

After seeding the knowledge base, generate embeddings for semantic search:

\`\`\`bash
docker-compose exec backend python scripts/04-generate-embeddings.py
\`\`\`

## API Endpoints

### Tickets
- `POST /tickets` - Create new ticket
- `GET /tickets/{id}` - Get ticket by ID
- `GET /tickets` - List tickets (with filters: employee, status, category)
- `PATCH /tickets/{id}/status` - Update ticket status

### AI/NLP
- `POST /classify` - Classify ticket text (category, priority, auto-resolve)
- `GET /kb/search?query=...` - Search knowledge base (semantic or keyword)
- `POST /chatbot` - Chatbot interaction (classify, search KB, create ticket)

### Knowledge Base
- `GET /kb/{id}` - Get KB article by ID

### Health
- `GET /health` - Health check
- `GET /` - API info

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

\`\`\`env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/powergrid_tickets

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@powergrid.in
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@powergrid.in

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

### Email Configuration

For Gmail SMTP:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use the app password in `SMTP_PASSWORD`

### SMS Configuration

For Twilio:
1. Sign up at https://www.twilio.com
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Add credentials to `.env`

## Project Structure

\`\`\`
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database connection
│   ├── models.py               # Database models
│   ├── ai_classifier.py        # Hugging Face classifier
│   ├── semantic_search.py      # Semantic search engine
│   ├── notifications.py        # Email/SMS service
│   ├── automation.py           # Automation rules
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend container
│   ├── test_ai.py              # AI component tests
│   └── test_notifications.py  # Notification tests
├── scripts/
│   ├── 01-create-schema.sql           # Database schema
│   ├── 02-seed-knowledge-base.sql     # KB seed data
│   ├── 03-seed-sample-tickets.sql     # Sample tickets
│   └── 04-generate-embeddings.py      # Embedding generation
├── app/
│   ├── page.tsx                # Main application page
│   ├── layout.tsx              # Root layout
│   └── globals.css             # Global styles
├── components/
│   ├── chatbot.tsx             # Chatbot interface
│   └── ticket-dashboard.tsx    # Ticket dashboard
├── lib/
│   └── api.ts                  # API client
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Frontend container
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
\`\`\`

## Testing

### Test AI Components

\`\`\`bash
docker-compose exec backend python test_ai.py
\`\`\`

### Test Notifications

\`\`\`bash
docker-compose exec backend python test_notifications.py
\`\`\`

### Test API

Visit http://localhost:8000/docs for interactive API documentation.

## Features in Detail

### AI Classification

The system uses Hugging Face's BART model for zero-shot classification:
- Automatically categorizes tickets (network, access, hardware, software, other)
- Assigns priority based on keywords and context
- Detects auto-resolvable issues

### Semantic Search

Uses sentence-transformers for intelligent KB search:
- Understands context and meaning, not just keywords
- Returns relevance scores for each result
- Caches embeddings for fast search

### Auto-Resolution

Common issues are automatically resolved:
- Password reset → Link to self-service portal
- VPN setup → Installation guide
- Email configuration → Mobile setup instructions

### Notifications

Automated email and SMS notifications:
- Ticket created → Confirmation with details
- Status updated → Progress notification
- Ticket resolved → Resolution confirmation (with SMS)

### Automation Rules

- SLA-based response times
- Auto-assignment based on category
- Escalation rules for overdue tickets

## Troubleshooting

### Database Connection Issues

\`\`\`bash
# Check database status
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
\`\`\`

### Backend Issues

\`\`\`bash
# View backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Check health
curl http://localhost:8000/health
\`\`\`

### Frontend Issues

\`\`\`bash
# View frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# Rebuild frontend
docker-compose up -d --build frontend
\`\`\`

### AI Model Loading Issues

AI models are downloaded during Docker build. If you encounter issues:

\`\`\`bash
# Rebuild backend with no cache
docker-compose build --no-cache backend

# Or download models manually
docker-compose exec backend python -c "from transformers import pipeline; pipeline('zero-shot-classification', model='facebook/bart-large-mnli')"
\`\`\`

## Production Deployment

### Security Checklist

- [ ] Change default database password
- [ ] Use strong passwords for all services
- [ ] Enable SSL/TLS for database connections
- [ ] Configure proper CORS origins
- [ ] Set up proper authentication (SSO)
- [ ] Use environment-specific secrets
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### Performance Optimization

- Use connection pooling (already configured)
- Cache AI model predictions
- Implement Redis for session management
- Use CDN for frontend assets
- Enable database query optimization
- Monitor and scale based on load

## Support

For issues or questions:
- Create an issue in the repository
- Contact IT Support at ext. 2222
- Email: itassets@powergrid.in

## License

Internal use only - POWERGRID Corporation

## Acknowledgments

- Built with FastAPI, Next.js, and Hugging Face
- UI components from shadcn/ui
- Icons from Lucide React
