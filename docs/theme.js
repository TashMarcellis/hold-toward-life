(function () {
  var root = document.documentElement;
  var btn = document.getElementById("theme");
  function sync() {
    var dark = root.dataset.theme === "dark";
    btn.setAttribute("aria-pressed", dark ? "true" : "false");
    btn.textContent = dark ? "Light mode" : "Dark mode";
  }
  btn.addEventListener("click", function () {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    try { localStorage.setItem("htl-theme", root.dataset.theme); } catch (e) {}
    sync();
  });
  sync();
})();
