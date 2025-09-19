# Project Setup Guide

This document provides a step-by-step guide to set up and run the project locally, including configuration of environment variables, database setup, and Google Cloud Storage integration.

---

## 1. Clone the Repository

```bash
git clone https://github.com/vm-palanhaar/tourism_backend.git
cd tourism_backend
```

---

## 2. Create Virtual Environment

It is recommended to use a virtual environment to isolate project dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Linux / macOS:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
DJANGO_SECRET_KEY=django-secret-key
DEBUG=True
# Database credentials
DB_PGSQL_NAME=database-name
DB_PGSQL_USER=postgres
DB_PGSQL_PWD=admin
DB_PGSQL_HOST=localhost
DB_PGSQL_PORT=5432
# Google Cloud Storage
GOOGLE_CLOUD_STORAGE_BUCKET
# Customer Service Email
EMAIL_CUSTOMER_SERVICE_MAIL
EMAIL_CUSTOMER_SERVICE_PWD
```

---

## 5. Setup Database (PostgreSQL)

Ensure PostgreSQL is installed and running. Create a database with the name specified in `.env`:

```sql
CREATE DATABASE database-name;
```

Then run Django migrations:

```bash
python manage.py migrate
```

---

## 6. Google Cloud Service Account Setup

This project requires a **Google Cloud Service Account** for accessing the storage bucket.

### Steps to Create `credentials.json`

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin → Service Accounts**.
3. Click **Create Service Account**.
4. Assign a name (e.g., `indrailsuperapp-service-account`).
5. Grant it the role **Storage Admin** (to access Cloud Storage).
6. After creating, go to the service account → **Keys** → **Add Key → Create new key**.
7. Select **JSON** → Download the file.
8. Save it in your project root as `credentials.json`.

⚠️ **Important:** Never commit `credentials.json` or `.env` to GitHub. Add them to `.gitignore`.

---

## 7. Run the Project

Finally, start the Django development server:

```bash
python manage.py runserver
```

Access the application at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 8. Additional Notes

- Keep `.env` and `credentials.json` private and secure.
- For production deployment, ensure `DEBUG=False`.
- Configure PostgreSQL user and password according to your local/production setup.
