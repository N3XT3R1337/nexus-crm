<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=280&section=header&text=Nexus%20CRM&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Enterprise%20Customer%20Relationship%20Management&descSize=20&descAlignY=55&descColor=b8b8ff" width="100%"/>

<a href="#">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=28&duration=3000&pause=1000&color=9D4EDD&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=80&lines=Nexus+CRM+%E2%80%94+Manage+Relationships%2C+Close+Deals;Pipeline+Analytics+%7C+RBAC+%7C+Real-time+Updates" alt="Typing SVG" />
</a>

<br/>
<br/>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

<table>
<tr>
<td align="center"><b>60+</b><br/>API Endpoints</td>
<td align="center"><b>15</b><br/>Data Models</td>
<td align="center"><b>40+</b><br/>Vue Components</td>
<td align="center"><b>75</b><br/>Passing Tests</td>
<td align="center"><b>5</b><br/>RBAC Roles</td>
<td align="center"><b>50+</b><br/>Permissions</td>
</tr>
</table>

</div>

---

## Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Overview](#-api-overview)
- [Role-Based Access Control](#-role-based-access-control)
- [Screenshots](#-screenshots)
- [License](#-license)

---

## Features

<table>
<tr>
<td width="50%" valign="top">

<h3>Backend Capabilities</h3>

<ul>
<li><b>JWT Authentication</b> with access + refresh tokens</li>
<li><b>RBAC</b> with 5 roles and 50+ granular permissions</li>
<li><b>Deal Pipeline Engine</b> with stage transitions, win/lose tracking</li>
<li><b>Full-Text Search</b> across contacts, companies, deals</li>
<li><b>Analytics Dashboard</b> — revenue forecasts, conversion rates, pipeline velocity</li>
<li><b>Audit Logging</b> for complete change tracking</li>
<li><b>Webhook System</b> with event subscriptions and retry logic</li>
<li><b>Email Templates</b> per user and organization</li>
<li><b>API Key Management</b> with expiration</li>
<li><b>Celery Task Queue</b> for async email and webhook dispatch</li>
<li><b>WebSocket</b> real-time notifications</li>
<li><b>Multi-tenant</b> organization isolation</li>
</ul>

</td>
<td width="50%" valign="top">

<h3>Frontend Experience</h3>

<ul>
<li><b>DataTable</b> with sort, filter, paginate, bulk actions</li>
<li><b>Kanban Board</b> with drag-and-drop deal pipeline</li>
<li><b>Contact & Deal Cards</b> with inline editing</li>
<li><b>Activity Timeline</b> for tracking interactions</li>
<li><b>Charts</b> — revenue, pipeline, conversion via Chart.js</li>
<li><b>Global Search</b> with instant results (Alt+S)</li>
<li><b>Form Builder</b> for dynamic forms</li>
<li><b>Tag Input</b>, <b>Date Range Picker</b>, <b>Rich Text Editor</b></li>
<li><b>Notification Bell</b> with real-time WebSocket updates</li>
<li><b>Dark / Light Theme</b> toggle</li>
<li><b>Responsive Layout</b> with sidebar navigation</li>
<li><b>Keyboard Shortcuts</b> for power users</li>
</ul>

</td>
</tr>
</table>

---

## Architecture

<details>
<summary><b>System Architecture Diagram</b></summary>
<br/>

```mermaid
graph TB
    subgraph Frontend["Frontend — Vue 3 + TypeScript"]
        UI[Vue Components]
        Pinia[Pinia Stores]
        Router[Vue Router]
        WS_Client[WebSocket Client]
    end

    subgraph Backend["Backend — FastAPI"]
        API[REST API v1]
        Auth[JWT Auth + RBAC]
        Services[Business Logic]
        Pipeline[Deal Pipeline Engine]
        Search[Full-Text Search]
        Analytics[Analytics Engine]
        WS_Server[WebSocket Manager]
    end

    subgraph Workers["Async Workers"]
        Celery[Celery Workers]
        EmailTask[Email Tasks]
        WebhookTask[Webhook Dispatch]
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL 16)]
        Redis[(Redis 7)]
    end

    UI --> Pinia
    Pinia --> API
    WS_Client --> WS_Server
    Router --> UI

    API --> Auth
    Auth --> Services
    Services --> Pipeline
    Services --> Search
    Services --> Analytics
    Services --> PG

    Celery --> EmailTask
    Celery --> WebhookTask
    Celery --> Redis
    Celery --> PG

    WS_Server --> Redis

    style Frontend fill:#42b883,color:#fff
    style Backend fill:#009688,color:#fff
    style Workers fill:#ff6f00,color:#fff
    style Data fill:#1565c0,color:#fff
```

</details>

---

## Tech Stack

<div align="center">

### Backend
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)

### Frontend
[![Vue.js](https://img.shields.io/badge/Vue.js_3-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black)](https://pinia.vuejs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://chartjs.org)

### Infrastructure
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org)

</div>

---

## Quick Start

### Docker (recommended)

```bash
git clone https://github.com/N3XT3R1337/nexus-crm.git && cd nexus-crm
cp .env.example .env
docker compose up -d
```

The app will be available at `http://localhost:3000` with the API at `http://localhost:8000`.

### Local Development

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in a new terminal)
cd frontend && npm install && npm run dev
```

### Seed Data

```bash
make seed    # Generates 500 contacts, 200 companies, 100 deals
```

---

## Project Structure

```
nexus-crm/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Auth dependencies & permission checks
│   │   │   └── v1/                   # API v1 endpoints
│   │   │       ├── auth.py           #   Registration, login, token refresh
│   │   │       ├── contacts.py       #   Contact CRUD + bulk actions
│   │   │       ├── companies.py      #   Company management
│   │   │       ├── deals.py          #   Deal pipeline & transitions
│   │   │       ├── activities.py     #   Activity tracking
│   │   │       ├── notes.py          #   Notes on contacts/deals
│   │   │       ├── tags.py           #   Tag management
│   │   │       ├── users.py          #   User administration
│   │   │       ├── email_templates.py#   Email template CRUD
│   │   │       ├── notifications.py  #   Notification management
│   │   │       ├── webhooks.py       #   Webhook subscriptions
│   │   │       ├── reports.py        #   Analytics & reports
│   │   │       ├── search.py         #   Full-text search
│   │   │       └── dashboard.py      #   Dashboard statistics
│   │   ├── core/
│   │   │   ├── security.py           # JWT, password hashing
│   │   │   ├── rbac.py               # Role-based access control
│   │   │   └── websocket.py          # WebSocket connection manager
│   │   ├── models/                   # 15 SQLAlchemy models
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/                 # Business logic layer
│   │   │   ├── auth.py               #   Authentication service
│   │   │   ├── analytics.py          #   Dashboard & reporting
│   │   │   ├── deal_pipeline.py      #   Pipeline stage transitions
│   │   │   ├── search.py             #   Full-text search service
│   │   │   ├── notification.py       #   Notification dispatch
│   │   │   └── webhook.py            #   Webhook event handling
│   │   ├── tasks/                    # Celery async tasks
│   │   ├── config.py                 # Application settings
│   │   ├── database.py               # SQLAlchemy engine & session
│   │   ├── main.py                   # FastAPI application entry
│   │   └── seed.py                   # Sample data generator
│   ├── tests/                        # 75 pytest tests
│   ├── alembic/                      # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.ts             # Axios instance with interceptors
│   │   ├── components/               # 40+ Vue components
│   │   │   ├── common/               #   DataTable, Modal, SearchBar, etc.
│   │   │   ├── dashboard/            #   StatsCard, Charts
│   │   │   ├── deals/                #   KanbanBoard, DealCard
│   │   │   ├── contacts/             #   ContactCard
│   │   │   ├── activities/           #   ActivityTimeline
│   │   │   ├── layout/               #   Sidebar, TopBar
│   │   │   └── notifications/        #   NotificationBell
│   │   ├── views/                    # 15+ page views
│   │   ├── stores/                   # 5 Pinia stores
│   │   ├── composables/              # useTheme, useKeyboardShortcuts, useWebSocket
│   │   ├── types/                    # TypeScript interfaces
│   │   ├── router/                   # Vue Router configuration
│   │   └── main.ts
│   ├── Dockerfile
│   ├── vite.config.ts
│   └── package.json
├── docker-compose.yml                # PostgreSQL + Redis + Backend + Celery + Frontend
├── Makefile                          # Development commands
├── .env.example
├── .editorconfig
├── .gitignore
└── LICENSE
```

---

## API Overview

| Module | Endpoints | Description |
|--------|-----------|-------------|
| **Auth** | `POST /register` `POST /login` `POST /refresh` `GET /me` `PUT /me` `POST /change-password` | Authentication & profile |
| **Contacts** | `GET` `POST` `PUT` `DELETE` + `/bulk` `/activities` `/deals` `/notes` | Contact management with relationships |
| **Companies** | `GET` `POST` `PUT` `DELETE` + `/contacts` `/deals` | Company management |
| **Deals** | `GET` `POST` `PUT` `DELETE` + `/stages` `/transition` `/win` `/lose` `/pipeline` | Deal pipeline engine |
| **Activities** | `GET` `POST` `PUT` `DELETE` + `/complete` | Activity tracking (calls, emails, meetings) |
| **Notes** | `GET` `POST` `PUT` `DELETE` | Notes on contacts, deals, companies |
| **Tags** | `GET` `POST` `PUT` `DELETE` | Color-coded tag system |
| **Users** | `GET` `POST` `PUT` `DELETE` | User administration |
| **Email Templates** | `GET` `POST` `PUT` `DELETE` | Reusable email templates |
| **Notifications** | `GET` `PUT /read` `PUT /read-all` `DELETE` | Notification management |
| **Webhooks** | `GET` `POST` `PUT` `DELETE` | Event-driven webhook subscriptions |
| **Reports** | `GET /revenue-forecast` `/pipeline-velocity` `/conversion-rates` | Analytics & reporting |
| **Search** | `GET /search?q=` | Cross-entity full-text search |
| **Dashboard** | `GET /stats` `/pipeline-summary` `/deal-value-by-month` `/contacts-by-source` | Dashboard analytics |

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI).

---

## Role-Based Access Control

| Permission | Viewer | Sales Rep | Manager | Admin | Super Admin |
|:-----------|:------:|:---------:|:-------:|:-----:|:-----------:|
| View contacts/deals | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create/edit contacts | ❌ | ✅ | ✅ | ✅ | ✅ |
| Delete contacts | ❌ | ❌ | ✅ | ✅ | ✅ |
| Transition deal stages | ❌ | ✅ | ✅ | ✅ | ✅ |
| Manage users | ❌ | ❌ | 👀 | ✅ | ✅ |
| Delete users | ❌ | ❌ | ❌ | ❌ | ✅ |
| System settings | ❌ | ❌ | ❌ | ✅ | ✅ |
| Audit logs | ❌ | ❌ | ❌ | ✅ | ✅ |

---

## Screenshots

<div align="center">

| Dashboard | Pipeline |
|:---------:|:--------:|
| Revenue charts, stats cards, activity feed | Kanban board with drag-and-drop stages |

| Contacts | Deal Detail |
|:--------:|:-----------:|
| DataTable with filters, search, bulk actions | Timeline, notes, stage history |

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=120&section=footer" width="100%"/>

Built with ❤️ by **panaceya** | [github.com/N3XT3R1337](https://github.com/N3XT3R1337)

</div>
