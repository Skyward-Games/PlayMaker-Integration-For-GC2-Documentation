// Progressive enhancement: generated navigation and content also work without JS.
const root = document.documentElement;
const themeButtons = [...document.querySelectorAll('[data-theme-toggle]')];
function syncThemeButtons() {
  const dark = root.dataset.theme === 'dark';
  themeButtons.forEach(button => {
    button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    button.querySelector('.label').textContent = dark ? 'Light' : 'Dark';
    button.querySelector('.icon').textContent = dark ? '☀' : '☾';
  });
}
syncThemeButtons();
themeButtons.forEach(button => button.addEventListener('click', () => {
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('playmaker-gc2-docs-theme', root.dataset.theme); } catch {}
  syncThemeButtons();
}));

const search = document.querySelector('[data-search]');
const links = [...document.querySelectorAll('.nav-link')];
const status = document.querySelector('#search-status');
search?.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase();
  let count = 0;
  links.forEach(link => {
    link.hidden = Boolean(query && !link.textContent.toLowerCase().includes(query));
    if (!link.hidden) count++;
  });
  document.querySelectorAll('.nav-group').forEach(group => {
    group.hidden = ![...group.querySelectorAll('.nav-link')].some(link => !link.hidden);
  });
  status.textContent = query ? (count ? count + ' matching page' + (count === 1 ? '' : 's') : 'No matching pages. Try a shorter title.') : '';
});

const menu = document.querySelector('[data-menu]');
const sidebar = document.querySelector('.sidebar');
const scrim = document.querySelector('[data-scrim]');
const closeButton = document.querySelector('[data-close-menu]');
const mobile = matchMedia('(max-width: 960px)');
function setMenu(open, restoreFocus = false) {
  const active = mobile.matches && open;
  sidebar.classList.toggle('open', active);
  scrim.classList.toggle('open', active);
  document.body.classList.toggle('nav-open', active);
  menu.setAttribute('aria-expanded', String(active));
  sidebar.inert = mobile.matches && !active;
  if (active) closeButton.focus();
  else if (restoreFocus && mobile.matches) menu.focus();
}
setMenu(false);
menu?.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true', true));
closeButton?.addEventListener('click', () => setMenu(false, true));
scrim?.addEventListener('click', () => setMenu(false, true));
links.forEach(link => link.addEventListener('click', () => setMenu(false)));
mobile.addEventListener('change', () => setMenu(false));

document.addEventListener('keydown', event => {
  const editing = event.target.closest('input, textarea, select, [contenteditable="true"]');
  if (event.key === '/' && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
    event.preventDefault();
    if (mobile.matches) setMenu(true);
    search.focus();
  }
  if (event.key === 'Escape') {
    if (mobile.matches && sidebar.classList.contains('open')) setMenu(false, true);
    else if (document.activeElement === search) {
      search.value = '';
      search.dispatchEvent(new Event('input'));
      search.blur();
    }
  }
  if (event.key === 'Tab' && mobile.matches && sidebar.classList.contains('open')) {
    const focusable = [...sidebar.querySelectorAll('a[href], button, input')].filter(el => !el.hidden && el.getClientRects().length);
    const first = focusable[0], last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
});

document.querySelectorAll('pre > code').forEach(code => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-code';
  button.textContent = 'Copy';
  button.setAttribute('aria-label', 'Copy code block');
  button.setAttribute('aria-live', 'polite');
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'Copied';
    } catch {
      // Select only the code text so copying remains possible if clipboard access is blocked.
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Selected';
    }
    setTimeout(() => { button.textContent = 'Copy'; }, 1600);
  });
  code.parentElement.appendChild(button);
});

const progress = document.querySelector('[data-reading-progress]');
const headings = [...document.querySelectorAll('main h2[id], main h3[id]')];
const tocLinks = [...document.querySelectorAll('.toc nav a')];
let scrollScheduled = false;
function updateReadingState() {
  scrollScheduled = false;
  const total = document.documentElement.scrollHeight - innerHeight;
  progress.style.width = (total > 0 ? Math.max(0, Math.min(100, scrollY / total * 100)) : 0) + '%';
  let active = headings[0]?.id;
  for (const heading of headings) {
    if (heading.getBoundingClientRect().top <= 130) active = heading.id;
  }
  tocLinks.forEach(link => {
    const current = link.hash === '#' + active;
    link.classList.toggle('active', current);
    if (current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
function scheduleReadingState() {
  if (!scrollScheduled) { scrollScheduled = true; requestAnimationFrame(updateReadingState); }
}
addEventListener('scroll', scheduleReadingState, { passive: true });
addEventListener('resize', scheduleReadingState);
addEventListener('load', scheduleReadingState);
updateReadingState();
