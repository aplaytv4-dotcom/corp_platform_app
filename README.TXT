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

Дополнительно для backend PDF:

- reportlab


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

    http://localhost:5173

Примечание:

    если http://127.0.0.1:5173 не открывается, используйте http://localhost:5173

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

Руководитель управления:

- login: manager_main
- password: manager12345

Начальники отделов:

- login: head_dep_hr
- password: manager12345

- login: head_dep_it
- password: manager12345

- login: head_dep_fin
- password: manager12345

- login: head_dep_sec
- password: manager12345

Дополнительный тестовый начальник старого отдела:

- login: head_dep_1
- password: manager12345


==================================================
12. БЫСТРАЯ РУЧНАЯ ПРОВЕРКА
==================================================

1. Открыть frontend:

    http://localhost:5173/login

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

IMPORTANT UPDATE
================

Frontend dev URL:

    http://localhost:5173

Если http://127.0.0.1:5173 не открывается, используйте localhost.

Команда для полной пересборки тестовых данных:

    python manage.py reseed_demo_data

Эта команда:

- пересоздаёт демо-данные
- обновляет тестовые логины
- восстанавливает пароль admin: admin12345
- помогает после проблем с кодировкой в старых тестовых данных

Отчеты:

- HTML preview, Word и PDF теперь используют текущий язык интерфейса frontend
- для preview отчетов frontend передает параметр lang в backend
- в ежедневном отчете пустые колонки автоматически скрываются
- если в выбранном табеле нет причин и примечаний, колонки "Причина" и "Примечание" не показываются
- табельный номер исключен из всех отчетов
- в ежедневные отчеты добавлен порядковый номер строки сотрудника
- в ежедневных отчетах отображается фактическая должность сотрудника отдельной колонкой
- PDF отчеты теперь собираются через reportlab с Unicode-шрифтом и корректно показывают кириллицу
- HTML preview, Word и PDF оформлены в деловом стиле с таблицами
- основной шрифт отчетов: Times New Roman
- размер основного текста отчетов: 14
- размер заголовков отчетов: 16
- даты в отчетах выводятся в человекочитаемом формате, например: 15 апреля 2026 года
- в ежедневный отчет добавлен блок подписи начальника отдела
- в блоке подписи есть должность, место для подписи, Ф.И.О. и дата
- на экране сотрудников переведены таблица, поиск, статус и форма создания/редактирования
- на экране штатных единиц переведены таблица, подзаголовок, форма и статусы
 
==================================================
15. IMPORTANT UPDATE
==================================================
 
Frontend dev URL:
 
    http://localhost:5173
 
Если http://127.0.0.1:5173 не открывается, используйте localhost.
 
Команда для полной пересборки тестовых данных:
 
    python manage.py reseed_demo_data
 
Эта команда:
 
- пересоздаёт демо-данные
- обновляет тестовые логины
- восстанавливает пароль admin: admin12345
- исправляет тестовую базу после проблем с кодировкой в старых seed-данных
 
==================================================
16. REPORT SIGNATURE UPDATE
==================================================
 
- In the daily report signature block, the department head name is now taken from the current employee assignment for the selected department.
- Priority:
  1. active assignment with actual position "Начальник отдела"
  2. active assignment with staff position "Начальник отдела"
  3. fallback to manager user profile for the department
- This applies to HTML preview, Word, and PDF.
- The department head name is shown in short F.I.O. format, for example: "Иванов И.И."
- The Positions screen now uses i18n-based table and form labels for both Russian and Uzbek.
- CRUD sections now use i18n-based table headers and form labels for Russian and Uzbek:
  Absence Reasons, Managements, Departments, Positions, Users, Employees, Staff Units, Assignments.
- Report preview now reloads when RU/UZ is switched, so the report content follows the current interface language.
- Daily reports now include a summary block:
  total staff, present count, absent count, and absence breakdown by reason.
- Signature block in reports is centered more neatly, and the hint labels are shown in parentheses.
- In daily reports, the small date at the top left is the report generation date, while the date under the department head signature is the report date itself.
- Daily report header now shows: "Ежедневный отчет по посещаемости за <date>" aligned to the right.
- Daily report summary is now a right-aligned text block:
  staff total, present total, absent total, and each absence reason with employee F.I.O. list.
