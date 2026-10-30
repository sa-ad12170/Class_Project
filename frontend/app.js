const state = {
  employees: [],
  departments: [],
};

const viewTitles = {
  dashboard: "Dashboard",
  employees: "Employees",
  payslips: "Payslips",
};

const moneyFormatter = new Intl.NumberFormat("en-UG", {
  style: "currency",
  currency: "UGX",
  maximumFractionDigits: 0,
});

function formatMoney(value) {
  return moneyFormatter.format(Number(value) || 0);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const detail = data?.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join(", ")
      : detail || "The request could not be completed.";
    throw new Error(message);
  }
  return data;
}

let toastTimer;
function showToast(message, isError = false) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.classList.toggle("is-error", isError);
  toast.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 3400);
}

function showView(viewName, focusId = null) {
  document.querySelectorAll("[data-view]").forEach((view) => {
    view.classList.toggle("is-active", view.dataset.view === viewName);
  });
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("is-active", item.dataset.viewLink === viewName);
  });
  document.querySelector("#page-title").textContent = viewTitles[viewName];
  window.location.hash = viewName;
  window.scrollTo({ top: 0, behavior: "smooth" });

  if (focusId) {
    requestAnimationFrame(() => document.querySelector(`#${focusId}`)?.focus());
  }
}

function setupNavigation() {
  document.querySelectorAll("[data-view-link]").forEach((control) => {
    control.addEventListener("click", (event) => {
      event.preventDefault();
      showView(control.dataset.viewLink, control.dataset.focus || null);
    });
  });

  const initialView = window.location.hash.slice(1);
  if (viewTitles[initialView]) {
    showView(initialView);
  }
}

function renderRecentPayslips(payslips) {
  const body = document.querySelector("#recent-payslips-body");
  const empty = document.querySelector("#recent-payslips-empty");
  body.innerHTML = payslips
    .map(
      (item) => `
        <tr>
          <td><strong>${escapeHtml(item.employee_name || item.employee_id || "Employee")}</strong></td>
          <td>${escapeHtml(item.payslip_id)}</td>
          <td>${formatMoney(item.gross)}</td>
          <td><strong>${formatMoney(item.net)}</strong></td>
        </tr>
      `,
    )
    .join("");
  empty.classList.toggle("is-hidden", payslips.length > 0);
}

