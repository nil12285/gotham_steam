document.addEventListener("DOMContentLoaded", function () {
    if (document.body?.id !== "wagtail") return;

    document.querySelectorAll(
        'form input:not([type="checkbox"]):not([type="radio"]):not([type="file"]):not([type="submit"]), ' +
        'form textarea'
    ).forEach(function (el) {
        el.classList.add("form-control");
    });

    document.querySelectorAll('form select').forEach(function (el) {
        el.classList.add("form-select");
    });
});