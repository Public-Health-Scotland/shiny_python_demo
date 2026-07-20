// Prevent loops between hashchange and tab clicks
let suppressHashHandler = false;

function closeMobileMenu() {
  const mobileMenu = document.querySelector(".navbar-collapse.show");
  if (mobileMenu) {
    const bsCollapse = bootstrap.Collapse.getInstance(mobileMenu);
    if (bsCollapse) {
      bsCollapse.hide();
    }
  }
}

// Close all dropdown menus via Bootstrap
function closeDropdownMenu() {
  document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    let dropdown = bootstrap.Dropdown.getInstance(toggle);
    if (!dropdown) dropdown = new bootstrap.Dropdown(toggle);
    dropdown.hide();
  });
}

// Common handler for "tab changed"
function handleTabChange(value) {
  if (!value) return;

  suppressHashHandler = true;
  window.location.hash = value;
  closeDropdownMenu();
  closeMobileMenu();

  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  setTimeout(() => (suppressHashHandler = false), 50);
}

// Activate tab based on current hash
function activateTabFromHash() {
  const hash = window.location.hash.slice(1);
  if (!hash) return;

  const link = document.querySelector(
    `[data-value="${hash}"], .dropdown-menu [data-value="${hash}"]`
  );
  if (!link) return;

  suppressHashHandler = true;
  link.click();
  closeDropdownMenu();

  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  setTimeout(() => (suppressHashHandler = false), 50);
}

// From Python: sync hash when selected_tab changes
Shiny.addCustomMessageHandler("update_hash", handleTabChange);

// User clicks a tab
document.addEventListener("click", function (e) {
  // Let Bootstrap handle opening the dropdown menu
  if (e.target.closest(".dropdown-toggle")) return;

  const link = e.target.closest("[data-value]");
  if (!link) return;

  const value = link.getAttribute("data-value");
  handleTabChange(value);
});

// Browser back/forward
window.addEventListener("hashchange", function () {
  if (suppressHashHandler) return;
  activateTabFromHash();
});

// On initial connect: honor hash if present
$(document).on("shiny:connected", function () {
  activateTabFromHash();
});
