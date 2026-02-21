document.addEventListener('DOMContentLoaded', () => {
    // State
    let articles = [];
    let savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
    let currentView = 'latest'; // 'latest' or 'saved'

    // Supabase Configuration
    const SUPABASE_URL = 'https://lglvnwyzsvaguseznpcv.supabase.co';
    const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxnbHZud3l6c3ZhZ3VzZXpucGN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2ODU2MzcsImV4cCI6MjA4NzI2MTYzN30.0xtPuYihDLxqiDjJ1BZ3AGRLSPCxI2hcaBvX2WnPirM';

    // DOM Elements
    const feedContainer = document.getElementById('feed-container');
    const template = document.getElementById('article-card-template');
    const refreshBtn = document.getElementById('refresh-btn');
    const navItems = document.querySelectorAll('.nav-item');
    const pageTitle = document.querySelector('.page-title');
    const titleSubtitle = document.querySelector('.subtitle');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');

    // Initialize
    init();

    async function init() {
        try {
            await fetchArticles();
            renderArticles();
            setupEventListeners();
        } catch (e) {
            console.error("Initialization failed:", e);
            // Error state is already rendered by fetchArticles
        }
    }

    async function fetchArticles() {
        try {
            // Fetch from Supabase directly
            const response = await fetch(`${SUPABASE_URL}/rest/v1/articles?select=*&order=published_at.desc`, {
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            });

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            articles = await response.json();

            // Merge local storage saved state with the remote copy
            articles = articles.map(article => {
                const isSaved = savedArticles.some(saved => saved.id === article.id);
                return { ...article, is_saved: isSaved };
            });

        } catch (error) {
            console.error('Error fetching articles:', error);
            feedContainer.innerHTML = `
                <div class="loading-state" style="color: #ff3333; animation: none;">
                    Failed to load intelligence feed from Supabase.
                    <br><br>
                    <strong>Error Detail:</strong> ${error.message}
                    <br><br>
                    Make sure to run the sync pipeline first: <code>python navigation.py</code>
                </div>
            `;
            // Throw so init() knows it failed and doesn't render empty cards over the error
            throw error;
        }
    }

    function renderArticles() {
        feedContainer.innerHTML = '';

        if (!Array.isArray(articles) || !Array.isArray(savedArticles)) {
            savedArticles = savedArticles || [];
            articles = articles || [];
        }

        let displayList = currentView === 'latest' ? articles : savedArticles;

        // If current view is a category match, filter the master list
        if (currentView !== 'latest' && currentView !== 'saved') {
            displayList = articles.filter(a => a.category === currentView);
        }

        if (displayList.length === 0) {
            feedContainer.innerHTML = `
                <div class="loading-state" style="animation: none;">
                    ${currentView === 'latest' ? 'No recent signals found.' : (currentView === 'saved' ? 'You have no saved reports.' : `No signals found for ${currentView}.`)}
                </div>
            `;
            return;
        }

        displayList.forEach(article => {
            const clone = template.content.cloneNode(true);

            // Populate data
            const card = clone.querySelector('.article-card');

            const imageEl = clone.querySelector('.article-image');

            // Retro-fix Reddit Logos for older database/localStorage records
            if (article.source && article.source.includes('Reddit')) {
                article.image_url = 'https://www.iconpacks.net/icons/2/free-reddit-logo-icon-2436-thumb.png';
            }

            if (article.image_url) {
                imageEl.style.backgroundImage = `url('${article.image_url}')`;
            }

            clone.querySelector('.source-badge').textContent = article.source;

            // Format date
            const date = new Date(article.published_at);
            const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            clone.querySelector('.publish-time').textContent = timeStr;

            const titleLink = clone.querySelector('.article-title a');
            titleLink.textContent = article.title;

            // Clean up potentially broken relative URLs from older database records or localStorage
            let safeUrl = article.url;
            if (safeUrl && safeUrl.startsWith('/') && article.source === 'Hypebot') {
                safeUrl = 'https://www.hypebot.com' + safeUrl;
            }
            titleLink.href = safeUrl;

            clone.querySelector('.article-summary').textContent = article.summary;

            const saveBtn = clone.querySelector('.save-btn');

            // Determine if this item is currently saved based on local storage tracking
            const isSaved = savedArticles.some(saved => saved.id === article.id);

            if (isSaved) {
                saveBtn.classList.add('saved');
                saveBtn.textContent = 'Saved';
            }

            // Save Toggle Event
            saveBtn.addEventListener('click', () => toggleSave(article, saveBtn, card));

            feedContainer.appendChild(clone);
        });
    }

    function toggleSave(article, btnElement, cardElement) {
        const index = savedArticles.findIndex(saved => saved.id === article.id);

        if (index > -1) {
            // Unsave
            savedArticles.splice(index, 1);
            btnElement.classList.remove('saved');
            btnElement.textContent = 'Save for later';

            // If we are in the saved view, remove the card visually
            if (currentView === 'saved') {
                cardElement.style.display = 'none';
                if (savedArticles.length === 0) {
                    feedContainer.innerHTML = `<div class="loading-state" style="animation: none;">You have no saved reports.</div>`;
                }
            }
        } else {
            // Save
            article.is_saved = true;
            savedArticles.push(article);
            btnElement.classList.add('saved');
            btnElement.textContent = 'Saved';
        }

        // Persist to local storage
        localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
    }

    function setupEventListeners() {
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();

                // Update Nav UI
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');

                // Update View State (e.g., 'latest', 'saved', 'Analysis', 'News', 'Community')
                currentView = item.dataset.view;

                // Update Headers
                if (currentView === 'latest') {
                    pageTitle.textContent = 'Intelligence Feed';
                    titleSubtitle.textContent = 'Latest signals from the last 24 hours.';
                } else if (currentView === 'saved') {
                    pageTitle.textContent = 'Saved Reports';
                    titleSubtitle.textContent = 'Your archived intelligence.';
                } else {
                    pageTitle.textContent = currentView + ' Feed';
                    titleSubtitle.textContent = `Filtered intelligence for ${currentView}.`;
                }

                renderArticles();
            });
        });

        refreshBtn.addEventListener('click', async () => {
            refreshBtn.textContent = 'Refreshing...';
            refreshBtn.style.opacity = '0.7';
            await fetchArticles();
            renderArticles();
            setTimeout(() => {
                refreshBtn.textContent = 'Force Refresh';
                refreshBtn.style.opacity = '1';
            }, 500);
        });

        // Toggle Sidebar
        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.toggle('open');
                } else {
                    sidebar.classList.toggle('collapsed');
                }
            });

            // Close sidebar on mobile when a nav item is clicked
            navItems.forEach(item => {
                item.addEventListener('click', () => {
                    if (window.innerWidth <= 768) {
                        sidebar.classList.remove('open');
                    }
                });
            });
        }
    }
});
