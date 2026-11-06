/* Minimal progressive enhancement: client-side row filter for long tables.
   The site is fully usable with JavaScript disabled. */
(function () {
  "use strict";

  function attach(input) {
    var key = input.getAttribute("data-filter");
    var table = document.querySelector('table[data-rows="' + key + '"]');
    if (!table) return;
    var rows = table.tBodies[0].rows;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      for (var i = 0; i < rows.length; i++) {
        var text = rows[i].textContent.toLowerCase();
        rows[i].style.display = !q || text.indexOf(q) !== -1 ? "" : "none";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var inputs = document.querySelectorAll("input[data-filter]");
    for (var i = 0; i < inputs.length; i++) attach(inputs[i]);
  });
})();
