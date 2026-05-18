// Change navbar height variable based on scroll position
window.addEventListener("scroll", function () {
  const root = document.documentElement;

  if (window.scrollY > 50) {
    // Switch to scrolled height
    root.style.setProperty("--navbar-height", "var(--navbar-height-scrolled)");
  } else {
    // Switch back to normal height
    root.style.setProperty("--navbar-height", "var(--navbar-height-default)");
  }
});
