# Bidii Quality Builders

A Django-based construction/service management system for handling customers, estimates, jobs, invoices, and dashboard reporting.

## Project Overview

Bidii Quality Builders helps organize a basic business workflow:

1. Register and manage customers.
2. Create estimates for customer work.
3. Accept estimates and automatically create jobs.
4. Generate and track invoices.
5. View operational and revenue insights on a dashboard.

## Tech Stack

- Python 3
- Django 6.0.3
- PostgreSQL (configured in settings for hosted DB usage, e.g., Supabase)
- Tailwind CSS via `django-tailwind`
- Matplotlib for dashboard chart rendering

## Installed Django Apps

- `customer` - Customer records and customer creation/list views
- `estimates` - Estimate model and estimate acceptance flow
- `jobs` - Job model linked to accepted estimates
- `invoices` - Invoice model linked to jobs
- `dashboard` - Home dashboard with summary metrics and charts
- `theme` - Tailwind integration app

## Current URL Routing

- `/admin/` - Django admin
- `/customers/` - Customer app routes
- `/` - Dashboard home
- `/__reload__/` - Browser reload endpoint in development

## Data Model Summary

- `Customer`
  - name, email, phone_number, address
- `Estimate`
  - customer, description, visit_date, estimated_cost, status (`pending`, `accepted`, `rejected`)
- `Job`
  - one-to-one with estimate, start_date, end_date, status (`scheduled`, `ongoing`, `completed`)
- `Invoice`
  - one-to-one with job, total_amount, issued_date, due_date, paid

## Important Workflow Logic

When an estimate is accepted (`estimates/services.py`):

- Estimate status is changed to `accepted`.
- A linked job is automatically created with:
  - `start_date = estimate.visit_date`
  - `status = scheduled`

## Prerequisites

- Python 3.11+ recommended
- PostgreSQL database
- Node.js + npm (required by Tailwind tooling)

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432
```

## Local Setup

### 1. Clone and enter the project

```bash
git clone <your-repository-url>
cd bidii
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv bidii_env
.\bidii_env\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv bidii_env
source bidii_env/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Start development server

```bash
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Tailwind (Theme App)

This project includes `django-tailwind` and `theme` in installed apps.

Common commands (run after environment setup):

```bash
python manage.py tailwind install
python manage.py tailwind start
```

If your Node/npm path differs, update `NPM_BIN_PATH` in settings.

## Useful Django Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
```

## Project Structure (High Level)

```text
bidii_quality_builders/   # Django project settings and root URLs
customer/                 # Customer module
estimates/                # Estimates and estimate acceptance logic
jobs/                     # Jobs domain model
invoices/                 # Invoices domain model
dashboard/                # Dashboard views and chart logic
materials/
payments/
theme/                    # Tailwind theme app
templates/                # Global templates
requirements.txt          # Python dependencies
manage.py                 # Django management entry point
```

## Notes

- The database engine is configured for PostgreSQL in project settings.
- `django-browser-reload` is enabled when `DEBUG=True`.
- `materials` and `payments` apps currently contain scaffolding and can be expanded as new features are added.
