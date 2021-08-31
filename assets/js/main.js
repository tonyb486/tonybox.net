// Mildly complicated dark mode logic, but it seems to work!
function updateDarkMode(darkModePreference) {
    // Based on the user's preference, we decide if we want dark mode or not.
    // if the localstorage is set to "toggle," then we toggle it to the opposite of that preference.
    darkModeToggled = (localStorage.getItem("darkmode") == "toggle");
    document.body.className = (darkModeToggled ? !darkModePreference : darkModePreference) ? "dark" : null;
}

document.addEventListener('DOMContentLoaded', function() {
    darkMode = window.matchMedia('(prefers-color-scheme: dark)');
    darkMode.addListener(function(e) { updateDarkMode(e.matches); })
    updateDarkMode(darkMode.matches);
});

function toggle_darkmode() {
    var newToggle = ((localStorage.getItem("darkmode") == "toggle") ? "default" : "toggle")
    localStorage.setItem("darkmode", newToggle);
    updateDarkMode(window.matchMedia('(prefers-color-scheme: dark)').matches);
}

// Menu Toggle for Mobile
function toggle_menu() {
    var menu = document.getElementById("menu");
    menu.className = (menu.className == "hidden") ? "shown" : "hidden"
}