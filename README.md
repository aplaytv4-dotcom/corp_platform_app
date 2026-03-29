# Attendance Backend

Modular Django + DRF backend for employee attendance accounting.

## Stack

- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL

## Apps

- `common`
- `accounts`
- `organization`
- `staff`
- `attendance`

## Run

1. Create a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust PostgreSQL settings.
4. Run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Start the server:

```powershell
python manage.py runserver
```
