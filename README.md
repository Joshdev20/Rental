# Rentals.ca listing page replica

A static, front-end-only replica of the Rentals.ca property listing page for
**Applewood Village – 3805 Marlborough Dr NE, Calgary, AB**
(<https://rentals.ca/calgary/3805-marlborough-dr-ne>).

No backend or build step is required to view it: open `index.html`, or serve the
folder with any static server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## What's included

- `index.html` – the full page markup (nav, listing, footer) plus the contact
  enquiry modal.
- `css/styles.css` – the site stylesheet (component styles, including the
  scoped `data-v-*` rules used by the modal).
- `css/fontawesome.css` – Font Awesome icon rules.
- `css/replica.css` – small shims for the modal chrome.
- `js/app.js` – vanilla-JS interactivity: open/close the contact modal, reveal
  the phone number, and validate the enquiry form.
- `assets/` – fonts, property photos, icons and badges.

## Contact modal

The "Contact Property" call-to-action opens a contact/enquiry modal built from
the real `listing-lead-form` component markup, with matching scoped styles. It
closes on the × button, the overlay, or `Esc`, reveals the leasing phone number,
and validates the required fields before submitting.

## Rebuilding

`index.html` is assembled from the captured page fragments in `tools/parts/`:

```bash
pip install beautifulsoup4 lxml
python3 tools/build.py
```
