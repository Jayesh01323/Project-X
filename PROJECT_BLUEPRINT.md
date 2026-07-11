# Project-X Blueprint

## Executive Summary

Project-X is a full-stack engineering foundation that integrates three core components:
1. **FastAPI Backend** - RESTful API with SQLModel ORM
2. **React Frontend** - Modern web interface (placeholder)
3. **Chrome Extension** - Browser integration (Manifest V3)

This blueprint defines the architecture, technical decisions, and implementation roadmap for the project.

---

## 1. System Architecture

### 1.1 High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         Project-X System                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Chrome     │    │   React      │    │   FastAPI    │     │
│  │  Extension   │◄──►│  Frontend    │◄──►│   Backend    │     │
│  │  (V3)        │    │  (Vite+TS)   │    │  (SQLModel)  │     │
│  └──────────────┘    └──────────────┘    └──────┬──────┘     │
│                                                  │             │
│                                            ┌─────▼─────┐      │
│                                            │  SQLite   │      │
│                                            │ Database  │      │
│                                            └───────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Communication Protocols

- **Extension ↔ Backend**: REST API over HTTP
- **Frontend ↔ Backend**: REST API over HTTP
- **Backend ↔ Database**: SQLModel ORM with SQLite
- **Extension ↔ Content Scripts**: Chrome Runtime Messaging
- **Extension ↔ Popup**: Chrome Runtime Messaging

---

## 2. Backend Architecture

### 2.1 Technology Stack

- **Framework**: FastAPI 0.110+
- **ORM**: SQLModel 0.0.16+
- **Config**: Pydantic Settings 2.2+
- **Server**: Uvicorn 0.27+
- **Database**: SQLite (development), PostgreSQL (production-ready)

### 2.2 Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application instance
│   ├── api/                       # API route handlers
│   │   ├── __init__.py
│   │   ├── v1/                    # API v1 routes
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main API router
│   │   │   └── endpoints/         # Individual endpoint modules
│   │   │       ├── health.py
│   │   │       ├── users.py
│   │   │       └── ...
│   │   └── dependencies.py        # Shared API dependencies
│   ├── core/                      # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py              # Settings model
│   │   ├── settings.py            # Settings instance
│   │   └── security.py            # Security utilities
│   ├── database/                  # Database configuration
│   │   ├── __init__.py
│   │   ├── session.py             # DB session management
│   │   └── base.py                # Base model class
│   ├── models/                    # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── ...
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── ...
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── ...
│   ├── providers/                 # External provider integrations
│   ├── learning/                  # Learning/AI modules
│   ├── memory/                    # Memory management
│   ├── prompt/                    # Prompt engineering
│   └── internet/                  # Internet connectivity
├── pyproject.toml                 # Project configuration and dependencies
└── main.py                        # Entry point (if needed)
```

### 2.3 Key Design Patterns

- **Dependency Injection**: FastAPI's built-in DI for services and database sessions
- **Repository Pattern**: Services abstract data access
- **Schema Separation**: Separate Pydantic schemas for request/response
- **Layered Architecture**: API → Services → Models → Database

### 2.4 Database Strategy

**Development**: SQLite for simplicity
**Production**: PostgreSQL for scalability

Migration strategy:
- Use SQLModel's built-in migration support
- Alembic for complex migrations (future)

---

## 3. Frontend Architecture

### 3.1 Technology Stack

- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build Tool**: Vite 5+
- **State Management**: Zustand or React Context (TBD)
- **HTTP Client**: Axios or Fetch API
- **Styling**: CSS Modules or Tailwind CSS (TBD)

### 3.2 Directory Structure

```
frontend/
├── src/
│   ├── main.tsx                   # Application entry
│   ├── App.tsx                    # Root component
│   ├── vite-env.d.ts
│   ├── components/                # Reusable UI components
│   │   ├── common/
│   │   └── layout/
│   ├── pages/                     # Page components
│   ├── hooks/                     # Custom React hooks
│   ├── services/                  # API service layer
│   ├── stores/                    # State management
│   ├── types/                     # TypeScript types
│   ├── utils/                     # Utility functions
│   └── styles/                    # Global styles
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

