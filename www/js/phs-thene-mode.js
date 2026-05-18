/** this function listens for changes to any input with name "mode" 
  (the segmented control) and updates the theme accordingly.
  */
function labelTheme(html){
  let theme = html.getAttribute("data-bs-theme");
  let label = document.getElementById("theme-label");
  label.textContent = "Selected " + theme;
  return theme;
}

function updatePlotlyTheme(theme) {
    let isDark = theme === "dark";
    const template = isDark ? "plotly_dark" : "ggplot2";
    console.log("Updating Plotly to:", template);

    // Find all Plotly charts
    //let plots = document.querySelectorAll(".plotly-graph-div.js-plotly-plot");
    const plots = document.querySelectorAll(".js-plotly-plot");

    plots.forEach(plot => {
      const data = plot.data;
      const layout = plot.layout;

      // Remove template and layout overrides
      delete layout.template;

      // Rebuild the figure with the new template
      //Plotly.react(plot, data, { ...layout, template: template });
      Plotly.newPlot(plot, data, { ...layout, template: template });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    theme = labelTheme(html);
    //updatePlotlyTheme(theme);
    const observer = new MutationObserver(() => {
        theme = labelTheme(html);
        //updatePlotlyTheme(theme);
    });

    observer.observe(html, {
        attributes: true,
        attributeFilter: ["data-bs-theme"],
    });

    // 2. Re-apply theme when switching nav panels
    // 2. Watch for nav panel changes (Bootstrap 5)
    // document.querySelectorAll('a[data-bs-toggle="tab"]').forEach(tab => {
    //     tab.addEventListener("shown.bs.tab", () => {
    //       setTimeout(() => {
    //         theme = labelTheme(html);
    //         updatePlotlyTheme(theme);
    //       }, 50); // 50ms is enough
    //     });
    // });
});

// document.addEventListener("DOMContentLoaded", () => {
//     const btn = document.getElementById("theme_mode");
//     console.log("Button element:", btn);

//     if (!btn) return;

//     btn.addEventListener("click", () => {
//         console.log("Dark mode button clicked");
//     });
// });

