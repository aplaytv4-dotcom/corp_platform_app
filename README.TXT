ATTENDANCE SYSTEM
=================

Проект состоит из двух частей:

1. Backend: Django + Django REST Framework + PostgreSQL + JWT
2. Frontend: Vue 3 + Pinia + Vue Router + axios + i18n


==================================================
1. НАЗНАЧЕНИЕ ПРОЕКТА
==================================================

Система предназначена для учета посещаемости сотрудников.

Основные возможности:

- авторизация по JWT
- учет организационной структуры
- учет сотрудников и назначений
- ведение ежедневного табеля посещаемости
- справочник причин отсутствия
- HTML preview отчетов
- выгрузка отчетов в Word и PDF
- разграничение доступа по ролям


==================================================
2. ТЗ НА BACKEND
==================================================

Технологии:

- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT

Архитектурные требования:

- модульная структура
- настройки БД через env
- бизнес-логика вынесена в services.py
- чтение данных вынесено в selectors.py
- permissions.py для правил доступа
- TimeStampedModel
- soft delete через is_active
- транзакции в сервисах

Apps:

- accounts
- organization
- staff
- attendance
- common

Структура каждого app:

- models.py
- serializers.py
- views.py
- urls.py
- permissions.py
- services.py
- selectors.py

Backend модели:

accounts:
- кастомный User
- username
- password
- full_name
- role: admin / manager
- scope_type: all / management / department
- management
- department
- is_active

organization:
- Management
- Department

staff:
- Position
- StaffUnit
- Employee
- EmployeeAssignment

attendance:
- AbsenceReason
- AttendanceSheet
- AttendanceSheetItem

Основная бизнес-логика:

- open_or_create_attendance_sheet(date, department)
- bulk_update_attendance_items(sheet_id, items)
- transfer_employee(...)
- close_assignment(...)

Основные backend endpoint-ы:

Auth:
- POST /api/auth/login/
- POST /api/auth/refresh/
- GET /api/auth/me/
- POST /api/auth/change-password/

Core:
- /api/users/
- /api/managements/
- /api/departments/
- /api/positions/
- /api/staff-units/
- /api/employees/
- /api/assignments/

Attendance:
- POST /api/attendance-sheets/open-or-create/
- GET /api/attendance-sheets/{id}/
- PATCH /api/attendance-sheets/{id}/bulk-update/

Assignments:
- POST /api/assignments/transfer/
- PATCH /api/assignments/{id}/close/

Absence Reasons:
- GET /api/absence-reasons/
- POST /api/absence-reasons/
- PATCH /api/absence-reasons/{id}/

Reports:
- GET /api/reports/daily-attendance-html/
- GET /api/reports/daily-attendance-word/
- GET /api/reports/daily-attendance-pdf/
- GET /api/reports/summary-html/
- GET /api/reports/summary-word/
- GET /api/reports/summary-pdf/

Правила доступа:

admin:
- полный доступ

manager + department:
- доступ только к своему отделу

manager + management:
- доступ ко всем отделам своего управления

Валидации:

- absent => причина обязательна
- нельзя создать 2 табеля на одну дату и отдел
- нельзя иметь 2 активных назначения на сотрудника
- нельзя иметь 2 активных сотрудника на одну штатную единицу


==================================================
3. ТЗ НА FRONTEND
==================================================

Технологии:

- Vue 3
- Pinia
- Vue Router
- axios
- Vue I18n
- Composition API
- Vite

Структура frontend/src:

- api/
- assets/
- components/
- composables/
- layouts/
- modules/
- router/
- stores/
- views/
- i18n/
- utils/

Layouts:

- AuthLayout
- MainLayout

Маршруты:

Общие:
- /login
- /attendance
- /profile

Для всех авторизованных:
- /attendance
- /employees
- /absence-reasons
- /reports/preview

Только для admin:
- /users
- /managements
- /departments
- /positions
- /staff-units
- /assignments

Frontend использует только существующий REST API backend.
Новые URL на фронтенде не придумываются.

Основные экраны:

- Login
- Attendance
- Employees
- Absence Reasons
- Users
- Managements
- Departments
- Positions
- Staff Units
- Assignments
- Profile
- Report Preview

Языки интерфейса:

- русский
- узбекский

Требования UI:

- строгий деловой интерфейс
- основной экран после входа: табель
- для manager скрыты административные разделы
- кнопки Word/PDF только на экране preview отчета


==================================================
4. СТРУКТУРА ПРОЕКТА НА ДИСКЕ
==================================================

Корень backend:

- manage.py
- requirements.txt
- .env.example
- config/
- accounts/
- organization/
- staff/
- attendance/
- common/

Frontend:

- frontend/package.json
- frontend/vite.config.js
- frontend/.env.example
- frontend/src/...


==================================================
5. НЕОБХОДИМЫЕ ПАКЕТЫ
==================================================

Backend Python пакеты:

- Django
- djangorestframework
- djangorestframework-simplejwt
- psycopg[binary]

Frontend npm пакеты:

- vue
- pinia
- vue-router
- vue-i18n
- axios
- vite
- @vitejs/plugin-vue


==================================================
6. ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ
==================================================

Перед запуском должны быть установлены:

1. Python 3.13+
2. PostgreSQL
3. Node.js
4. npm


==================================================
7. УСТАНОВКА BACKEND
==================================================

Из корня проекта:

1. Создать виртуальное окружение:

    python -m venv .venv

2. Активировать:

    .\.venv\Scripts\Activate.ps1

3. Установить зависимости:

    python -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt

4. Скопировать env:

    Copy-Item .env.example .env

5. Проверить настройки PostgreSQL в .env:

    DB_NAME=attendance_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=127.0.0.1
    DB_PORT=5432

6. Если базы attendance_db нет, создать ее в PostgreSQL.

7. Выполнить миграции:

    python manage.py makemigrations
    python manage.py migrate

8. Запустить backend:

    python manage.py runserver 127.0.0.1:8000


==================================================
8. УСТАНОВКА FRONTEND
==================================================

Перейти в папку frontend:

    cd frontend

1. Скопировать env:

    Copy-Item .env.example .env

2. Установить зависимости:

    npm install

3. Запустить frontend:

    npm run dev


==================================================
9. НАСТРОЙКИ ENV
==================================================

Backend .env:

    DJANGO_SECRET_KEY=dev-secret-key-change-me-1234567890-abcdef
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver
    DB_NAME=attendance_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=127.0.0.1
    DB_PORT=5432
    ACCESS_TOKEN_MINUTES=60
    REFRESH_TOKEN_DAYS=7

Frontend .env:

    VITE_API_BASE_URL=http://127.0.0.1:8000


==================================================
10. URL ДЛЯ РАЗРАБОТКИ
==================================================

Frontend:

    http://127.0.0.1:5173

Backend API:

    http://127.0.0.1:8000

Django admin:

    http://127.0.0.1:8000/admin/


==================================================
11. ТЕСТОВЫЕ ЛОГИНЫ
==================================================

Администратор:

- login: admin
- password: admin12345

Менеджер отдела:

- login: manager_dep
- password: manager12345


==================================================
12. БЫСТРАЯ РУЧНАЯ ПРОВЕРКА
==================================================

1. Открыть frontend:

    http://127.0.0.1:5173/login

2. Войти под admin:

- admin / admin12345

3. Проверить, что после входа открывается экран табеля.

4. На табеле:

- выбрать дату
- выбрать отдел
- нажать "Открыть табель"
- изменить статус сотрудника на absent
- выбрать причину
- нажать "Сохранить табель"

5. Нажать "Просмотр отчета".

6. На экране preview проверить:

- Назад
- Сохранить в Word
- Сохранить в PDF
- Печать

7. Проверить разделы admin:

- Users
- Managements
- Departments
- Positions
- Staff Units
- Assignments

8. Проверить экран Profile:

- отображение данных пользователя
- смена пароля
- выход

9. Выйти и войти под manager:

- manager_dep / manager12345

10. Проверить, что manager:

- попадает на табель
- видит attendance, employees, absence-reasons, profile
- не видит admin разделы


==================================================
13. GIT
==================================================

Git уже инициализирован.

Первый commit:

- f069e21
- Initial attendance backend and frontend


==================================================
14. ПРИМЕЧАНИЕ
==================================================

Проект готов для локальной разработки.

Если нужно продолжение, следующий логичный шаг:

- пуш в GitHub
- настройка CI/CD
- Swagger/OpenAPI
- e2e тесты
- UI polishing
