document.addEventListener("DOMContentLoaded", () => {
  const year = new Date().getFullYear();
  const footerEl = document.getElementById("app-footer");

  if (footerEl) {
    footerEl.textContent = `© ${year} Public Health Scotland`;
  }
});


