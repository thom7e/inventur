(function () {
    function debounce(fn, wait) {
        let t;
        return function (...args) {
            clearTimeout(t);
            t = setTimeout(() => fn.apply(this, args), wait);
        };
    }

    const form = document.getElementById('adminSearchForm') || document.getElementById('searchForm');
    const input = form ? form.querySelector('input[name="search_query"], input[id="search_query"]') : null;
    const resultsContainer = document.getElementById('admin-search-results') || document.getElementById('search-results');

    if (!form || !input || !resultsContainer) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        performSearch(input.value);
    });

    const performSearch = debounce(function (query) {
        query = String(query || '').trim();
        if (query.length < 2) {
            resultsContainer.innerHTML = '<p class="text-muted mb-0">Bitte mindestens zwei Zeichen eingeben.</p>';
            return;
        }

        const action = (form.getAttribute('action') || '/admin/search' || '/search').trim();
        const url = action || '/admin/search';
        const body = new URLSearchParams({ search_query: query });

        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: body.toString(),
        })
            .then((res) => res.json())
            .then((data) => {
                const results = Array.isArray(data.results) ? data.results : [];
                if (!results.length) {
                    resultsContainer.innerHTML = '<p class="text-muted mb-0">Keine Treffer.</p>';
                    return;
                }
                resultsContainer.innerHTML = results
                    .map((r) => {
                        const preis = r.preis !== undefined ? r.preis : '';
                        const einheit = r.einheit ? ` <small class="text-muted">${escapeHtml(r.einheit)}</small>` : '';
                        return `<div class="search-result-item p-2 mb-2 border rounded">
                                    <div class="d-flex justify-content-between">
                                        <div><strong>${escapeHtml(r.artikelname)}</strong>${einheit}</div>
                                        <div class="text-right">${escapeHtml(String(preis))}</div>
                                    </div>
                                </div>`;
                    })
                    .join('');
            })
            .catch((err) => {
                console.error('Admin search error', err);
                resultsContainer.innerHTML = '<p class="text-danger mb-0">Fehler bei der Suche.</p>';
            });
    }, 200);

    input.addEventListener('input', (e) => performSearch(e.target.value));

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
})();