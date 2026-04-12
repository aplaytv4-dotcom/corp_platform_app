# Technical Specification For Developers

## 1. Project Purpose

The project is a corporate attendance platform for managing:

- users and access scopes
- managements and departments
- staff positions and staff units
- employees and assignments
- daily attendance sheets
- absence reasons
- daily and summary attendance reports
- administrative maintenance tasks

The system consists of:

- Django + Django REST Framework backend
- Vue 3 + Vite frontend
- PostgreSQL database

The goal of this document is to let a developer:

- understand the project structure quickly
- run the project locally
- understand the main business entities
- understand the backend and frontend responsibilities
- extend the system safely
- implement new features without guessing the architecture

## 2. Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL
- python-docx
- reportlab

### Frontend

- Vue 3
- Vite
- Pinia
- Vue Router
- Vue I18n
- Axios

## 3. Root Directory Structure

```text
corp_platform_app/
  accounts/
  attendance/
  common/
  config/
  frontend/
  organization/
  staff/
  templates/
  .venv/
  manage.py
  requirements.txt
  README.md
  PROJECT_DESCRIPTION.md
  TECHNICAL_SPEC.md
  log.txt
  start_project.ps1
```

## 4. Backend App Responsibilities

### `config`

Global Django configuration:

- settings
- root URLs
- WSGI and ASGI entry points

Important files:

- [config/settings.py](/abs/path/c:/corp_platform_app/config/settings.py:1)
- [config/urls.py](/abs/path/c:/corp_platform_app/config/urls.py:1)

### `accounts`

Responsible for:

- custom user model
- roles and access scopes
- authentication endpoints
- profile data
- password change
- user CRUD

Important files:

- [accounts/models.py](/abs/path/c:/corp_platform_app/accounts/models.py:1)
- [accounts/views.py](/abs/path/c:/corp_platform_app/accounts/views.py:1)
- [accounts/serializers.py](/abs/path/c:/corp_platform_app/accounts/serializers.py:1)
- [accounts/auth_urls.py](/abs/path/c:/corp_platform_app/accounts/auth_urls.py:1)
- [accounts/urls.py](/abs/path/c:/corp_platform_app/accounts/urls.py:1)

### `organization`

Responsible for:

- managements
- departments
- filtering visible structure by user scope

Important files:

- [organization/models.py](/abs/path/c:/corp_platform_app/organization/models.py:1)
- [organization/views.py](/abs/path/c:/corp_platform_app/organization/views.py:1)
- [organization/selectors.py](/abs/path/c:/corp_platform_app/organization/selectors.py:1)
- [organization/urls.py](/abs/path/c:/corp_platform_app/organization/urls.py:1)

### `staff`

Responsible for:

- positions
- staff units
- employees
- employee assignments
- querying current assignments by date and department

Important files:

- [staff/models.py](/abs/path/c:/corp_platform_app/staff/models.py:1)
- [staff/views.py](/abs/path/c:/corp_platform_app/staff/views.py:1)
- [staff/selectors.py](/abs/path/c:/corp_platform_app/staff/selectors.py:1)
- [staff/services.py](/abs/path/c:/corp_platform_app/staff/services.py:1)
- [staff/urls.py](/abs/path/c:/corp_platform_app/staff/urls.py:1)

### `attendance`

Responsible for:

- absence reasons
- attendance sheets
- sheet items
- open or create daily sheet workflow
- bulk update attendance items
- HTML, DOCX, and PDF reports
- summary report by period

Important files:

- [attendance/models.py](/abs/path/c:/corp_platform_app/attendance/models.py:1)
- [attendance/views.py](/abs/path/c:/corp_platform_app/attendance/views.py:1)
- [attendance/selectors.py](/abs/path/c:/corp_platform_app/attendance/selectors.py:1)
- [attendance/services.py](/abs/path/c:/corp_platform_app/attendance/services.py:1)
- [attendance/serializers.py](/abs/path/c:/corp_platform_app/attendance/serializers.py:1)
- [attendance/urls.py](/abs/path/c:/corp_platform_app/attendance/urls.py:1)
- [attendance/tests.py](/abs/path/c:/corp_platform_app/attendance/tests.py:1)

### `common`

Responsible for:

- shared timestamped model base class
- permissions helpers
- UTF-8 renderer
- report generation helpers
- health endpoint
- utility services
- admin utilities and backup related functionality

Important files:

- [common/models.py](/abs/path/c:/corp_platform_app/common/models.py:1)
- [common/permissions.py](/abs/path/c:/corp_platform_app/common/permissions.py:1)
- [common/renderers.py](/abs/path/c:/corp_platform_app/common/renderers.py:1)
- [common/services.py](/abs/path/c:/corp_platform_app/common/services.py:1)
- [common/views.py](/abs/path/c:/corp_platform_app/common/views.py:1)
- [common/urls.py](/abs/path/c:/corp_platform_app/common/urls.py:1)

## 5. Frontend Structure

Main frontend root:

- [frontend/src/main.js](/abs/path/c:/corp_platform_app/frontend/src/main.js:1)
- [frontend/src/App.vue](/abs/path/c:/corp_platform_app/frontend/src/App.vue:1)

