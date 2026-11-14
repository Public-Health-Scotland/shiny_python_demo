let pendingHash = null;
let initialHash = getHashValue();
let preserveInitialHash = Boolean(initialHash);

// Read the URL fragment and decode it for matching against nav values.
function getHashValue() {
  const hash = window.location.hash.slice(1);
  try {
    return decodeURIComponent(hash);
  } catch {
    return hash;
  }
}

// Hide the mobile navigation menu when a tab is selected.
function closeMobileMenu() {
  const mobileMenu = document.querySelector(".navbar-collapse.show");
  if (mobileMenu) {
    const bsCollapse = bootstrap.Collapse.getInstance(mobileMenu);
    if (bsCollapse) {
      bsCollapse.hide();
    }
  }
}

// Close all open Bootstrap dropdown menus.
function closeDropdownMenu() {
  // Ensure each dropdown has a Bootstrap instance before hiding it.
  document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    let dropdown = bootstrap.Dropdown.getInstance(toggle);
    if (!dropdown) dropdown = new bootstrap.Dropdown(toggle);
    dropdown.hide();
  });
}

// Update the URL and close navigation menus after a tab change.
function handleTabChange(value) {
  if (!value) return;

  const nextHash = `#${encodeURIComponent(value)}`;
  if (getHashValue() !== value) {
    pendingHash = nextHash;
    window.location.hash = nextHash;
  }
  closeDropdownMenu();
  closeMobileMenu();

  // Scroll to the top after the current frame's layout work.
  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// Activate the nav link whose value matches the URL fragment.
function activateTabFromHash() {
  const hash = getHashValue();
  if (!hash) return false;

  // Find the link corresponding to the current fragment.
  const link = Array.from(
    document.querySelectorAll(".navbar a[data-value]")
  ).find(
    link => link.getAttribute("data-value") === hash
  );
  if (!link) return false;

  if (!link.classList.contains("active")) {
    link.click();
  }
  closeDropdownMenu();

  // Scroll to the top after the tab has been activated.
  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  return true;
}

// From Python: sync hash when selected_tab changes
// Ignore an initial server value that would overwrite a deep link.
Shiny.addCustomMessageHandler("update_hash", value => {
  if (preserveInitialHash && value !== initialHash) return;
  if (value === initialHash) preserveInitialHash = false;
  handleTabChange(value);
});

// User clicks a tab
// Keep the URL in sync while leaving Bootstrap and Shiny click handling intact.
document.addEventListener("click", function (e) {
  if (!e.isTrusted) return;

  // Let Bootstrap handle opening the dropdown menu
  if (e.target.closest(".dropdown-toggle")) return;

  const link = e.target.closest(".navbar a[data-value]");
  if (!link) return;

  preserveInitialHash = false;
  const value = link.getAttribute("data-value");
  handleTabChange(value);
});

// Browser back/forward
// Ignore the router's own hash update; otherwise activate the requested tab.
window.addEventListener("hashchange", function () {
  if (window.location.hash === pendingHash) {
    pendingHash = null;
    return;
  }
  preserveInitialHash = false;
  activateTabFromHash();
});

// On initial connect: honor hash if present
// Activate a deep-linked tab after Shiny has connected.
$(document).on("shiny:connected", function () {
  if (!activateTabFromHash()) {
    preserveInitialHash = false;
  }
});
