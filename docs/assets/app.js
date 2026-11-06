// Simple client-side helpers: table filtering, date stamp, print.
(function () {
  // Stamp the "last verified" footer line(s)
  document.querySelectorAll('[data-verified-date]').forEach(function (el) {
    el.textContent = '2026-11-06';
  });

  // Table filter: input[data-filter="tableId"] filters rows of table#tableId
  document.querySelectorAll('input[data-filter]').forEach(function (input) {
    var table = document.getElementById(input.getAttribute('data-filter'));
    if (!table) return;
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      table.querySelectorAll('tbody tr').forEach(function (row) {
        var text = row.textContent.toLowerCase();
        row.style.display = !q || text.indexOf(q) !== -1 ? '' : 'none';
      });
    });
  });

  // Print buttons
  document.querySelectorAll('[data-print]').forEach(function (btn) {
    btn.addEventListener('click', function () { window.print(); });
  });
})();