function renderDepartments() {
  const list = document.querySelector("#department-list");
  list.innerHTML = state.departments
    .map((department) => {
      const initials = department.name
        .split(/\s+/)
        .map((word) => word[0])
        .join("")
        .slice(0, 2)
        .toUpperCase();
      const staffCount = Array.isArray(department.staff) ? department.staff.length : 0;
      return `
        <div class="department-item">
          <span class="department-badge">${escapeHtml(initials)}</span>
          <div>
            <strong>${escapeHtml(department.name)}</strong>
            <small>${staffCount} ${staffCount === 1 ? "staff member" : "staff members"}</small>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderEmployees() {
  const list = document.querySelector("#employee-list");
  const empty = document.querySelector("#employees-empty");
  const count = document.querySelector("#employee-count");
  count.textContent = `${state.employees.length} ${state.employees.length === 1 ? "employee" : "employees"}`;

  list.innerHTML = state.employees
    .map((employee) => {
      const fullName = `${employee.first_name || ""} ${employee.last_name || ""}`.trim();
      const initials = `${employee.first_name?.[0] || ""}${employee.last_name?.[0] || ""}`.toUpperCase();
      return `
        <div class="employee-card">
          <span class="employee-avatar">${escapeHtml(initials || "E")}</span>
          <div>
            <strong>${escapeHtml(fullName || employee.employee_id)}</strong>
            <small>${escapeHtml(employee.employee_id)} · ${escapeHtml(employee.position)} · ${escapeHtml(employee.department)}</small>
          </div>
          <span class="employee-status">${escapeHtml(employee.status || "Active")}</span>
        </div>
      `;
    })
    .join("");
  empty.classList.toggle("is-hidden", state.employees.length > 0);

  const select = document.querySelector("#payslip-employee");
  const selected = select.value;
  select.innerHTML = '<option value="">Select an employee</option>';
  state.employees.forEach((employee) => {
    const option = document.createElement("option");
    option.value = employee.employee_id;
    option.textContent = `${employee.first_name} ${employee.last_name} (${employee.employee_id})`;
    select.append(option);
  });
  if (state.employees.some((employee) => employee.employee_id === selected)) {
    select.value = selected;
  }
}

async function loadDashboard() {
  const data = await api("/api/dashboard");
  document.querySelector("#stat-employees").textContent = data.stats.employees;
  document.querySelector("#stat-departments").textContent = data.stats.departments;
  document.querySelector("#stat-payslips").textContent = data.stats.payslips;
  document.querySelector("#stat-total-net").textContent = formatMoney(data.stats.total_net_pay);
  renderRecentPayslips(data.recent_payslips);
}

async function loadEmployees() {
  state.employees = await api("/api/employees");
  renderEmployees();
}

async function loadDepartments() {
  state.departments = await api("/api/departments");
  renderDepartments();
}

function formPayload(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function setupEmployeeForm() {
  const form = document.querySelector("#employee-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      const payload = formPayload(form);
      payload.birth_year = Number(payload.birth_year);
      await api("/api/employees", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      form.reset();
      showToast("Employee saved successfully.");
      await Promise.all([loadEmployees(), loadDashboard()]);
    } catch (error) {
      showToast(error.message, true);
    } finally {
      button.disabled = false;
    }
  });
}

function payslipPayload(form, includeIdentifiers = true) {
  const data = formPayload(form);
  const payload = {
    base_salary: Number(data.base_salary),
    allowance_rate: Number(data.allowance_rate),
    deduction_rate: Number(data.deduction_rate),
    hours_worked: Number(data.hours_worked),
  };
  if (includeIdentifiers) {
    payload.payslip_id = data.payslip_id;
    payload.employee_id = data.employee_id;
    payload.payroll_id = data.payroll_id || null;
  }
  return payload;
}

function renderCalculation(calculation, statusText) {
  document.querySelector("#result-status").textContent = statusText;
  document.querySelector("#result-base").textContent = formatMoney(calculation.base_salary);
  document.querySelector("#result-allowance").textContent = `+ ${formatMoney(calculation.allowance_amount)}`;
  document.querySelector("#result-gross").textContent = formatMoney(calculation.gross);
  document.querySelector("#result-deduction").textContent = `− ${formatMoney(calculation.deduction_amount)}`;
  document.querySelector("#result-net").textContent = formatMoney(calculation.net);
}

function setupPayslipForm() {
  const form = document.querySelector("#payslip-form");
  const calculateButton = document.querySelector("#calculate-button");

  calculateButton.addEventListener("click", async () => {
    if (!form.reportValidity()) return;
    try {
      const calculation = await api("/api/payroll/calculate", {
        method: "POST",
        body: JSON.stringify(payslipPayload(form, false)),
      });
      renderCalculation(calculation, "Preview calculated");
      showToast("Payroll preview calculated.");
    } catch (error) {
      showToast(error.message, true);
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      const saved = await api("/api/payslips", {
        method: "POST",
        body: JSON.stringify(payslipPayload(form)),
      });
      renderCalculation(saved, "Payslip saved");
      form.reset();
      showToast(`Payslip ${saved.payslip_id} saved successfully.`);
      await loadDashboard();
    } catch (error) {
      showToast(error.message, true);
    } finally {
      button.disabled = false;
    }
  });
}

async function initialize() {
  document.querySelector("#current-date").textContent = new Intl.DateTimeFormat("en-UG", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date());
  setupNavigation();
  setupEmployeeForm();
  setupPayslipForm();

  try {
    await Promise.all([loadDashboard(), loadEmployees(), loadDepartments()]);
  } catch (error) {
    showToast(error.message, true);
  }
}

document.addEventListener("DOMContentLoaded", initialize);
