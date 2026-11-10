/* HeartCare AI front end. Plain JavaScript, no libraries. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Geometry helpers for the SVG charts ---------- */

  // Point on a half circle. deg 0 is the left end, 180 is the right end.
  function polar(cx, cy, r, deg) {
    var a = (180 - deg) * Math.PI / 180;
    return [cx + r * Math.cos(a), cy - r * Math.sin(a)];
  }

  function arc(cx, cy, r, d0, d1) {
    var p0 = polar(cx, cy, r, d0);
    var p1 = polar(cx, cy, r, d1);
    return 'M' + p0[0].toFixed(2) + ' ' + p0[1].toFixed(2) +
      ' A' + r + ' ' + r + ' 0 0 1 ' + p1[0].toFixed(2) + ' ' + p1[1].toFixed(2);
  }

  /* ---------- Prediction form ---------- */

  function initPredictForm() {
    var form = document.getElementById('predict-form');
    if (!form) { return; }

    var fields = [].slice.call(form.querySelectorAll('.field input, .field select'));
    var fill = document.getElementById('meter-fill');
    var text = document.getElementById('meter-text');
    var bar = document.getElementById('meter');
    var btn = document.getElementById('predict-btn');

    function message(el) {
      var v = el.validity;
      if (v.valueMissing) { return el.tagName === 'SELECT' ? 'Select an option.' : 'Enter a value.'; }
      if (v.badInput) { return 'Enter a number.'; }
      if (v.rangeUnderflow || v.rangeOverflow) {
        return 'Enter a value between ' + el.min + ' and ' + el.max + '.';
      }
      if (v.stepMismatch) { return el.step === '1' ? 'Enter a whole number.' : 'Enter a valid number.'; }
      return '';
    }

    function show(el) {
      var wrap = el.closest('.field');
      var msg = message(el);
      wrap.classList.toggle('has-error', !!msg);
      wrap.querySelector('.error').textContent = msg;
      if (msg) { el.setAttribute('aria-invalid', 'true'); } else { el.removeAttribute('aria-invalid'); }
      return !msg;
    }

    function progress() {
      var done = fields.filter(function (el) { return el.value !== '' && el.validity.valid; }).length;
      fill.style.width = (done / fields.length * 100) + '%';
      bar.setAttribute('aria-valuenow', done);
      text.textContent = done + ' of ' + fields.length + ' values entered';
    }

    fields.forEach(function (el) {
      el.addEventListener('input', function () {
        if (el.closest('.field').classList.contains('has-error')) { show(el); }
        progress();
      });
      el.addEventListener('change', progress);
      el.addEventListener('blur', function () { if (el.value !== '') { show(el); } });
    });

    form.addEventListener('submit', function (e) {
      var firstBad = null;
      fields.forEach(function (el) {
        if (!show(el) && !firstBad) { firstBad = el; }
      });
      if (firstBad) {
        e.preventDefault();
        firstBad.focus();
        return;
      }
      btn.disabled = true;
      btn.textContent = 'Predicting';
    });

    // Back button restores the page from cache with the button still disabled.
    window.addEventListener('pageshow', function () {
      btn.disabled = false;
      btn.textContent = 'Predict heart disease';
    });

    var alertBox = document.getElementById('form-alert');
    if (alertBox) { alertBox.focus(); }
    progress();
  }

  /* ---------- Result gauge ---------- */

  function initGauge() {
    var host = document.querySelector('.gauge');
    if (!host) { return; }
    var target = host.querySelector('.gauge__svg');

    var p = parseFloat(host.getAttribute('data-prob'));
    var lo = parseFloat(host.getAttribute('data-low-max'));
    var hi = parseFloat(host.getAttribute('data-high-min'));
    var cx = 170, cy = 165, r = 125, gap = 1.2;

    var bands = [[0, lo, 'low'], [lo, hi, 'moderate'], [hi, 100, 'high']];
    var current = p < lo ? 'low' : (p >= hi ? 'high' : 'moderate');

    var html = '<svg viewBox="0 0 340 190" focusable="false">';
    bands.forEach(function (b, i) {
      var d0 = b[0] * 1.8 + (i > 0 ? gap : 0);
      var d1 = b[1] * 1.8 - (i < 2 ? gap : 0);
      html += '<path class="seg seg-' + b[2] + (b[2] === current ? '' : ' seg--dim') +
        '" d="' + arc(cx, cy, r, d0, d1) + '"/>';
    });
    [0, lo, hi, 100].forEach(function (v) {
      var q = polar(cx, cy, r + 24, v * 1.8);
      html += '<text class="tick" x="' + q[0].toFixed(1) + '" y="' + q[1].toFixed(1) +
        '" text-anchor="middle" dominant-baseline="middle">' + v + '%</text>';
    });
    html += '<circle class="marker" r="12" cx="' + polar(cx, cy, r, 0)[0] + '" cy="' + cy + '"/></svg>';
    target.innerHTML = html;

    var marker = target.querySelector('.marker');
    function place(v) {
      var q = polar(cx, cy, r, v * 1.8);
      marker.setAttribute('cx', q[0].toFixed(2));
      marker.setAttribute('cy', q[1].toFixed(2));
    }

    if (reduceMotion) { place(p); return; }

    // One sweep from 0% to the result when the page opens.
    var start = null, duration = 900;
    function step(ts) {
      if (start === null) { start = ts; }
      var t = Math.min(1, (ts - start) / duration);
      place(p * (1 - Math.pow(1 - t, 3)));
      if (t < 1) { requestAnimationFrame(step); }
    }
    place(0);
    requestAnimationFrame(step);
  }

  /* ---------- History filter ---------- */

  function initHistory() {
    var select = document.getElementById('risk-filter');
    if (!select) { return; }
    var rows = [].slice.call(document.querySelectorAll('tbody tr[data-risk]'));
    var count = document.getElementById('row-count');
    var none = document.getElementById('no-match');

    function apply() {
      var want = select.value, shown = 0;
      rows.forEach(function (row) {
        var ok = !want || row.getAttribute('data-risk') === want;
        row.hidden = !ok;
        if (ok) { shown += 1; }
      });
      count.textContent = 'Showing ' + shown + ' of ' + rows.length + ' predictions';
      none.hidden = shown !== 0;
    }
    select.addEventListener('change', apply);
    apply();
  }

  /* ---------- Dashboard charts ---------- */

  function donut(d) {
    var host = document.getElementById('donut');
    if (!host) { return; }
    var order = [['Low', 'low'], ['Moderate', 'moderate'], ['High', 'high']];
    var total = order.reduce(function (s, o) { return s + d.risk[o[0]]; }, 0);
    if (!total) { return; }

    var R = 70, C = 2 * Math.PI * R, offset = 0;
    var h = '<svg viewBox="0 0 180 180" role="img" aria-label="Predictions by risk level">';
    h += '<circle class="donut-track" cx="90" cy="90" r="' + R + '"/>';
    order.forEach(function (o) {
      var n = d.risk[o[0]];
      if (!n) { return; }
      var len = n / total * C;
      h += '<circle class="donut-seg seg-' + o[1] + '" cx="90" cy="90" r="' + R +
        '" stroke-dasharray="' + len.toFixed(2) + ' ' + (C - len).toFixed(2) +
        '" stroke-dashoffset="' + (-offset).toFixed(2) + '" transform="rotate(-90 90 90)"/>';
      offset += len;
    });
    h += '<text class="donut-num" x="90" y="88" text-anchor="middle" dominant-baseline="central">' + total + '</text>';
    h += '<text class="donut-cap" x="90" y="112" text-anchor="middle">predictions</text></svg>';
    host.innerHTML = h;
  }

  function histogram(d) {
    var host = document.getElementById('histogram');
    if (!host) { return; }
    var bins = d.histogram, lo = d.low_max, hi = d.high_min;
    var W = 520, H = 240, L = 34, R = 24, T = 18, B = 30;
    var pw = W - L - R, ph = H - T - B;

    var top = Math.max.apply(null, bins);
    var step = Math.max(1, Math.ceil(top / 4));
    var max = step * 4;

    var h = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Number of predictions in each 10 percent band of probability">';
    for (var i = 0; i <= 4; i++) {
      var y = T + ph - ph * i / 4;
      h += '<line class="grid-line" x1="' + L + '" x2="' + (W - R) + '" y1="' + y + '" y2="' + y + '"/>';
      h += '<text class="axis-text" x="' + (L - 8) + '" y="' + y + '" text-anchor="end" dominant-baseline="middle">' + (step * i) + '</text>';
    }

    var bw = pw / 10;
    bins.forEach(function (n, idx) {
      if (!n) { return; }
      var centre = idx * 10 + 5;
      var band = centre < lo ? 'low' : (centre >= hi ? 'high' : 'moderate');
      var bh = ph * n / max;
      var x = L + idx * bw + 3;
      var yy = T + ph - bh;
      h += '<rect class="bar bar-' + band + '" x="' + x.toFixed(1) + '" y="' + yy.toFixed(1) +
        '" width="' + (bw - 6).toFixed(1) + '" height="' + bh.toFixed(1) + '" rx="3"/>';
      h += '<text class="bar-n" x="' + (x + (bw - 6) / 2).toFixed(1) + '" y="' + (yy - 5).toFixed(1) +
        '" text-anchor="middle">' + n + '</text>';
    });
    for (var k = 0; k <= 10; k += 2) {
      h += '<text class="axis-text" x="' + (L + k * bw) + '" y="' + (H - 8) + '" text-anchor="middle">' + (k * 10) + '%</text>';
    }
    h += '</svg>';
    host.innerHTML = h;
  }

  function initDashboard() {
    var el = document.getElementById('dash-data');
    if (!el) { return; }
    var data = JSON.parse(el.textContent);
    donut(data);
    histogram(data);
  }

  document.addEventListener('DOMContentLoaded', function () {
    initPredictForm();
    initGauge();
    initHistory();
    initDashboard();
  });
})();
