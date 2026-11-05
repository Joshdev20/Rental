"""Assemble the static replica markup from the captured rentals.ca DOM."""
import re
from bs4 import BeautifulSoup, Comment

SRC = '/workspace/project/tools/parts'
OUT = '/workspace/project'

def read(p):
    return open(f'{SRC}/{p}', encoding='utf-8', errors='replace').read()

# ---- photo mapping: property images -> local files, in order of appearance ----
page_raw = read('part_page.html')
photo_urls = list(dict.fromkeys(re.findall(
    r'https://images\.rentals\.ca/property-pictures/medium/calgary-ab/552603/[a-z0-9-]+\.jpg', page_raw)))
photo_map = {u: f'assets/img/photos/photo-{i+1:02d}.jpg' for i, u in enumerate(photo_urls)}

FA_RE = re.compile(r'<svg[^>]*class="([^"]*svg-inline--fa[^"]*)"[^>]*data-icon="([^"]+)"[^>]*data-prefix="([^"]+)"[^>]*>.*?</svg>', re.S)

def clean(html):
    soup = BeautifulSoup(html, 'lxml')
    # strip comments
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    # strip vue scope attributes
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr in ('data-fa-i2svg', 'data-current-language', 'data-msgid'):
                del tag.attrs[attr]
    # rewrite image sources
    def src(v):
        if not v:
            return v
        if v in photo_map:
            return photo_map[v]
        if v.startswith('/static/fe/img/social-icons/'):
            return 'assets/img/social-icons/' + v.rsplit('/', 1)[1]
        if v.startswith('/static/fe/img/'):
            return 'assets/img/' + v.rsplit('/', 1)[1]
        return v
    for img in soup.find_all('img'):
        if img.get('src'):
            img['src'] = src(img['src'])
        if img.get('srcset'):
            img['srcset'] = ', '.join(
                src(p.strip().split(' ')[0]) + (' ' + p.strip().split(' ')[1] if len(p.strip().split(' ')) > 1 else '')
                for p in img['srcset'].split(','))
    # The inline Font Awesome <svg> markup is preserved verbatim: the site's
    # stylesheet targets those `svg` elements directly, so replacing them with
    # `<i>` icon fonts changes sizing and spacing.
    return str(soup)

def body_of(html):
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body or soup
    parts = [str(c) for c in body.find_all(recursive=False)]
    return '\n'.join(parts)

nav = body_of(clean(read('part_nav.html')))
page = body_of(clean(read('part_page.html')))
footer = body_of(clean(read('part_footer.html')))

# drop the hidden SEO block (duplicate of the visible page)
page = re.sub(r'<div class="listing-details-ssr".*?</div>\s*(?=<nav class="navbar-listing-details")', '', page, flags=re.S)

