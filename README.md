# 🔧 Sadguru Plumbing Backend

<div align="center">

**A Flask and MySQL REST backend for plumbing-material management and PDF requirement lists.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-B30B00?style=flat-square)

</div>

## Overview

Sadguru Plumbing Backend provides REST endpoints for a plumbing-material workflow. It stores material names, categories, available sizes and units in MySQL, and generates a downloadable PDF requirement list for a selected customer and site.

## Features

- Retrieve materials ordered by category and name.
- Retrieve distinct material categories.
- Add and delete material records.
- Generate an A4 PDF material requirement list.
- Include customer and site details in the generated document.
- Configure database connection settings through environment variables.

## Tech Stack

- **Language:** Python
- **Backend:** Flask, Flask-CORS
- **Database:** MySQL
- **PDF generation:** ReportLab
- **Deployment:** Gunicorn-compatible Flask application

## Request Flow

```text
Client / Frontend
      |
      v
Flask REST API
      |
      +---- GET /api/materials --------> MySQL SELECT
      |
      +---- POST /api/materials -------> MySQL INSERT
      |
      +---- DELETE /api/materials/id --> MySQL DELETE
      |
      +---- POST /api/pdf/generate ----> ReportLab PDF
                                           |
                                           v
                                      PDF download
```

## Project Structure

```text
sadguru-plumbing-backend/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

## Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/gaykepramod413-prog/sadguru-plumbing-backend.git
   cd sadguru-plumbing-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure database environment variables.

   **Windows PowerShell**
   ```powershell
   $env:DB_HOST = "localhost"
   $env:DB_PORT = "3306"
   $env:DB_USER = "your_mysql_user"
   $env:DB_PASSWORD = "your_mysql_password"
   $env:DB_NAME = "your_database"
   ```

   **macOS / Linux**
   ```bash
   export DB_HOST="localhost"
   export DB_PORT="3306"
   export DB_USER="your_mysql_user"
   export DB_PASSWORD="your_mysql_password"
   export DB_NAME="your_database"
   ```

5. Start the application:

   ```bash
   python app.py
   ```

The default port is `3000`, or the platform-provided `PORT`. Direct startup attempts to initialize the materials table.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/api/materials` | List materials |
| GET | `/api/materials/categories` | List categories |
| POST | `/api/materials` | Add a material |
| DELETE | `/api/materials/{id}` | Delete a material |
| POST | `/api/pdf/generate` | Generate a PDF list |

### Add a material

`POST /api/materials`

```json
{
  "name": "PVC Elbow",
  "category": "PVC Fittings",
  "sizes": "1/2 inch, 3/4 inch",
  "unit": "Pieces"
}
```

### Generate a PDF

`POST /api/pdf/generate`

```json
{
  "customerName": "Customer Name",
  "siteName": "Project Site",
  "items": [
    {
      "name": "PVC Elbow",
      "size": "1/2 inch",
      "unit": "Pieces",
      "quantity": 10
    }
  ]
}
```

The response is an A4 PDF attachment named `material-list.pdf`.

## Database

The application creates a `materials` table with:

| Column | Type | Purpose |
|---|---|---|
| id | INT, primary key | Auto-increment identifier |
| name | VARCHAR(150) | Material name |
| category | VARCHAR(100) | Material category |
| sizes | VARCHAR(255) | Comma-separated sizes |
| unit | VARCHAR(30) | Measurement unit |

## Security & Production Notes

- Database credentials are read from environment variables.
- SQL statements use parameterized values for material insertion and deletion.
- **Current limitation:** the listed management endpoints do not implement user authentication or role-based authorization.
- Add authentication, authorization, input validation, pagination and rate limiting before exposing management operations publicly.
- Avoid returning raw database exception details to public clients; log sanitized diagnostics server-side.
- Use HTTPS and hosting-provider secret storage in production.
- Never commit passwords or production connection strings.

## Roadmap

- Add update and search material endpoints.
- Add administrator authentication and authorization.
- Add API/database automated tests.
- Add pagination and robust validation.
- Improve PDF handling for long names and multi-page lists.

## Interview Notes

**Why use MySQL?** The material records have structured fields and relationships that fit a relational database.

**Why use parameterized SQL?** It separates SQL commands from supplied values and helps prevent SQL injection.

**How is the PDF generated?** The API receives customer/site details and selected items, ReportLab draws the A4 document into an in-memory buffer, and Flask sends it as a downloadable attachment.

---

<div align="center">

**Built by [Pramod Gayke](https://github.com/gaykepramod413-prog)**

</div>
