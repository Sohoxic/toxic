class SearchEngine {
    constructor() {
        this.searchIndex = [];
        this.isLoaded = false;
        this.loadSearchIndex();
    }

    async loadSearchIndex() {
        try {
            const response = await fetch('/search-index.json');
            this.searchIndex = await response.json();
            this.isLoaded = true;
            console.log(`Search index loaded with ${this.searchIndex.length} entries`);
        } catch (error) {
            console.error('Failed to load search index:', error);
        }
    }

    search(query, maxResults = 10) {
        if (!this.isLoaded || !query.trim()) {
            return [];
        }

        const searchTerms = query.toLowerCase().split(/\s+/);
        const results = [];

        for (const item of this.searchIndex) {
            const score = this.calculateScore(item, searchTerms);
            if (score > 0) {
                results.push({
                    ...item,
                    score: score,
                    highlightedTitle: this.highlightText(item.title, searchTerms),
                    highlightedExcerpt: this.highlightText(item.excerpt, searchTerms)
                });
            }
        }

        // Sort by score (descending) and return top results
        return results
            .sort((a, b) => b.score - a.score)
            .slice(0, maxResults);
    }

    calculateScore(item, searchTerms) {
        let score = 0;
        const title = item.title.toLowerCase();
        const content = item.content.toLowerCase();
        const tags = item.tags.map(tag => tag.toLowerCase());

        for (const term of searchTerms) {
            // Title matches get highest score
            if (title.includes(term)) {
                score += title === term ? 100 : 50;
            }

            // Tag matches get high score
            for (const tag of tags) {
                if (tag.includes(term)) {
                    score += tag === term ? 80 : 40;
                }
            }

            // Content matches get lower score
            if (content.includes(term)) {
                score += 10;
            }
        }

        return score;
    }

    highlightText(text, searchTerms) {
        if (!text) return '';
        
        let highlightedText = text;
        
        for (const term of searchTerms) {
            const regex = new RegExp(`(${this.escapeRegExp(term)})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
        }
        
        return highlightedText;
    }

    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
}

// Initialize search functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const searchEngine = new SearchEngine();
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchContainer = document.getElementById('search-container');

    if (!searchInput || !searchResults) {
        console.log('Search elements not found on this page');
        return;
    }

    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchContainer.classList.remove('has-results');
            return;
        }

        // Debounce search to avoid too many searches while typing
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });

    function performSearch(query) {
        const results = searchEngine.search(query);
        displayResults(results, query);
    }

    function displayResults(results, query) {
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="search-no-results">
                    <p>No results found for "${query}"</p>
                </div>
            `;
        } else {
            const resultsHTML = results.map(result => `
                <div class="search-result">
                    <h3 class="search-result-title">
                        <a href="${result.url}">${result.highlightedTitle}</a>
                    </h3>
                    <p class="search-result-excerpt">${result.highlightedExcerpt}</p>
                    <div class="search-result-meta">
                        ${result.tags.length > 0 ? `<span class="search-result-tags">${result.tags.join(', ')}</span>` : ''}
                        ${result.date ? `<span class="search-result-date">${result.date}</span>` : ''}
                    </div>
                </div>
            `).join('');

            searchResults.innerHTML = `
                <div class="search-results-header">
                    <p>Found ${results.length} result${results.length !== 1 ? 's' : ''} for "${query}"</p>
                </div>
                ${resultsHTML}
            `;
        }

        searchContainer.classList.add('has-results');
    }

    // Close search results when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchContainer.contains(event.target)) {
            searchContainer.classList.remove('has-results');
        }
    });

    // Handle keyboard navigation
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            searchContainer.classList.remove('has-results');
            this.blur();
        }
    });
}); 