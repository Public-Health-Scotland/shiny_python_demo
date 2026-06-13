// Function to handle the URL hash on page load
function syncHashToShiny() {
    const currentHash = window.location.hash.replace('#', '');
    if (currentHash) {
        // Send the hash value back to Python Shiny
        Shiny.setInputValue('initial_hash', currentHash);
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

// Update the hash whenever the user changes tabs
Shiny.addCustomMessageHandler('update_hash', function(hash_value) {
  window.location.hash = hash_value;
  closeDropdownMenu();
});

// Close menu when hash changes via back/forward buttons
window.addEventListener('hashchange', function() {
    closeDropdownMenu();
});

// Run once when the document is ready
$(document).on('shiny:connected', function(event) {
  syncHashToShiny();
});