### 3.3 Key Features

- Type-safe API client generation
- Responsive design
- Component library
- Error boundaries
- Loading states
- Authentication flow (future)

---

## 4. Browser Extension Architecture

### 4.1 Technology Stack

- **Manifest Version**: 3 (latest standard)
- **Background**: Service Worker (JavaScript)
- **Content Scripts**: Vanilla JavaScript
- **Popup**: HTML + CSS + JavaScript
- **Storage**: Chrome Storage API

### 4.2 Directory Structure

```
extension/
├── manifest.json                  # Extension configuration
├── assets/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
├── background/
│   └── main.js                    # Service worker
├── content/
│   └── main.js                    # Content script
├── popup/
│   ├── index.html                 # Popup UI
│   ├── popup.js                   # Popup logic
│   └── popup.css                  # Popup styles
└── options/
    └── options.html               # Options page (future)
```

### 4.3 Core Features

- **Background Service Worker**: Persistent background tasks
- **Content Scripts**: DOM interaction and page analysis
- **Popup UI**: Quick access to extension features
- **Storage**: Persistent settings and data
- **Messaging**: Communication between components

### 4.4 Security Considerations

- Minimal permissions (storage, activeTab)
- No inline scripts (CSP compliant)
- Secure message passing
- Input validation
- No sensitive data in logs

---

## 5. Shared Components

### 5.1 Purpose

Shared code between backend, frontend, and extension:

- Type definitions
- API contracts
- Validation schemas
- Constants and enums

### 5.2 Structure

```
shared/
├── types/
│   ├── api.ts                     # API type definitions
│   ├── models.ts                  # Shared data models
│   └── index.ts
├── constants/
│   ├── api.ts                     # API endpoints
│   └── config.ts                  # Configuration constants
└── index.ts                       # Main export
```

---

## 6. Development Workflow

### 6.1 Backend Development

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
cp ../.env.example .env

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black app/
ruff check app/
```

### 6.2 Frontend Development

```bash
# Setup
cd frontend
npm create vite@latest . -- --template react-ts
npm install

# Run development server
npm run dev

# Build
npm run build

# Preview
npm run preview
```

### 6.3 Extension Development

```bash
# Load in Chrome
1. Open chrome://extensions/
2. Enable Developer mode
3. Click "Load unpacked"
4. Select extension/ directory

