document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("theme_mode");
  if (!select) return;

  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  let userHasChosen = false;
  let syncingFromSystem = false;

  select.addEventListener("change", () => {
    if (!syncingFromSystem) userHasChosen = true;
    document.documentElement.setAttribute("data-bs-theme", select.value);
  });

  const syncWithSystem = () => {
    if (userHasChosen) return;

    syncingFromSystem = true;
    select.value = systemTheme.matches ? "dark" : "light";
    select.dispatchEvent(new Event("change", { bubbles: true }));
    syncingFromSystem = false;
  };

  syncWithSystem();
  systemTheme.addEventListener("change", syncWithSystem);
});

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
