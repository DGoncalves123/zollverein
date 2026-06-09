/* Sticky waypoint bar: reflects the section in view, and a tap-to-jump menu.
   Progressive enhancement — the page is fully readable without it. */
(function () {
  "use strict";

  var toggle = document.getElementById("routeToggle");
  var menu = document.getElementById("routeMenu");
  var here = document.getElementById("waybarHere");
  var chapters = Array.prototype.slice.call(
    document.querySelectorAll("[data-here]")
  );

  if (!toggle || !menu) return;

  // --- Route menu open/close ---
  function setOpen(open) {
    menu.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  }
  toggle.addEventListener("click", function () {
    setOpen(menu.hidden);
  });
  // Close after tapping a destination, and on outside tap / Escape.
  menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) setOpen(false);
  });
  document.addEventListener("click", function (e) {
    if (!menu.hidden && !e.target.closest("#waybar")) setOpen(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !menu.hidden) setOpen(false);
  });

  // --- Reflect current section in the waybar label ---
  if ("IntersectionObserver" in window && here && chapters.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            here.textContent = entry.target.getAttribute("data-here");
          }
        });
      },
      // Trigger when a section crosses the band just below the sticky bar.
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    chapters.forEach(function (c) {
      io.observe(c);
    });
  }
})();
