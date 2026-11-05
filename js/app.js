/* Static replica interactivity: contact modal open/close, form validation. */
(function () {
  'use strict';

  var modal = document.getElementById('contact-modal');
  if (!modal) return;

  function open() {
    modal.hidden = false;
    document.body.classList.add('modal-open');
    var first = modal.querySelector('input, select, textarea, button');
    if (first) first.focus();
  }

  function close() {
    modal.hidden = true;
    document.body.classList.remove('modal-open');
  }

  document.querySelectorAll('[data-modal-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });

  // Any "Contact Property" CTA opens the enquiry modal.
  document.querySelectorAll('a.btn-cta--contact, .btn-cta--fifteen').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      open();
    });
  });

  modal.addEventListener('mousedown', function (e) {
    if (e.target === modal || e.target.classList.contains('vfm__overlay')) close();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) close();
  });

  // "View Phone Number" reveals the leasing office phone, as on the live form.
  var reveal = modal.querySelector('[data-reveal-phone]');
  if (reveal) {
    reveal.addEventListener('click', function (e) {
      e.preventDefault();
      var h4 = reveal.closest('h4');
      if (h4) h4.textContent = 'Avenue Living @ (825) 425-2719';
    });
  }

  var form = modal.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;
      form.querySelectorAll('[required]').forEach(function (field) {
        var empty = !field.value.trim();
        field.classList.toggle('field--error', empty);
        if (empty) valid = false;
      });
      if (valid) close();
    });
    form.addEventListener('input', function (e) {
      if (e.target.matches('[required]')) {
        e.target.classList.toggle('field--error', !e.target.value.trim());
      }
    });
  }

  // Match the live page's element state: modal starts closed.
  close();
})();
