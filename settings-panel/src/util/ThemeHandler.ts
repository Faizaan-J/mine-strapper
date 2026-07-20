const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

const updateTheme = (event: MediaQueryListEvent) => {
    if (event.matches) {
        document.documentElement.setAttribute("data-theme", "dark");
    } else {
        document.documentElement.setAttribute("data-theme", "light");
    }
}

updateTheme(mediaQuery as unknown as MediaQueryListEvent);

mediaQuery.addEventListener("change", updateTheme);