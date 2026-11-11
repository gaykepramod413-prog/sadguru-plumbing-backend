# 🔧 Sadguru Plumbing — Backend

<div align="center">

**A Flask and MySQL backend for managing plumbing materials and generating material requirement PDFs.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![PDF](https://img.shields.io/badge/PDF-ReportLab-B30B00?style=flat-square)

</div>

## 📌 Overview

Sadguru Plumbing Backend provides REST endpoints for a plumbing materials workflow. It stores material names, categories, available sizes, and units in MySQL, and creates a downloadable PDF list for a selected job.

## ✨ Features

- Retrieve all materials, ordered by category and name.
- Retrieve the available material categories.
- Add a material with its category, sizes, and unit.
- Delete a material by its ID.
- Generate an A4 PDF material requirement list.
- Include customer and site details in the generated PDF.
- Configure the database using environment variables.

## 🧰 Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **Database:** MySQL
- **PDF generation:** ReportLab
- **Deployment support:** Gunicorn-compatible Flask application

## 📁 Project Structure

```text
sadguru-plumbing-backend/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

## ⚙️ Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/gaykepramod413-prog/sadguru-plumbing-backend.git
   cd sadguru-plumbing-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your MySQL connection using environment variables.

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

   The application runs on port `3000` by default (or the platform-provided `PORT`). On direct startup, it creates the `materials` table if it does not already exist.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/api/materials` | List materials |
| GET | `/api/materials/categories` | List material categories |
| POST | `/api/materials` | Add a material |
| DELETE | `/api/materials/{id}` | Delete a material |
| POST | `/api/pdf/generate` | Generate a PDF material list |

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

### Generate a material list

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

The response is a downloadable PDF file named `material-list.pdf`.

## 🗄️ Database

The backend creates the following table on direct application startup:

| Column | Type | Description |
|---|---|---|
| id | INT, primary key | Auto-increment ID |
| name | VARCHAR(150) | Material name |
| category | VARCHAR(100) | Material category |
| sizes | VARCHAR(255) | Comma-separated sizes |
| unit | VARCHAR(30) | Measurement unit |

## 🔐 Security Notes

- Store database credentials only in environment variables or your hosting provider's secret settings.
- Do not commit passwords, API keys, or production connection strings.
- Rotate any credential that has previously been committed to a public repository.
- Use production-safe settings when deploying.

## 🗺️ Possible Improvements

- Add update-material and search endpoints.
- Add input validation and authentication for management operations.
- Add automated API and database tests.
- Add pagination for larger material lists.

---

<div align="center">

**Built by [Pramod Gayke](https://github.com/gaykepramod413-prog)**

</div>
