const page = window.location.href.split('?')[0];
const navs = document.getElementsByClassName("nav");

for (var nav in navs) {
    navPage = navs[nav].href
    if (navPage == page) {
        navs[nav].id = "current-page";
        break;
    }
}