// Table filter + nav toggle. No dependencies.
(function () {
  var q = document.getElementById('q');
  var rows = Array.prototype.slice.call(document.querySelectorAll('table.grid tbody tr'));
  var count = document.getElementById('count');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var state = 'all';

  function apply() {
    var term = (q && q.value ? q.value : '').trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (tr) {
      var text = tr.textContent.toLowerCase();
      var status = tr.getAttribute('data-status') || '';
      var flag = tr.getAttribute('data-flag') === '1';
      var okStatus = state === 'all'
        || (state === 'flag' && flag)
        || (state === 'unverified' && status === 'unverified')
        || (state === 'verified' && status === 'verified' && !flag);
      var okText = !term || text.indexOf(term) !== -1;
      var show = okStatus && okText;
      tr.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (count) count.textContent = shown + (shown === 1 ? ' row' : ' rows');
  }

  if (q) q.addEventListener('input', apply);
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('on'); });
      c.classList.add('on');
      state = c.getAttribute('data-filter');
      apply();
    });
  });
  apply();

  var toggle = document.getElementById('navtoggle');
  var nav = document.getElementById('sidenav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
