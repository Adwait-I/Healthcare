# 🏥 Healthcare Management Backend API

A complete, production-structured backend system for a healthcare application built with **Python 3.11**, **Django 5**, **Django REST Framework (DRF)**, and **PostgreSQL**, secured with **JWT authentication** via `djangorestframework-simplejwt`.

---

## 🚀 Features

- **🔐 Custom Email-Based Authentication**: Secure registration and login using email (no username), strict password complexity, and JWT access/refresh token rotation.
- **🏥 Patient Management**: Secure CRUD for patient records, strictly scoped so authenticated users only view and manage patients they created.
- **👨‍⚕️ Doctor Directory**: Complete CRUD for doctors, including specialization, years of experience, unique license numbers, and consultation fees.
- **🔗 Patient-Doctor Mappings**: Assign doctors to patients with clinical notes and database-level unique constraints preventing duplicate assignments.
- **🛡️ Predictable Error Handling**: Custom global DRF exception handler returning structured `{success, status_code, error, detail}` envelopes without leaking server stack traces.
- **🐘 PostgreSQL Integration**: Configured for high-performance relational storage using `psycopg2-binary`.
- **🧪 Comprehensive Test Suite**: 50 automated unit & integration tests covering auth, permissions, ownership filtering, mapping logic, and validation error cases.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Framework:** Django 5.0.6
- **API Engine:** Django REST Framework 3.15.2
- **Authentication:** `djangorestframework-simplejwt`
- **Database:** PostgreSQL (with `psycopg2-binary`)
- **Environment Configuration:** `python-decouple`
- **CORS:** `django-cors-headers`

---

## 📁 Project Architecture

```
byte/
├── healthcare_project/       # Project configuration
│   ├── settings.py           # 100% env-driven configuration
│   ├── urls.py               # Root URL router & API directory
│   ├── wsgi.py
│   └── __init__.py
├── accounts/                 # Custom User model & JWT auth
├── patients/                 # Patient management (owner-scoped)
├── doctors/                  # Doctor directory
├── mappings/                 # Patient-Doctor mapping & assignments
├── core/                     # Global exception handler & utilities
├── tests/                    # 50 unit and integration tests
├── .env.example              # Template for environment variables
├── requirements.txt          # Python dependencies
├── manage.py
└── README.md
```

---

## ⚙️ Quick Start & Setup

### 1. Prerequisites
- **Python 3.11** installed (`python3.11 --version`)
- **PostgreSQL** running locally or remotely

### 2. Clone and Setup Environment
```bash
git clone <your-repository-url>
cd <repository-folder>

# Create Python 3.11 virtual environment
python3.11 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Edit `.env` with your PostgreSQL credentials:
```ini
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 4. Create the Database & Run Migrations
```bash
# In PostgreSQL (psql):
# CREATE DATABASE healthcare_db;

# Apply Django migrations
python manage.py migrate
```

### 5. Create Admin Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver 8080
```
- **API Directory & Documentation:** [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
- **Admin Dashboard:** [http://127.0.0.1:8080/admin/](http://127.0.0.1:8080/admin/)

---

## 🧪 Running Automated Tests

Run the full suite of 50 unit and integration tests:
```bash
python manage.py test tests --verbosity=2
```

---

## 📡 API Endpoints Reference

All protected endpoints require the header:
```http
Authorization: Bearer <your_access_token>
```

### 1. Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/auth/register/` | Register user (`name`, `email`, `password`) | No |
| `POST` | `/api/auth/login/` | Log in and receive access & refresh tokens | No |
| `POST` | `/api/auth/token/refresh/` | Refresh expired access token | No |

### 2. Patient Management
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/api/patients/` | List own patients (`created_by=request.user`) | Yes |
| `POST` | `/api/patients/` | Create a new patient | Yes |
| `GET` | `/api/patients/<id>/` | Retrieve specific patient details | Yes |
| `PUT` | `/api/patients/<id>/` | Full update of patient record | Yes |
| `PATCH` | `/api/patients/<id>/` | Partial update of patient record | Yes |
| `DELETE` | `/api/patients/<id>/` | Delete patient record | Yes |

### 3. Doctor Management
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/api/doctors/` | List all doctors in directory | Yes |
| `POST` | `/api/doctors/` | Add a new doctor (unique license validation) | Yes |
| `GET` | `/api/doctors/<id>/` | Retrieve specific doctor profile | Yes |
| `PUT` | `/api/doctors/<id>/` | Full update of doctor profile | Yes |
| `PATCH` | `/api/doctors/<id>/` | Partial update of doctor profile | Yes |
| `DELETE` | `/api/doctors/<id>/` | Remove doctor record | Yes |

### 4. Patient-Doctor Mappings
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/api/mappings/` | List all patient-doctor assignments | Yes |
| `POST` | `/api/mappings/` | Assign doctor to patient (`patient`, `doctor`, `notes`) | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/delete/<id>/` | Remove assignment by mapping ID | Yes |

---

## 🛡️ Consistent Error Response Format

When validation fails or errors occur, the API always responds with a standardized JSON envelope:
```json
{
  "success": false,
  "status_code": 400,
  "error": "Bad Request",
  "detail": {
    "phone_number": [
      "Phone number must have 7–15 digits."
    ]
  }
}
```

---

## 📜 License
This project is licensed under the MIT License.
