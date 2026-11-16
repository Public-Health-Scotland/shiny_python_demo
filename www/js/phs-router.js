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
  document.querySelectorAll(".dropdown-toggle").forEach(toggle => {
    let dropdown = bootstrap.Dropdown.getInstance(toggle);
    if (!dropdown) dropdown = new bootstrap.Dropdown(toggle);
    dropdown.hide();
  });
}

// Update the URL and close navigation menus after a tab change.
function handleTabChange(value, smoothScroll = true) {
  if (!value) return;

  const nextHash = `#${encodeURIComponent(value)}`;
  if (getHashValue() !== value) {
    pendingHash = nextHash;
    window.location.hash = nextHash;
  }
  closeDropdownMenu();
  closeMobileMenu();

  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: smoothScroll ? "smooth" : "instant" });
  });
}

// Activate the nav link whose value matches the URL fragment.
function activateTabFromHash(isInitialLoad = false) {
  const hash = getHashValue();
  if (!hash) return false;

  const link = Array.from(
    document.querySelectorAll(".nav-link[data-value], .dropdown-item[data-value]")
  ).find(
    link => link.getAttribute("data-value") === hash
  );
  if (!link) return false;

  if (!link.classList.contains("active")) {
    // Use Bootstrap's Tab API directly if available to avoid unnecessary click overhead,
    // falling back to .click() so Shiny's tabset input binding registers the change.
    if (window.bootstrap && bootstrap.Tab) {
      bootstrap.Tab.getOrCreateInstance(link).show();
    } else {
      link.click();
    }
  }
  closeDropdownMenu();

  // Jump immediately on initial load rather than animating a scroll
  requestAnimationFrame(() => {
    window.scrollTo({ top: 0, behavior: isInitialLoad ? "instant" : "smooth" });
  });

  return true;
}

// From Python: sync hash when selected_tab changes
Shiny.addCustomMessageHandler("update_hash", value => {
  if (preserveInitialHash && value !== initialHash) return;
  if (value === initialHash) preserveInitialHash = false;
  handleTabChange(value);
});

// User clicks a tab
document.addEventListener("click", function (e) {
  if (!e.isTrusted) return;

  if (e.target.closest(".dropdown-toggle")) return;

  const link = e.target.closest(".nav-link[data-value], .dropdown-item[data-value]");
  if (!link) return;

  preserveInitialHash = false;
  const value = link.getAttribute("data-value");
  handleTabChange(value);
});

// Browser back/forward
window.addEventListener("hashchange", function () {
  if (window.location.hash === pendingHash) {
    pendingHash = null;
    return;
  }
  preserveInitialHash = false;
  activateTabFromHash(false);
});

// Run as soon as the DOM is parsed (before WebSocket connection completes)
function initRouter() {
  if (!activateTabFromHash(true)) {
    preserveInitialHash = false;
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initRouter);
} else {
  initRouter();
}

// Re-verify once Shiny connects in case dynamic tabs were rendered late
$(document).on("shiny:connected", function () {
  if (preserveInitialHash) {
    initRouter();
  }
});
