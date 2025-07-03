# Tilit Book

A little "pet" project web application where users can view, comment, and upload images of my cat, Tilit! This full-stack application features image uploads, real-time commenting, and a modern, responsive interface.

## Technology Stack

### Frontend
- **React 19** with TypeScript
- **Vite** for fast development and building
- **React Router** for navigation
- **React Hook Form** for form handling
- **Axios** for API communication
- **Tailwind CSS** for styling

### Backend
- **FastAPI** for the REST API
- **SQLAlchemy** for database ORM
- **PostgreSQL** for data storage
- **AWS S3** for image storage
- **Pydantic** for data validation

### DevOps
- **Docker** and **Docker Compose** for containerization
- **Alembic** for database migrations

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) (if running frontend locally)
- [Python 3.10+](https://www.python.org/downloads/) (if running backend locally)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tilit_book
   ```

2. **Set up environment variables**
   Example .env:
   ```
   DB_HOST="db"
   DB_PORT=5432
   POSTGRES_DB=""
   POSTGRES_USER=""
   POSTGRES_PASSWORD=""
   AWS_ACCESS_KEY_ID=""
   AWS_SECRET_ACCESS_KEY=""
   AWS_S3_BUCKET_NAME=""
   ```

3. **Start the application with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
