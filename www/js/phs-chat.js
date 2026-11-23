Shiny.addCustomMessageHandler("setChatState", function(message) {
    const el = document.getElementById(message.id);

    if (!el) return;

    if (message.enabled) {
        el.classList.remove("disabled");
        el.removeAttribute("aria-disabled");
    } else {
        el.classList.add("disabled");
        el.setAttribute("aria-disabled", "true");

        // Close the chat if it is open
        el.closest("details")?.removeAttribute("open");
    }
});