### Important frontend folders

- `api/`: Axios wrappers for backend endpoints
- `components/`: reusable UI building blocks
- `layouts/`: page shell layouts
- `router/`: route configuration and guards
- `stores/`: Pinia stores
- `utils/`: helper utilities
- `views/`: screen-level components
- `i18n/`: translations
- `modules/`: CRUD configuration for reference pages

Key files:

- [frontend/src/api/http.js](/abs/path/c:/corp_platform_app/frontend/src/api/http.js:1)
- [frontend/src/router/index.js](/abs/path/c:/corp_platform_app/frontend/src/router/index.js:1)
- [frontend/src/router/routes.js](/abs/path/c:/corp_platform_app/frontend/src/router/routes.js:1)
- [frontend/src/stores/authStore.js](/abs/path/c:/corp_platform_app/frontend/src/stores/authStore.js:1)
- [frontend/src/stores/attendanceStore.js](/abs/path/c:/corp_platform_app/frontend/src/stores/attendanceStore.js:1)
- [frontend/src/stores/referenceStore.js](/abs/path/c:/corp_platform_app/frontend/src/stores/referenceStore.js:1)
- [frontend/src/views/AttendanceView.vue](/abs/path/c:/corp_platform_app/frontend/src/views/AttendanceView.vue:1)
- [frontend/src/views/ReportPreviewView.vue](/abs/path/c:/corp_platform_app/frontend/src/views/ReportPreviewView.vue:1)
- [frontend/src/components/AppCrudPage.vue](/abs/path/c:/corp_platform_app/frontend/src/components/AppCrudPage.vue:1)
- [frontend/src/utils/apiErrors.js](/abs/path/c:/corp_platform_app/frontend/src/utils/apiErrors.js:1)
- [frontend/src/i18n/messages.js](/abs/path/c:/corp_platform_app/frontend/src/i18n/messages.js:1)

## 6. Business Entities

### User

Fields:

- `username`
- `full_name`
- `role`
- `scope_type`
- `management`
- `department`
- `is_active`
- `is_staff`

Roles:

- `admin`
- `manager`

Scope types:

- `all`
- `management`
- `department`

### Management

Fields:

- `name`
- `code`
- `is_active`

### Department

Fields:

- `management`
- `name`
- `code`
- `is_active`

Constraint:

- unique `code` inside one `management`

### Position

Fields:

- `name`
- `short_name`
- `hierarchy_order`
- `is_active`

### StaffUnit

Fields:

- `department`
- `staff_position`
- `unit_number`
- `is_active`

Constraint:

- unique `unit_number` inside one `department`

### Employee

Fields:

- `last_name`
- `first_name`
- `middle_name`
- `short_fio`
- `personnel_number`
- `is_active`

Constraint:

- unique `personnel_number`

### EmployeeAssignment

Fields:

- `employee`
- `staff_unit`
- `actual_position`
- `start_date`
- `end_date`
- `is_current`
- `note`

Constraints:

- one current assignment per employee
- one current assignment per staff unit

### AbsenceReason

Fields:

- `name`
- `code`
- `is_system`
- `created_by`
- `is_active`

### AttendanceSheet

Fields:

- `date`
- `department`
- `created_by`
- `updated_by`

Constraint:

- one sheet per `date + department`

### AttendanceSheetItem

Fields:

- `attendance_sheet`
- `employee`
- `status`
- `absence_reason`
- `note`

Statuses:

- `present`
- `absent`

Constraint:

- one sheet row per `attendance_sheet + employee`

## 7. Access Control Rules

Access is enforced both by queryset filtering and explicit permission helpers.

Important helper:

- [common/permissions.py](/abs/path/c:/corp_platform_app/common/permissions.py:1)

Rules:

- `admin` can access all records
- `manager + all` can access active records broadly
- `manager + management` can access only departments and data inside one management
- `manager + department` can access only one department and dependent data

Developer rule:

When adding new backend endpoints, never return all records directly.
Always route visibility through selectors or shared permission helpers.

## 8. Main Backend API Map

### Auth

- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`
- `POST /api/auth/change-password/`

### Accounts

- `GET /api/users/`
- `POST /api/users/`
- `PUT/PATCH /api/users/{id}/`

### Organization

- `GET /api/managements/`
- `POST /api/managements/`
- `PUT/PATCH /api/managements/{id}/`
- `GET /api/departments/`
- `POST /api/departments/`
- `PUT/PATCH /api/departments/{id}/`

### Staff

- `GET /api/positions/`
- `GET /api/staff-units/`
- `GET /api/employees/`
- `GET /api/assignments/`

and matching create/update endpoints through DRF routers.

### Attendance

- `GET /api/absence-reasons/`
- `POST /api/absence-reasons/`
- `PATCH /api/absence-reasons/{id}/`
- `POST /api/attendance-sheets/open-or-create/`
- `PATCH /api/attendance-sheets/{id}/bulk-update/`
- `GET /api/reports/daily-attendance-html/`
- `GET /api/reports/daily-attendance-word/`
- `GET /api/reports/daily-attendance-pdf/`
- `GET /api/reports/summary-html/`
- `GET /api/reports/summary-word/`
- `GET /api/reports/summary-pdf/`

### Common

- `GET /api/health/`

## 9. Core Workflows

### 9.1 Login Flow

1. Frontend sends credentials to `POST /api/auth/login/`.
2. Backend returns JWT access and refresh tokens plus user info.
3. Frontend stores tokens in local storage.
4. Axios attaches access token to next requests.
5. If access token expires, frontend tries refresh automatically.

Main implementation:

- [frontend/src/api/http.js](/abs/path/c:/corp_platform_app/frontend/src/api/http.js:1)
- [frontend/src/stores/authStore.js](/abs/path/c:/corp_platform_app/frontend/src/stores/authStore.js:1)

### 9.2 Open Or Create Attendance Sheet

1. User selects date and department.
2. Frontend calls `POST /api/attendance-sheets/open-or-create/`.
3. Backend finds or creates one sheet for the date and department.
4. Backend syncs sheet rows with active assignments for that department and date.
5. Frontend displays rows for editing.

Main implementation:

- [attendance/services.py](/abs/path/c:/corp_platform_app/attendance/services.py:1)
- [frontend/src/stores/attendanceStore.js](/abs/path/c:/corp_platform_app/frontend/src/stores/attendanceStore.js:1)

### 9.3 Save Attendance Sheet

1. Frontend validates that every absent row has an absence reason.
2. Frontend sends bulk payload to `PATCH /api/attendance-sheets/{id}/bulk-update/`.
3. Backend validates each row and updates the sheet.
4. Frontend shows success or normalized API errors.

### 9.4 Daily Report Preview

1. Frontend navigates to `/reports/preview?type=daily&sheet_id=...`.
2. Preview view loads HTML from `daily-attendance-html`.
3. User can also download DOCX/PDF or print.

### 9.5 Summary Report By Period

1. User selects start and end dates on attendance page.
2. Frontend navigates to `/reports/preview?type=summary&start_date=...&end_date=...`.
3. Preview view loads HTML from `summary-html`.
4. User can also download DOCX/PDF.

## 10. Report Rules

Current supported report outputs:

- HTML
- DOCX
- PDF

Report generation code:

- [attendance/views.py](/abs/path/c:/corp_platform_app/attendance/views.py:1)
- [common/services.py](/abs/path/c:/corp_platform_app/common/services.py:1)

Developer rule:

- prefer reusing report label dictionaries and formatting helpers
- do not duplicate document generation logic in views
- keep one source of truth for localized report labels

## 11. Frontend Design Rules

When extending the frontend:

- reuse `AppCrudPage` for CRUD-like entities
- keep API calls inside `api/`
- keep persistent cross-screen state in Pinia stores
- keep route guards inside router
- use `messages.js` for all user-visible text
- do not hardcode localized strings in views
- use `normalizeApiError` for API error output

Important shared patterns:

- [frontend/src/components/AppCrudPage.vue](/abs/path/c:/corp_platform_app/frontend/src/components/AppCrudPage.vue:1)
- [frontend/src/utils/apiErrors.js](/abs/path/c:/corp_platform_app/frontend/src/utils/apiErrors.js:1)

## 12. Run Instructions

### Backend

```powershell
cd C:\corp_platform_app
.\.venv\Scripts\python.exe manage.py runserver
```

### Frontend

```powershell
cd C:\corp_platform_app\frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

### One-command startup

```powershell
cd C:\corp_platform_app
powershell -ExecutionPolicy Bypass -File .\start_project.ps1
```

## 13. Testing

Current checks used in development:

- `.\.venv\Scripts\python.exe manage.py check`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`
- `.\.venv\Scripts\python.exe manage.py test attendance`
- `npm.cmd run build`

Developer rule:

- every restored or added business workflow should get a regression test
- reporting, permissions, and assignment logic are especially important

## 14. Current Important Improvements Already Implemented

- missing Django migrations were added
- summary report by period was restored in the frontend
- report preview route reactivity was fixed
- backend tests for reports were added
- unified frontend API error normalization was added
- attendance page error handling was localized and cleaned up

## 15. Priority Roadmap For Next Development Stage

### High priority

- add more backend tests for permissions, assignments, and CRUD flows
- improve Django admin usability
- improve profile and login API error handling
- add logging and environment separation for dev/prod

### Medium priority

- improve report print layout using real production data
- improve staff unit occupancy visibility
- add stronger frontend validation for reference forms
- add audit trail for important changes

### Lower priority

- add CI workflow
- extend documentation with API examples
- improve backup and restore UX

## 16. Developer Delivery Rules

When implementing new code in this project:

1. Read selectors, services, and permissions before changing behavior.
2. Prefer extending existing modules over creating duplicate logic.
3. Keep backend business logic in services/selectors, not bloated views.
4. Keep frontend error messages localized.
5. Add or update tests for important behavior changes.
6. Update `log.txt` after each meaningful batch of changes.
7. Keep `PROJECT_DESCRIPTION.md` and `TECHNICAL_SPEC.md` relevant when architecture changes.
