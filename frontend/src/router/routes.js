import AttendanceView from "@/views/AttendanceView.vue";
import AbsenceReasonsView from "@/views/AbsenceReasonsView.vue";
import AssignmentsView from "@/views/AssignmentsView.vue";
import DepartmentsView from "@/views/DepartmentsView.vue";
import EmployeesView from "@/views/EmployeesView.vue";
import ForbiddenView from "@/views/ForbiddenView.vue";
import LoginView from "@/views/LoginView.vue";
import ManagementsView from "@/views/ManagementsView.vue";
import PositionsView from "@/views/PositionsView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ReportPreviewView from "@/views/ReportPreviewView.vue";
import StaffUnitsView from "@/views/StaffUnitsView.vue";
import UsersView from "@/views/UsersView.vue";

export const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guestOnly: true, layout: "auth" },
  },
  {
    path: "/",
    redirect: "/attendance",
  },
  {
    path: "/attendance",
    name: "attendance",
    component: AttendanceView,
    meta: { requiresAuth: true, layout: "main" },
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileView,
    meta: { requiresAuth: true, layout: "main" },
  },
  {
    path: "/employees",
    name: "employees",
    component: EmployeesView,
    meta: { requiresAuth: true, layout: "main" },
  },
  {
    path: "/absence-reasons",
    name: "absence-reasons",
    component: AbsenceReasonsView,
    meta: { requiresAuth: true, layout: "main" },
  },
  {
    path: "/reports/preview",
    name: "reports-preview",
    component: ReportPreviewView,
    meta: { requiresAuth: true, layout: "main" },
  },
  {
    path: "/users",
    name: "users",
    component: UsersView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/managements",
    name: "managements",
    component: ManagementsView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/departments",
    name: "departments",
    component: DepartmentsView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/positions",
    name: "positions",
    component: PositionsView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/staff-units",
    name: "staff-units",
    component: StaffUnitsView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/assignments",
    name: "assignments",
    component: AssignmentsView,
    meta: { requiresAuth: true, requiresAdmin: true, layout: "main" },
  },
  {
    path: "/403",
    name: "forbidden",
    component: ForbiddenView,
    meta: { requiresAuth: true, layout: "main" },
  },
];