- Daily report layout updated:
  title centered in two lines, department and totals aligned left, absence reasons visually highlighted in a separate block.
- On the attendance screen, the "Примечание" field is now compact in height and closer in size to the other working inputs.
- CRUD forms now show backend validation errors directly in the modal instead of failing silently.
- Attendance sheet sync now includes only active employees on active staff units.
- When a sheet is reopened, rows for employees who no longer belong in the sheet are removed automatically.
- Report signature block now uses only an active current head-of-department assignment on an active staff unit.
- If there is no active department head assignment, the F.I.O. field in the report signature stays empty.
- If the department head is absent, inactive, or assigned to an inactive staff unit, the report signature now falls back to the next active employee in the department based on the configured position hierarchy for the report date.
- Daily report rows are now rebuilt against active assignments on the report date, so employees from inactive staff units do not appear in the report preview even if the sheet had been opened earlier.
- In the report signature, when the department head is absent, the report now shows the actual position and short F.I.O. of the next active employee in the hierarchy for that report date.
- Positions now have a configurable hierarchy_order field shown in the UI as "Тарифная сетка" / "Tarif setkasi". Reports and signatory replacement use it instead of the old hardcoded hierarchy list.
- hierarchy_order for positions is entered manually when creating a position; it is no longer auto-filled by default in the form.
- Tariff grid semantics: the higher the value, the more senior the position. Signatory fallback and replacement logic now choose the employee with the highest tariff grade among active assignments.
- On the Assignments screen, records are historical. The UI now shows current assignments by default, and closed records can be viewed separately through the filter.
- On the attendance screen, if status is set to "present", the absence reason and note are now cleared automatically in the UI and also forcibly cleared on backend save.
- In the daily report title, the second line with the report date is now shown in regular weight instead of bold.

==================================================
17. АКТУАЛЬНОЕ ТЗ НА BACKEND
==================================================

Этот раздел является актуальным описанием backend и заменяет исходное ТЗ выше, если между ними есть расхождения.

Технологии:

- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT
- django-cors-headers
- reportlab

Архитектура:

- модульная структура приложений: `accounts`, `organization`, `staff`, `attendance`, `common`
- в каждом приложении используются `models.py`, `serializers.py`, `views.py`, `urls.py`, `permissions.py`, `services.py`, `selectors.py`
- настройки базы и окружения берутся из `.env`
- бизнес-логика вынесена в `services.py`
- чтение и выборки вынесены в `selectors.py`
- используется `TimeStampedModel`
- soft delete реализован через `is_active`
- операции записи выполняются через транзакции
- есть Django Admin для основных сущностей

Фактические модели:

accounts:
- кастомный `User`
- `username`
- `password`
- `full_name`
- `role: admin / manager`
- `scope_type: all / management / department`
- `management`
- `department`
- `is_active`

organization:
- `Management`
- `Department`

staff:
- `Position`
- `StaffUnit`
- `Employee`
- `EmployeeAssignment`

attendance:
- `AbsenceReason`
- `AttendanceSheet`
- `AttendanceSheetItem`

Фактические правила по staff:

- у `Position` есть поле `hierarchy_order`, которое на frontend называется `Тарифная сетка`
- чем выше значение тарифной сетки, тем выше должность
- значение тарифной сетки задаётся вручную при создании/редактировании должности
- `EmployeeAssignment` хранит историю назначений; старые записи закрываются, а не удаляются
- одновременно не может быть двух текущих назначений у одного сотрудника
- одновременно не может быть двух текущих сотрудников на одной штатной единице

Фактические правила по attendance:

- в табель попадают только активные сотрудники с активными назначениями на активных штатных единицах
- при повторном открытии табеля устаревшие строки автоматически удаляются
- `status = absent` требует причину отсутствия
- `status = present` принудительно очищает `absence_reason` и `note`
- нельзя создать два табеля на одну дату и один отдел

Сервисы бизнес-логики:

- `open_or_create_attendance_sheet(date, department, user)`
- `bulk_update_attendance_items(sheet_id, items, user)`
- `transfer_employee(...)`
- `close_assignment(...)`

Отчёты:

- daily: HTML / Word / PDF
- summary: HTML / Word / PDF
- отчёты локализуются по `lang=ru/uz`
- PDF формируется через `reportlab` с Unicode-шрифтом
- daily report содержит:
  - отдел
  - блок `По штату / Присутствуют / Отсутствуют`
  - причины отсутствия с Ф.И.О.
  - таблицу с фактической должностью
  - блок подписи
- подписант daily report выбирается из активных сотрудников отдела на дату отчёта
- сотрудники, отмеченные в табеле как отсутствующие, не могут быть выбраны как подписанты
- выбор подписанта идёт по максимальному значению тарифной сетки
- в подписи выводятся фактическая должность и короткое Ф.И.О.

Актуальные backend endpoints:

Auth:
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`
- `POST /api/auth/change-password/`

Core:
- `/api/users/`
- `/api/managements/`
- `/api/departments/`
- `/api/positions/`
- `/api/staff-units/`
- `/api/employees/`
- `/api/assignments/`

Attendance:
- `POST /api/attendance-sheets/open-or-create/`
- `GET /api/attendance-sheets/{id}/`
- `PATCH /api/attendance-sheets/{id}/bulk-update/`

Assignments:
- `POST /api/assignments/transfer/`
- `PATCH /api/assignments/{id}/close/`

Absence Reasons:
- `GET /api/absence-reasons/`
- `POST /api/absence-reasons/`
- `PATCH /api/absence-reasons/{id}/`

Reports:
- `GET /api/reports/daily-attendance-html/`
- `GET /api/reports/daily-attendance-word/`
- `GET /api/reports/daily-attendance-pdf/`
- `GET /api/reports/summary-html/`
- `GET /api/reports/summary-word/`
- `GET /api/reports/summary-pdf/`

Права доступа:

- admin: полный доступ
- manager + department: доступ только к своему отделу
- manager + management: доступ ко всем отделам своего управления


==================================================
18. АКТУАЛЬНОЕ ТЗ НА FRONTEND
==================================================

Этот раздел является актуальным описанием frontend и заменяет исходное ТЗ выше, если между ними есть расхождения.

Технологии:

- Vue 3
- Pinia
- Vue Router
- axios
- Vue I18n
- Composition API
- Vite

Структура `frontend/src`:

- `api/`
- `assets/`
- `components/`
- `composables/`
- `layouts/`
- `modules/`
- `router/`
- `stores/`
- `views/`
- `i18n/`
- `utils/`

Layouts:

- `AuthLayout`
- `MainLayout`

MainLayout содержит:

- боковое меню
- переключатель языка `RU / UZ`
- имя пользователя
- пункты `Профиль` / `Выйти`

Маршруты:

Общие:
- `/login`
- `/attendance`
- `/profile`

Для всех авторизованных:
- `/attendance`
- `/employees`
- `/absence-reasons`
- `/reports/preview`

Только для admin:
- `/users`
- `/managements`
- `/departments`
- `/positions`
- `/staff-units`
- `/assignments`

Frontend работает строго поверх существующего REST API backend.

Фактические экраны:

- `Login`
- `Attendance`
- `Employees`
- `Absence Reasons`
- `Users`
- `Managements`
- `Departments`
- `Positions`
- `Staff Units`
- `Assignments`
- `Profile`
- `Report Preview`

Фактическое поведение экранов:

Attendance:
- это главный экран после входа
- при `absent` показывается выбор причины
- при `present` причина и примечание очищаются сразу на frontend
- поле `Примечание` сделано компактным

Assignments:
- экран показывает историю назначений
- по умолчанию отображаются только текущие записи
- есть фильтр `Текущие / Закрытые / Все`
- кнопка `Закрыть` показывается только для текущих назначений

Positions:
- в таблице и форме есть поле `Тарифная сетка`
- значение задаётся вручную

Report Preview:
- открывается в текущем окне
- кнопки `Word / PDF / Печать` есть только на этом экране
- при переключении `RU / UZ` отчёт перезагружается
- daily report показывает сводный блок, причины отсутствия, фактические должности и подпись замещающего сотрудника
- в preview не должны попадать устаревшие строки с неактивных штатных единиц

Языки интерфейса:

- русский
- узбекский

UI / UX:

- строгий деловой интерфейс
- основной экран после входа: табель
- у manager скрыты административные разделы
- меню имеет hover / active подсветку
- i18n применяется к основным CRUD-экранам и отчётам
