document.addEventListener("DOMContentLoaded", () => {
  const year = new Date().getFullYear();
  const footerEl = document.getElementById("app-footer");

  if (footerEl) {
    footerEl.textContent = `© ${year} Public Health Scotland`;
  }
});

Shiny.addCustomMessageHandler('update_url', function(message) {
    console.log("Received message from Python:", message);
    
    const url = new URL(window.location);
    url.searchParams.set(message.key, message.value);
    
    // This line actually changes the browser's address bar
    window.history.pushState({}, '', url);
});
