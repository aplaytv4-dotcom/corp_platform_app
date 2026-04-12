# Attendance Platform Project Description

## Overview

This project is a corporate attendance accounting platform with a Django REST backend and a Vue 3 frontend.
It is designed for managing organizational structure, staff positions, employees, assignments, daily attendance sheets,
absence reasons, and generated attendance reports.

## Main Goals

- Maintain an up-to-date organizational structure.
- Manage employees and their current assignments.
- Open and update daily attendance sheets by department and date.
- Track absence reasons for employees who are not present.
- Generate daily and summary attendance reports in HTML, Word, and PDF formats.
- Support role-based access for administrators and managers.

## Architecture

### Backend

The backend is built with Django and Django REST Framework.

Core apps:

- `accounts`: authentication, profile data, password change, access scope.
- `organization`: managements and departments.
- `staff`: positions, staff units, employees, assignments.
- `attendance`: attendance sheets, attendance items, absence reasons, reports.
- `common`: shared models, permissions, renderers, document generation helpers, admin utilities.

Backend features:

- JWT authentication with refresh tokens.
- Role and scope based access control.
- PostgreSQL as the main database.
- HTML, DOCX, and PDF report generation.
- Admin support for system management.

### Frontend

The frontend is built with Vue 3, Vite, Pinia, Vue Router, and Vue I18n.

Frontend features:

- Login and authenticated routing.
- CRUD screens for core entities.
- Attendance sheet editing UI.
- Daily report preview.
- Summary report preview for a selected period.
- Russian and Uzbek localization.
- Shared reusable form and table components.

## Data Model Summary

- A `Management` contains multiple `Department` records.
- A `Department` contains `StaffUnit` records.
- A `StaffUnit` is linked to a staff position (`Position`).
- An `Employee` can have assignments to staff units through `EmployeeAssignment`.
- An `AttendanceSheet` belongs to a department and a date.
- An `AttendanceSheetItem` stores employee attendance status for a sheet.
- An `AbsenceReason` explains an absence when status is `absent`.

## Access Model

- `admin`: full access to the system.
- `manager` with `all` scope: broad access to active records.
- `manager` with `management` scope: access limited to one management.
- `manager` with `department` scope: access limited to one department.

## Reports

Supported report types:

- Daily attendance report.
- Summary attendance report for a selected date range.

Supported output formats:

- HTML preview.
- DOCX download.
- PDF download.

## Current Important Improvements Already Added

- Restored summary report by period in the frontend.
- Fixed report preview updates when route query parameters change.
- Added backend tests for daily and summary reports.
- Added unified frontend API error normalization.
- Removed broken hardcoded error strings from the attendance screen.
- Added missing Django migrations to keep models and migration history in sync.

## Run Requirements

- Python virtual environment in `.venv`
- PostgreSQL configured via `.env`
- Frontend dependencies installed in `frontend/node_modules`

## Main Entry Points

- Backend: `manage.py`
- Frontend: `frontend/package.json`
- Project launcher: `start_project.ps1`
