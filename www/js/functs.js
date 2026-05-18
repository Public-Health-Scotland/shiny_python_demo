document.addEventListener("DOMContentLoaded", () => {
  const year = new Date().getFullYear();
  const footerEl = document.getElementById("app-footer");

  if (footerEl) {
    footerEl.textContent = `© ${year} Public Health Scotland`;
  }
});

// Function to handle the URL hash on page load
function syncHashToShiny() {
    const currentHash = window.location.hash.replace('#', '');
    if (currentHash) {
        // Send the hash value back to Python Shiny
        Shiny.setInputValue('initial_hash', currentHash);
    }
}

// Update the hash whenever the user changes tabs
Shiny.addCustomMessageHandler('update_hash', function(hash_value) {
  window.location.hash = hash_value;
});

// Run once when the document is ready
$(document).on('shiny:connected', function(event) {
  syncHashToShiny();
});