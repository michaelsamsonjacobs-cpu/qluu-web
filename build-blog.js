#!/usr/bin/env node
/**
 * build-blog.js — Static Blog Generator for QLUU
 * 
 * Pulls blog posts from Google Sheets CSV and generates individual
 * static HTML pages with proper SEO meta tags, schema markup, and
 * canonical URLs. This makes blog content visible to search engines
 * and AI crawlers (currently invisible due to client-side JS rendering).
 *
 * Usage:
 *   node build-blog.js
 *
 * Output:
 *   - /blog/[id].html for each post
 *   - Updates sitemap.xml with blog post URLs
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/1FoPFnDHca0zvP44gg3nBvVciuqzjP1NHoFpP6IWUwCo/export?format=csv';
const OUTPUT_DIR = path.join(__dirname, 'blog');
const SITEMAP_PATH = path.join(__dirname, 'sitemap.xml');
const CANONICAL_DOMAIN = 'https://qluulab.com';

// ── Fetch CSV ───────────────────────────────────────────────────────
function fetchCSV(url) {
    return new Promise((resolve, reject) => {
        const follow = (u) => {
            https.get(u, (res) => {
                if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                    follow(res.headers.location);
                    return;
                }
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(data));
                res.on('error', reject);
            }).on('error', reject);
        };
        follow(url);
    });
}

// ── Parse CSV (minimal — no dependency needed) ──────────────────────
function parseCSV(text) {
    const lines = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        if (ch === '"') {
            if (inQuotes && text[i + 1] === '"') {
                current += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (ch === ',' && !inQuotes) {
            lines.push(current);
            current = '';
        } else if ((ch === '\n' || ch === '\r') && !inQuotes) {
            if (ch === '\r' && text[i + 1] === '\n') i++;
            lines.push(current);
            current = '';
            // Mark end of row
            lines.push('\n');
        } else {
            current += ch;
        }
    }
    if (current) lines.push(current);

    // Split into rows
    const rows = [];
    let row = [];
    for (const cell of lines) {
        if (cell === '\n') {
            if (row.length > 0) rows.push(row);
            row = [];
        } else {
            row.push(cell);
        }
    }
    if (row.length > 0) rows.push(row);

    // Convert to objects using header row
    const headers = rows[0];
    const data = [];
    for (let i = 1; i < rows.length; i++) {
        const obj = {};
        headers.forEach((h, idx) => {
            obj[h.trim()] = (rows[i][idx] || '').trim();
        });
        if (obj.Title && obj.Title.length > 0) {
            data.push(obj);
        }
    }
    return data;
}

// ── Generate HTML for a single blog post ────────────────────────────
function generatePostHTML(post) {
    const title = escapeHTML(post.Title || 'Untitled');
    const summary = escapeHTML(post.Summary || '');
    const tag = escapeHTML(post.Tag || 'NEWS');
    const date = escapeHTML(post.Date || '');
    const imageURL = post['Image URL'] || '';
    const fullContent = post['Full Article Content (HTML)'] || `<p class="text-xl leading-relaxed text-gray-900 dark:text-brand-sepia dark:opacity-90">${summary}</p>`;
    const id = post.ID || '1';
    const slug = `blog/${id}.html`;
    const canonicalURL = `${CANONICAL_DOMAIN}/${slug}`;

    // ISO date for schema
    const isoDate = parseDate(date);

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} | QLUU Lab</title>
    <link rel="canonical" href="${canonicalURL}">
    <meta name="description" content="${summary}">
    <meta name="keywords" content="counter-UAS, C-UAS news, drone defense, ${tag.toLowerCase()}, QLUU">

    <meta property="og:site_name" content="QLUU Lab">
    <meta property="og:type" content="article">
    <meta property="og:url" content="${canonicalURL}">
    <meta property="og:title" content="${title}">
    <meta property="og:description" content="${summary}">
    <meta property="og:image" content="${escapeHTML(imageURL)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@qluulab">
    <meta name="twitter:image" content="${escapeHTML(imageURL)}">

    <link rel="icon" type="image/png" href="../assets/favicon_q.png">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "${title.replace(/"/g, '\\"')}",
        "description": "${summary.replace(/"/g, '\\"')}",
        "image": "${imageURL}",
        "datePublished": "${isoDate}",
        "author": {
            "@type": "Organization",
            "name": "QLUU Lab",
            "url": "https://qluulab.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": "QLUU Lab",
            "logo": {
                "@type": "ImageObject",
                "url": "https://qluulab.com/assets/logo_wht.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "${canonicalURL}"
        }
    }
    </script>

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            navy: '#030914',
                            cyan: '#00AEEF',
                            blue: '#3498DB',
                            sepia: '#F7F1D5',
                            lightBg: '#fafcfe'
                        }
                    },
                    fontFamily: {
                        sans: ['Space Grotesk', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: #fafcfe;
            color: #1a202c;
            transition: background-color 0.5s, color 0.5s;
        }
        html.dark body { background: #030914; color: #ffffff; }
        .glass-nav {
            background: rgba(250, 252, 254, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(0, 174, 239, 0.2);
        }
        html.dark .glass-nav {
            background: rgba(3, 9, 20, 0.6);
            border-bottom: 1px solid rgba(0, 174, 239, 0.1);
        }
        .text-glow { text-shadow: 0 0 20px rgba(0, 174, 239, 0.3); }
        html.dark .text-glow { text-shadow: 0 0 20px rgba(0, 174, 239, 0.5); }
        .article-body h2 { font-size: 1.5rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; }
        .article-body h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; }
        .article-body p { margin-bottom: 1rem; line-height: 1.8; }
        .article-body ul, .article-body ol { margin-bottom: 1rem; padding-left: 1.5rem; }
        .article-body li { margin-bottom: 0.5rem; line-height: 1.7; }
        .article-body a { color: #00AEEF; text-decoration: underline; }
        .article-body img { border-radius: 12px; margin: 1.5rem 0; max-width: 100%; }
    </style>
</head>

<body class="bg-brand-lightBg text-gray-900 transition-colors dark:bg-brand-navy dark:text-white">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 w-full z-50 glass-nav py-4 px-8 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <a href="../index.html">
                <img src="../assets/logo_wht.png" alt="QLUU Logo" class="h-8 transition-all invert dark:invert-0">
            </a>
        </div>
        <div class="hidden md:flex items-center gap-8 text-sm font-semibold tracking-widest uppercase text-gray-900 dark:text-brand-sepia dark:opacity-90">
            <a href="../index.html" class="hover:text-gray-900 dark:hover:text-white transition-colors">Critical Infra</a>
            <a href="../os.html" class="hover:text-gray-900 dark:hover:text-white transition-colors">Operating System</a>
            <a href="../government.html" class="hover:text-gray-900 dark:hover:text-white transition-colors">Government Solutions</a>
            <a href="../drones.html" class="hover:text-gray-900 dark:hover:text-white transition-colors">Drone Fleet</a>
            <a href="../blog.html" class="hover:text-gray-900 dark:hover:text-white transition-colors text-brand-cyan">Blog</a>
            <button id="theme-toggle" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors cursor-pointer text-xl">
                <span id="theme-icon">🌙</span>
            </button>
            <a href="../contact.html" class="px-5 py-2 border border-brand-cyan text-brand-cyan rounded hover:bg-brand-cyan hover:text-black transition-all">Contact Us</a>
        </div>
    </nav>

    <div class="relative z-10">
        <!-- Article -->
        <article class="max-w-4xl mx-auto px-8 pb-20 pt-32">
            <div class="mb-8">
                <a href="../blog.html" class="inline-flex items-center text-brand-cyan hover:text-brand-blue font-bold tracking-widest uppercase text-sm mb-6 transition-colors">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                    </svg>
                    Back to News
                </a>
                <div class="flex items-center gap-4 mb-6">
                    <span class="text-xs font-bold uppercase tracking-widest text-brand-cyan px-3 py-1 border border-brand-cyan rounded-full bg-brand-cyan bg-opacity-10">${tag}</span>
                    <span class="text-sm text-gray-800 dark:text-brand-sepia dark:opacity-90 font-medium tracking-widest uppercase">${date}</span>
                </div>
                <h1 class="text-4xl md:text-5xl font-bold leading-tight mb-8 text-gray-900 dark:text-white">${title}</h1>
                ${imageURL ? `<div class="w-full h-64 md:h-96 rounded-xl overflow-hidden mb-12 shadow-lg border border-brand-cyan border-opacity-20">
                    <img src="${escapeHTML(imageURL)}" alt="${title}" class="w-full h-full object-cover">
                </div>` : ''}
            </div>

            <div class="article-body text-lg text-gray-800 dark:text-brand-sepia dark:opacity-90">
                ${fullContent}
            </div>

            <!-- CTA -->
            <div class="mt-16 p-8 border border-brand-cyan border-opacity-20 rounded-xl text-center bg-brand-cyan bg-opacity-5">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Protect Your Airspace</h3>
                <p class="text-gray-800 dark:text-brand-sepia mb-6">Learn how QLUUos can defend your critical infrastructure from drone threats.</p>
                <a href="../contact.html" class="inline-block bg-brand-cyan text-black px-8 py-4 font-bold tracking-widest uppercase hover:bg-brand-navy hover:text-brand-cyan transition-all rounded shadow-[0_0_20px_rgba(0,174,239,0.4)]">Request a Brief</a>
            </div>
        </article>

        <!-- Footer -->
        <footer class="py-12 border-t border-brand-blue border-opacity-20 text-center bg-gray-100 dark:bg-brand-navy bg-opacity-80 dark:bg-opacity-80 transition-colors">
            <img src="../assets/logo_wht.png" alt="QLUU" class="h-6 mx-auto mb-6 invert dark:invert-0">
            <p class="opacity-80 text-sm tracking-widest font-medium text-gray-900 dark:text-white">&copy; 2026 QLUU Lab, Inc. California, USA. All rights reserved.</p>
        </footer>
    </div>

    <script>
        // Theme
        const isDark = localStorage.getItem('theme') === 'dark';
        if (isDark) document.documentElement.classList.add('dark');
        const ti = document.getElementById('theme-icon');
        if (ti) ti.textContent = isDark ? '☀️' : '🌙';
        const tb = document.getElementById('theme-toggle');
        if (tb) tb.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            const d = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', d ? 'dark' : 'light');
            ti.textContent = d ? '☀️' : '🌙';
        });
    </script>
</body>
</html>`;
}

// ── Helpers ──────────────────────────────────────────────────────────
function escapeHTML(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function parseDate(dateStr) {
    // Try to parse various date formats to ISO
    try {
        const d = new Date(dateStr);
        if (!isNaN(d.getTime())) return d.toISOString().split('T')[0];
    } catch (e) {}
    return new Date().toISOString().split('T')[0];
}

// ── Update Sitemap ──────────────────────────────────────────────────
function updateSitemap(posts) {
    const blogEntries = posts.map(p => {
        const id = p.ID || '1';
        const isoDate = parseDate(p.Date);
        return `  <url>
    <loc>${CANONICAL_DOMAIN}/blog/${id}.html</loc>
    <lastmod>${isoDate}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>`;
    }).join('\n');

    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${CANONICAL_DOMAIN}/</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${CANONICAL_DOMAIN}/os.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${CANONICAL_DOMAIN}/government.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${CANONICAL_DOMAIN}/drones.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${CANONICAL_DOMAIN}/blog.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>${CANONICAL_DOMAIN}/contact.html</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
${blogEntries}
</urlset>`;

    fs.writeFileSync(SITEMAP_PATH, sitemap, 'utf8');
    console.log(`✅ Updated sitemap.xml with ${posts.length} blog posts`);
}

// ── Main ────────────────────────────────────────────────────────────
async function main() {
    console.log('🔄 Fetching blog posts from Google Sheets...');

    const csv = await fetchCSV(GOOGLE_SHEET_CSV_URL);
    const posts = parseCSV(csv);

    console.log(`📝 Found ${posts.length} posts`);

    // Ensure output directory exists
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    // Generate each post
    for (const post of posts) {
        const id = post.ID || '1';
        const html = generatePostHTML(post);
        const filePath = path.join(OUTPUT_DIR, `${id}.html`);
        fs.writeFileSync(filePath, html, 'utf8');
        console.log(`  ✅ Generated blog/${id}.html — "${post.Title}"`);
    }

    // Update sitemap
    updateSitemap(posts);

    console.log(`\n🎉 Done! Generated ${posts.length} static blog pages in /blog/`);
    console.log('   Run this script before every deploy to keep blog SEO current.');
}

main().catch(err => {
    console.error('❌ Build failed:', err);
    process.exit(1);
});
