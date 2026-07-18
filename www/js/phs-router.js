// Read hash on load and activate correct tab
function activateTabFromHash() {
    const hash = window.location.hash.slice(1);
    if (!hash) return;

    const link = document.querySelector(`a[data-value="${hash}"]`);
    if (link) {
        link.click();
        // Scroll after tab activation
        requestAnimationFrame(() => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
}

// Close dropdown menu when hash changes
function closeDropdownMenu() {
  const dropdownToggle = document.querySelector('.dropdown-toggle');  
  if (dropdownToggle) {
    // Remove Bootstrap's "show" class
    dropdownToggle.classList.remove('show');
    dropdownToggle.setAttribute('aria-expanded', 'false');
    
    // Also hide the dropdown menu
    const dropdownMenu = dropdownToggle.nextElementSibling;
    if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
      dropdownMenu.classList.remove('show');
    }
  }
}

// When Python Shiny sends a message → update hash + scroll
Shiny.addCustomMessageHandler("update_hash", function(value) {
    window.location.hash = value;
    closeDropdownMenu();
    requestAnimationFrame(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});

// When user clicks a tab → update hash + scroll
document.addEventListener("click", function(e) {
    const link = e.target.closest("a[data-value]");
    if (link) {
        const value = link.getAttribute("data-value");
        window.location.hash = value;

        requestAnimationFrame(() => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
});

// Close menu when hash changes via back/forward buttons
window.addEventListener('hashchange', closeDropdownMenu);

// Run once when Shiny is ready
$(document).on("shiny:connected", function() {
    activateTabFromHash();
});
