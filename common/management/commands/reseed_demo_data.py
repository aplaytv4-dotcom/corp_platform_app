from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from attendance.models import AbsenceReason, AttendanceSheet, AttendanceSheetItem
from organization.models import Department, Management
from staff.models import Employee, EmployeeAssignment, Position, StaffUnit


class Command(BaseCommand):
    help = "Полностью пересоздаёт демо-данные для локальной разработки."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Очистка старых демо-данных...")

        AttendanceSheetItem.objects.all().delete()
        AttendanceSheet.objects.all().delete()
        EmployeeAssignment.objects.all().delete()
        AbsenceReason.objects.all().delete()

        User.objects.exclude(username="admin").delete()
        Employee.objects.all().delete()
        StaffUnit.objects.all().delete()
        Position.objects.all().delete()
        Department.objects.all().delete()
        Management.objects.all().delete()

        admin = self._ensure_admin()
        data = self._create_reference_data(admin)
        self._create_demo_users(data)
        self._create_demo_staff(data)
        self._create_demo_attendance(data, admin)

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно пересозданы."))

    def _ensure_admin(self):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "full_name": "System Admin",
                "role": User.Role.ADMIN,
                "scope_type": User.ScopeType.ALL,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.full_name = "System Admin"
        admin.role = User.Role.ADMIN
        admin.scope_type = User.ScopeType.ALL
        admin.management = None
        admin.department = None
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("admin12345")
        admin.save()
        if created:
            self.stdout.write("Создан пользователь admin.")
        return admin

    def _create_reference_data(self, admin):
        management = Management.objects.create(name="Главное управление", code="MGMT-MAIN", is_active=True)

        departments = {
            "hr": Department.objects.create(management=management, name="Отдел кадров", code="DEP-HR", is_active=True),
            "it": Department.objects.create(management=management, name="ИТ отдел", code="DEP-IT", is_active=True),
            "fin": Department.objects.create(management=management, name="Финансовый отдел", code="DEP-FIN", is_active=True),
            "sec": Department.objects.create(management=management, name="Административный отдел", code="DEP-SEC", is_active=True),
        }

        positions = {
            "head": Position.objects.create(name="Начальник отдела", short_name="Нач. отдела", is_active=True),
            "specialist": Position.objects.create(name="Главный специалист", short_name="Гл. спец.", is_active=True),
            "inspector": Position.objects.create(name="Инспектор", short_name="Инсп.", is_active=True),
            "engineer": Position.objects.create(name="Инженер", short_name="Инж.", is_active=True),
            "accountant": Position.objects.create(name="Бухгалтер", short_name="Бух.", is_active=True),
            "administrator": Position.objects.create(name="Администратор", short_name="Адм.", is_active=True),
        }

        hierarchy_updates = {
            "head": 110,
            "specialist": 90,
            "inspector": 60,
            "engineer": 40,
            "accountant": 20,
            "administrator": 10,
        }
        for key, order in hierarchy_updates.items():
            positions[key].hierarchy_order = order
            positions[key].save(update_fields=["hierarchy_order"])

        absence_reasons = [
            AbsenceReason.objects.create(name="Больничный", code="SICK", is_system=False, created_by=admin, is_active=True),
            AbsenceReason.objects.create(name="Отпуск", code="VAC", is_system=False, created_by=admin, is_active=True),
            AbsenceReason.objects.create(name="Командировка", code="TRIP", is_system=False, created_by=admin, is_active=True),
            AbsenceReason.objects.create(name="Отгул", code="OFF", is_system=False, created_by=admin, is_active=True),
        ]

        return {
            "management": management,
            "departments": departments,
            "positions": positions,
            "absence_reasons": absence_reasons,
            "staff_units": [],
            "employees": [],
            "assignments": [],
        }

    def _create_demo_users(self, data):
        management = data["management"]
        departments = data["departments"]

        users = [
            {
                "username": "manager_main",
                "full_name": "Руководитель управления",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.MANAGEMENT,
                "management": management,
                "department": None,
                "password": "manager12345",
            },
            {
                "username": "manager_dep",
                "full_name": "Начальник отдела кадров",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.DEPARTMENT,
                "management": None,
                "department": departments["hr"],
                "password": "manager12345",
            },
            {
                "username": "head_dep_hr",
                "full_name": "Начальник отдела кадров",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.DEPARTMENT,
                "management": None,
                "department": departments["hr"],
                "password": "manager12345",
            },
            {
                "username": "head_dep_it",
                "full_name": "Начальник ИТ отдела",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.DEPARTMENT,
                "management": None,
                "department": departments["it"],
                "password": "manager12345",
            },
            {
                "username": "head_dep_fin",
                "full_name": "Начальник финансового отдела",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.DEPARTMENT,
                "management": None,
                "department": departments["fin"],
                "password": "manager12345",
            },
            {
                "username": "head_dep_sec",
                "full_name": "Начальник административного отдела",
                "role": User.Role.MANAGER,
                "scope_type": User.ScopeType.DEPARTMENT,
                "management": None,
                "department": departments["sec"],
                "password": "manager12345",
            },
        ]

        for item in users:
            user = User.objects.create(
                username=item["username"],
                full_name=item["full_name"],
                role=item["role"],
                scope_type=item["scope_type"],
                management=item["management"],
                department=item["department"],
                is_active=True,
                is_staff=False,
            )
            user.set_password(item["password"])
            user.save()

    def _create_demo_staff(self, data):
        departments = data["departments"]
        positions = data["positions"]

        templates = [
            ("hr", "001", positions["head"], "Каримов", "Азиз", "Рустамович", positions["head"]),
            ("hr", "002", positions["specialist"], "Ибрагимова", "Нилуфар", "Акмаловна", positions["specialist"]),
            ("hr", "003", positions["inspector"], "Рахимова", "Дилфуза", "Шавкатовна", positions["inspector"]),
            ("it", "001", positions["head"], "Саидов", "Отабек", "Нодирович", positions["head"]),
            ("it", "002", positions["engineer"], "Юлдашев", "Шерзод", "Икромович", positions["engineer"]),
            ("it", "003", positions["engineer"], "Пулатова", "Мафтуна", "Равшановна", positions["engineer"]),
            ("fin", "001", positions["head"], "Назаров", "Бекзод", "Абдуллаевич", positions["head"]),
            ("fin", "002", positions["accountant"], "Абдуллаева", "Замира", "Фарходовна", positions["accountant"]),
            ("fin", "003", positions["accountant"], "Турсунов", "Жасур", "Комилович", positions["accountant"]),
            ("sec", "001", positions["head"], "Махмудов", "Сардор", "Бахтиёрович", positions["head"]),
            ("sec", "002", positions["administrator"], "Хасанова", "Шахноза", "Олимовна", positions["administrator"]),
            ("sec", "003", positions["administrator"], "Эргашев", "Ботир", "Анварович", positions["administrator"]),
        ]

        for index, (dep_key, unit_number, staff_position, last_name, first_name, middle_name, actual_position) in enumerate(templates, start=1001):
            department = departments[dep_key]
            staff_unit = StaffUnit.objects.create(
                department=department,
                staff_position=staff_position,
                unit_number=unit_number,
                is_active=True,
            )
            employee = Employee.objects.create(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                personnel_number=str(index),
                is_active=True,
            )
            assignment = EmployeeAssignment.objects.create(
                employee=employee,
                staff_unit=staff_unit,
                actual_position=actual_position,
                start_date=date.today() - timedelta(days=120),
                is_current=True,
                note="Тестовое назначение",
            )
            data["staff_units"].append(staff_unit)
            data["employees"].append(employee)
            data["assignments"].append(assignment)

    def _create_demo_attendance(self, data, admin):
        reasons = data["absence_reasons"]
        reason_cycle = [reasons[0], reasons[1], reasons[2], reasons[3]]
        assignments = data["assignments"]

        by_department = {}
        for assignment in assignments:
            by_department.setdefault(assignment.staff_unit.department_id, []).append(assignment)

        for offset in range(0, 7):
            sheet_date = date.today() - timedelta(days=offset)
            for department in data["departments"].values():
                sheet = AttendanceSheet.objects.create(
                    date=sheet_date,
                    department=department,
                    created_by=admin,
                    updated_by=admin,
                )

                for row_index, assignment in enumerate(by_department.get(department.id, []), start=1):
                    is_absent = (offset + row_index) % 5 == 0
                    reason = reason_cycle[(offset + row_index) % len(reason_cycle)] if is_absent else None
                    note = ""
                    if is_absent:
                        note = f"Тестовая причина: {reason.name.lower()}"
                    AttendanceSheetItem.objects.create(
                        attendance_sheet=sheet,
                        employee=assignment.employee,
                        status=AttendanceSheetItem.Status.ABSENT if is_absent else AttendanceSheetItem.Status.PRESENT,
                        absence_reason=reason,
                        note=note,
                    )
