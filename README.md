# High-Performance Data Table App

This project is a full-stack application featuring an ultra-fast data table capable of handling 100,000+ records with instant response times.

## Tech Stack
- Backend: FastAPI
- Frontend: Next.js (TypeScript)
- Database: PostgreSQL
- Cache: Redis
- Deployment: Docker Compose

## Features
- Ultra-fast API (<100ms) with Redis caching
- Full-text search, filtering, sorting, and pagination
- Virtualized scrolling frontend with React Virtual
- Responsive and intuitive UI
- Error handling and thoughtful loading states

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/haritsrhn/high-perf-data-table.git
   cd high-perf-data-table
2. Create a .env file based on .env.example.
3. Start the entire application:
    ```bash
    docker-compose up --build
4.	Access the app:
    - Frontend: http://localhost:3000
    - Backend API docs: http://localhost:8000/docs

## Performance Optimizations
- Redis caching to avoid repeated DB hits
- Query optimization with SQLAlchemy indexes and async sessions
- Virtualized frontend list rendering (smooth 100k+ scrolls)
- Pagination and lazy loading for large data sets

## Architecture Decisions
- Chose FastAPI for its async performance and automatic OpenAPI docs.
- Used SWR in frontend for intelligent caching and revalidation.
- Dockerized full stack for reproducibility and fast onboarding.

## UI/UX Considerations
- Kept loading states minimal but clear.
- Used virtual scrolling to avoid DOM bloat.
- Mobile-responsive layout with clean design system (planned to enhance using shadcn/ui).

## Reflection
If I had more time:
- I’d add server-side cursor-based pagination for even better scalability.
- I’d polish UI using TailwindCSS + shadcn components.
- I’d implement optimistic updates and infinite scrolling for a seamless UX.