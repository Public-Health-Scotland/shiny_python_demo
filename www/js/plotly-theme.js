document.addEventListener("DOMContentLoaded", function() {
    // Store plot data globally by container target ID
    const plotsStore = {};

    // Custom theme configurations
    const customThemes = {
        phs_dark: {
            bg: "#1a1a2e",
            fontColor: "#e8e8e8",
            colorway: [
                "#0078D4", "#C73918", "#1E7F84", "#9B4393", "#3393DD",
                "#6B5C85", "#AF69A9", "#3F3685", "#948DA3", "#655E9D"
            ]
        },
        phs_ggplot2: {
            bg: "#ffffff",
            fontColor: "#333333",
            colorway: [
                "#3F3685", "#C73918", "#1E7F84", "#3393DD", "#9B4393",
                "#0078D4", "#AF69A9", "#6B5C85", "#948DA3", "#655E9D"
            ]
        }
    };

    function getThemeParams() {
        const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";
        const themeKey = isDark ? "phs_dark" : "phs_ggplot2";
        const activeConfig = customThemes[themeKey];

        return {
            template: themeKey,
            bg: activeConfig.bg,
            fontColor: activeConfig.fontColor,
            colorway: activeConfig.colorway
        };
    }

    // Helper to strip explicit trace colors so layout.colorway takes precedence
    function cleanTraceColors(dataArray) {
        if (!Array.isArray(dataArray)) return dataArray;

        return dataArray.map(trace => {
            // Deep clone trace object
            const cleanTrace = JSON.parse(JSON.stringify(trace));

            // Remove explicit marker colors set by Plotly Express
            if (cleanTrace.marker) {
                delete cleanTrace.marker.color;
            }
            if (cleanTrace.line) {
                delete cleanTrace.line.color;
            }

            return cleanTrace;
        });
    }

    function ensureResponsiveObserver(targetId, plotContainer) {
        if (plotContainer.dataset.resizeObserverBound === "true") return;

        if (typeof ResizeObserver !== "undefined") {
            const resizeObserver = new ResizeObserver(() => {
                if (document.getElementById(targetId) && window.Plotly) {
                    Plotly.Plots.resize(plotContainer);
                }
            });

            resizeObserver.observe(plotContainer);
            plotContainer.dataset.resizeObserverBound = "true";
            plotContainer._plotlyResizeObserver = resizeObserver;
        }
    }

    // Render or update a single plot element
    function renderPlot(targetId) {
        const plotContainer = document.getElementById(targetId);
        const plotData = plotsStore[targetId];

        if (!plotContainer || !plotData || !window.Plotly) return;

        const theme = getThemeParams();

        // Deep clone layout to prevent in-place mutation issues
        const layout = JSON.parse(JSON.stringify(plotData.layout || {}));
        layout.autosize = true;

        // Apply theme settings
        layout.template = theme.template;
        layout.paper_bgcolor = theme.bg;
        layout.plot_bgcolor = theme.bg;
        layout.font = layout.font || {};
        layout.font.color = theme.fontColor;
        layout.colorway = theme.colorway;

        // Clean trace data so colorway is enforced
        const cleanedData = cleanTraceColors(plotData.data);
        const config = {
            ...(plotData.config || {}),
            responsive: true,
            displayModeBar: false
        };

        // Apply ARIA accessibility attributes to the container
        if (plotData["aria-label"]) {
            plotContainer.setAttribute("role", "img");
            plotContainer.setAttribute("aria-label", plotData["aria-label"]);
            plotContainer.setAttribute("tabindex", "0");
        }

        Plotly.react(plotContainer, cleanedData, layout, config);
        ensureResponsiveObserver(targetId, plotContainer);
    }

    // Re-theme ALL registered plots client-side instantly
    function rethemeAllPlots() {
        Object.keys(plotsStore).forEach(targetId => {
            renderPlot(targetId);
        });
    }

    // 1. Unified custom message handler for any chart ID
    Shiny.addCustomMessageHandler("render_plotly_chart", function(message) {
        const targetId = message.target;
        plotsStore[targetId] = message; // Store payload
        renderPlot(targetId);
    });

    // 2. Client-side theme observer
    const themeObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === "attributes" && mutation.attributeName === "data-bs-theme") {
                rethemeAllPlots();
            }
        });
    });

    themeObserver.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-bs-theme"]
    });
});
