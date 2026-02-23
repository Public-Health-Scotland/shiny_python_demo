document.addEventListener("DOMContentLoaded", () => {
  const year = new Date().getFullYear();
  const footerEl = document.getElementById("app-footer");

  if (footerEl) {
    footerEl.textContent = `© Developed by Data science team - ${year}`;
  }
});