# Debug
- Background: chrome://extensions/ → Service Worker link
- Content: Browser console on any page
- Popup: Right-click popup → Inspect
```

---

## 7. API Design

### 7.1 Base URL

```
/api/v1
```

### 7.2 Standard Endpoints

```
GET    /health              # Health check
GET    /api/v1/users        # List users
POST   /api/v1/users        # Create user
GET    /api/v1/users/{id}   # Get user
PUT    /api/v1/users/{id}   # Update user
DELETE /api/v1/users/{id}   # Delete user
```

### 7.3 Response Format

```json
{
  "success": true,
  "data": {},
  "message": "Optional message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 7.4 Error Format

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 8. Database Schema

### 8.1 Base Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 8.2 Example: User Model

```python
class User(BaseModel, table=True):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
```

---

## 9. Security

### 9.1 Authentication

- JWT tokens (future implementation)
- API keys for extension (future)
- OAuth2 integration (future)

### 9.2 Best Practices

- Environment variables for secrets
- CORS configuration
- Rate limiting (future)
- Input validation
- SQL injection prevention (SQLModel handles this)
- XSS prevention
- CSRF protection

---

## 10. Testing Strategy

### 10.1 Backend Tests

- **Unit Tests**: Services, utilities
- **Integration Tests**: API endpoints
- **Database Tests**: Model operations
- **Coverage Target**: 80%+

### 10.2 Extension Tests

- Manual testing in Chrome
- Automated UI tests (future)
- Message passing tests

### 10.3 Frontend Tests

- Component tests (future)
- Integration tests (future)
- E2E tests (future)

---

## 11. Deployment

### 11.1 Backend

- **Development**: Uvicorn with --reload
- **Production**: Gunicorn + Uvicorn workers
- **Containerization**: Docker (future)
- **Orchestration**: Docker Compose (future)

### 11.2 Frontend

- **Build**: Vite production build
- **Hosting**: Static file server or CDN
- **CI/CD**: GitHub Actions (future)

### 11.3 Extension

- **Development**: Load unpacked
- **Production**: Chrome Web Store (future)
- **Versioning**: Semantic versioning

---

## 12. Monitoring & Logging

### 12.1 Backend

- Structured logging with structlog (future)
- Request/response logging
- Error tracking (future)
- Performance metrics (future)

### 12.2 Extension

- Console logging (development)
- Error reporting (future)
- Usage analytics (future, with consent)

---

## 13. Future Enhancements

### Phase 2

- [ ] PostgreSQL migration
- [ ] User authentication & authorization
- [ ] React frontend implementation
- [ ] Advanced extension features
- [ ] WebSocket support
- [ ] Caching layer (Redis)

### Phase 3

- [ ] AI/ML integration
- [ ] Advanced learning modules
- [ ] Cloud deployment
- [ ] CI/CD pipeline
- [ ] Comprehensive testing suite
- [ ] Performance optimization

---

## 14. Technical Decisions

### 14.1 Why FastAPI?

- Modern, fast, and async
- Automatic OpenAPI documentation
- Type hints and validation
- Easy to learn and use

### 14.2 Why SQLModel?

- Combines SQLAlchemy and Pydantic
- Type safety
- Easy migrations
- Great FastAPI integration

### 14.3 Why Manifest V3?

- Latest Chrome standard
- Better security
- Service workers instead of background pages
- Future-proof

### 14.4 Why SQLite?

- Zero configuration
- Perfect for development
- Easy to migrate to PostgreSQL
- Lightweight

---

## 15. Dependencies

### 15.1 Backend Core

Dependencies are managed in `backend/pyproject.toml`:

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlmodel>=0.0.16
pydantic-settings>=2.2.1
python-dotenv>=1.0.1
```

### 15.2 Backend Development (Optional)

Development dependencies (also in pyproject.toml):

```
pytest>=8.0.0
pytest-asyncio>=0.23.0
black>=24.0.0
ruff>=0.3.0
```

### 15.3 Frontend (TBD)

```
react>=18.0.0
typescript>=5.0.0
vite>=5.0.0
```

---

## 16. Contributing Guidelines

### Code Style

- **Python**: Black formatter, Ruff linter
- **JavaScript**: ESLint, Prettier
- **TypeScript**: Strict mode enabled

### Commit Messages

Follow conventional commits:
- `feat: add user authentication`
- `fix: resolve database connection issue`
- `docs: update API documentation`
- `refactor: simplify user service logic`

### Pull Request Process

1. Create feature branch from `main`
2. Implement changes with tests
3. Update documentation
4. Submit PR with description
5. Code review
6. Merge after approval

---

## 17. License

[Specify license - MIT, Apache 2.0, etc.]

---

## 18. Contact & Support

[Add contact information or support channels]

---

## Appendix

### A. Glossary

- **SQLModel**: SQL database library for Python, built on SQLAlchemy and Pydantic
- **Manifest V3**: Chrome's extension platform standard
- **Service Worker**: Background script for Chrome extensions
- **Pydantic**: Data validation library for Python

### B. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [Vite Documentation](https://vitejs.dev/)

### C. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2024-01-01 | Initial foundation blueprint |

---

**Document Status**: Draft  
**Last Updated**: 2024-01-01  
**Maintained By**: Project-X Team