# ---- contact modal (listing-lead-form) markup, hand-built from the LeadForm source ----
# Scope attributes (data-v-*) are kept so the page's own scoped component CSS applies,
# exactly as Vue would emit them for these components.
S = ' data-v-46d1f420'   # ListingContactBody
F = ' data-v-c26fe320'   # ListingLeadForm
MODAL = f'''
<div class="vfm__container vfm--fixed vfm--inset" id="contact-modal" hidden>
  <div class="vfm__overlay vfm--absolute vfm--inset" data-modal-close></div>
  <div class="vfm__content modal modal-listing-contact rounded modal__form" role="dialog" aria-modal="true" aria-labelledby="contact-modal-title"{S}>
    <div class="modal-listing-contact__header"{S}>
      <div class="modal-listing-contact__header--title mb-2"{S}>
        <h3 id="contact-modal-title"{S}>Get In Touch</h3>
        <button class="modal__close" type="button" data-modal-close aria-label="Close"{S}>
          ×
        </button>
      </div>
      <div class="modal-listing-contact__header__subheader"{S}>
        <div class="modal-listing-contact__header__subheader__name-and-address"{S}>
          <p class="modal-listing-contact__property-name"{S}>Applewood Village</p>
          <address{S}>3805 Marlborough Dr NE, Calgary,&nbsp;AB</address>
        </div>
        <div class="listing-lead-phone"{S}>
          <h4{S}><a href="#" data-reveal-phone{S}><svg aria-hidden="true" class="svg-inline--fa fa-phone" data-icon="phone" data-prefix="far" role="img" viewBox="0 0 512 512"><path fill="currentColor" d="M112.8 10.9c27.3-9.1 57 3.9 68.9 30l39.7 87.3c10.6 23.4 4 51-16 67.1l-24.2 19.3c25.5 50 65.5 91.4 114.4 118.8l21.2-26.6c16.1-20.1 43.7-26.7 67.1-16l87.3 39.7c26.2 11.9 39.1 41.6 30 68.9-20.7 62.3-83.7 116.2-160.9 102.6-173.7-30.6-299.6-156.5-330.2-330.2-13.6-77.2 40.4-140.1 102.6-160.9zm25.2 49.9c-1.7-3.8-6-5.7-10-4.4-45.2 15.1-79.1 58.6-70.5 107 27.1 153.8 137.4 264.2 291.2 291.3 48.4 8.5 91.9-25.3 107-70.5 1.3-4-.6-8.3-4.4-10L364 334.4c-3.4-1.5-7.4-.6-9.7 2.3l-33.5 41.9c-7 8.7-19 11.5-29 6.7-72.5-34.4-130.5-94.3-162.4-168.2-4.3-9.9-1.4-21.5 7-28.2l38.9-31.1c2.9-2.3 3.9-6.3 2.3-9.7L137.9 60.7z"></path></svg> View Phone Number</a></h4>
        </div>
      </div>
    </div>
    <div class="modal-listing-contact__body"{S}>
      <form class="listing-lead-form form" method="post" novalidate{F}>
        <div class="listing-lead-form__fields"{F}>
          <div class="row d-none"{F}>
            <input type="text" name="spam_name" tabindex="-1" autocomplete="disabled"{F}>
            <input type="tel" name="spam_phone" tabindex="-1" autocomplete="disabled"{F}>
            <input type="email" name="spam_email" tabindex="-1" autocomplete="disabled"{F}>
          </div>
          <div class="row mt-3"{F}>
            <div class="form__group col col-sm-6"{F}>
              <label for="lead-name"{F}>Name<span class="mandatory-star"{F}>*</span></label>
              <div class="field-clearable"{F}>
                <input id="lead-name" name="full_name" type="text" required placeholder="Enter your name"{F}>
              </div>
            </div>
            <div class="form__group col col-sm-6"{F}>
              <label for="lead-phone"{F}>Phone</label>
              <div class="field-clearable"{F}>
                <input id="lead-phone" name="phone" type="tel" placeholder="Enter your phone number"{F}>
              </div>
            </div>
          </div>
          <div class="row"{F}>
            <div class="form__group col col-sm-6"{F}>
              <label for="lead-email"{F}>Email<span class="mandatory-star"{F}>*</span></label>
              <div class="field-clearable"{F}>
                <input id="lead-email" name="email" type="email" required placeholder="Enter your email"{F}>
              </div>
            </div>
            <div class="form__group col col-sm-6"{F}>
              <label for="lead-unit"{F}>Unit</label>
              <select id="lead-unit" name="unit"{F}>
                <option value="23824706">$1,410 - 1 Bedroom</option>
                <option value="23824707">$1,720 - 2 Bedroom</option>
              </select>
            </div>
          </div>
          <div class="row"{F}>
            <div class="form__group col"{F}>
              <label for="lead-message"{F}>Your Message<span class="mandatory-star"{F}>*</span></label>
              <div class="field-clearable field-clearable--textarea"{F}>
                <textarea id="lead-message" name="message" class="listing-lead-form__message" rows="4" placeholder="Enter your message"{F}>I came across your listing for 3805 Marlborough Dr NE, Calgary and would be interested in seeing the place. What are the next steps?</textarea>
              </div>
            </div>
          </div>
          <div class="row"{F}>
            <div class="form__group form__group--user-consent col"{F}>
              <div class="listing-lead-form__user-consent"{F}>
                <label class="switcher-checkbox switcher-checkbox--active"{F}>
                  <input type="checkbox" checked{F}>
                </label>
                <span class="ml-4"{F}>Email me similar listings &amp; info</span>
              </div>
            </div>
          </div>
          <div class="row listing-lead-form__legal-row"{F}>
            <div class="form__group col"{F}>
              <p class="legal"{F}>By submitting this inquiry, you agree to our <a href="#" target="_blank"{F}>Terms of Service</a> and <a href="#" target="_blank"{F}>Privacy Policy</a>, and consent to be contacted by phone, text, and/or email regarding your inquiry.</p>
            </div>
          </div>
        </div>
        <div class="listing-lead-form__action-footer"{F}>
          <div class="row listing-lead-form__footer"{F}>
            <div class="form__group col-auto d-flex align-items-center mb-0 pr-md-0"{F}>
              <button type="submit" class="btn-cta btn-cta--sm btn-cta--nineteen btn-cta--tall"{F}>
                <svg aria-hidden="true" class="svg-inline--fa fa-envelope btn-cta__icon" data-icon="envelope" data-prefix="far" role="img" viewBox="0 0 512 512"><path fill="currentColor" d="M464 64H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V112c0-26.51-21.49-48-48-48zm0 48v40.805c-22.422 18.259-58.168 46.651-134.587 106.49-16.841 13.247-50.201 45.072-73.413 44.701-23.208.375-56.579-31.459-73.413-44.701C106.18 199.465 70.425 171.067 48 152.805V112h416zM48 400V214.398c22.914 18.251 55.409 43.862 104.938 82.646 21.857 17.205 60.134 55.186 103.062 54.955 42.717.231 80.509-37.199 103.053-54.947 49.528-38.783 82.032-64.401 104.947-82.653V400H48z"></path></svg>
                Contact Property
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>
'''

html = f'''<!DOCTYPE html>
<html lang="en" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>Applewood Village - 3805 Marlborough Dr NE, Calgary, AB</title>
<meta name="description" content="3805 Marlborough Dr NE is an apartment for rent in Calgary, AB. It is a 1-2 bedroom apartment in the Applewood Village building.">
<link rel="icon" type="image/png" href="assets/img/favicon-32x32.png">
<link rel="stylesheet" href="css/fontawesome.css">
<link rel="stylesheet" href="css/styles.css">
<link rel="stylesheet" href="css/replica.css">
</head>
<body>
<div id="app">
{nav}
{page}
{footer}
</div>
{MODAL}
<script src="js/app.js"></script>
</body>
</html>
'''

open(f'{OUT}/index.html', 'w', encoding='utf-8').write(html)
print('index.html', len(html))
