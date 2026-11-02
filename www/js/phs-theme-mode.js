/** this function listens for changes to any input with name "mode" 
  (the segmented control) and updates the theme accordingly.
  */
function labelTheme(html){
  let theme = html.getAttribute("data-bs-theme");
  let label = document.getElementById("theme-label");
  label.textContent = "Selected " + theme;
  return theme;
}

document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    theme = labelTheme(html);
    const observer = new MutationObserver(() => {
        theme = labelTheme(html);
    });

    observer.observe(html, {
        attributes: true,
        attributeFilter: ["data-bs-theme"],
    });
});
