document.documentElement.classList.add('js');

const revealItems = document.querySelectorAll('[data-reveal]');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}

document.querySelectorAll('[data-filter]').forEach((input) => {
  const selector = input.getAttribute('data-filter');
  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    document.querySelectorAll(selector).forEach((item) => {
      const haystack = (item.getAttribute('data-search') || item.textContent || '').toLowerCase();
      item.classList.toggle('is-hidden', query.length > 0 && !haystack.includes(query));
    });
  });
});
