import glob
import os
import re

html_files = glob.glob('*.html')
primary_files = ['index.html', 'os.html', 'government.html', 'drones.html', 'blog.html', 'contact.html', 'article.html']
files_to_update = [f for f in html_files if f in primary_files or f.endswith('_recovered.html')]

# Open Graph Replacement
def update_og(content):
    # Absolute URL for OG Image
    replacement_tags = """
    <meta property="og:title" content="QLUU">
    <meta property="og:description" content="Sovereign AI Defense Platform">
    <meta property="og:image" content="https://qluu.website/assets/og_preview_simple.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://qluu.website/assets/og_preview_simple.png">
    <meta property="og:url" content="https://qluu.website/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="QLUU">
"""
    # Remove existing
    lines = content.split('\n')
    filtered_lines = []
    for line in lines:
        if 'property="og:' not in line and 'name="twitter:' not in line:
            filtered_lines.append(line)
    content = '\n'.join(filtered_lines)
    
    # Inject after title
    if '</title>' in content:
        content = content.replace('</title>', '</title>' + replacement_tags)
    return content

# Mobile Menu Injection
hamburger_btn = """
        <button id="mobile-menu-btn" class="md:hidden p-2 text-gray-900 dark:text-white focus:outline-none">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
        </button>
"""

mobile_menu_overlay = """
    <div id="mobile-menu" class="fixed inset-0 z-[100] bg-brand-lightBg dark:bg-brand-navy hidden flex-col transition-all duration-300">
        <div class="flex justify-between items-center p-8 border-b border-brand-cyan border-opacity-20">
            <img src="./assets/logo_wht.png" alt="QLUU Logo" class="h-8 dark:invert-0 invert transition-all">
            <button id="mobile-menu-close" class="p-2 text-gray-900 dark:text-white">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
        <div class="flex flex-col items-center justify-center flex-1 gap-8 text-2xl font-bold uppercase tracking-widest text-gray-900 dark:text-brand-sepia p-8 text-center">
            <a href="index.html" class="hover:text-brand-cyan transition-colors mobile-link">Critical Infra</a>
            <a href="os.html" class="hover:text-brand-cyan transition-colors mobile-link">Operating System</a>
            <a href="government.html" class="hover:text-brand-cyan transition-colors mobile-link">Government Solutions</a>
            <a href="drones.html" class="hover:text-brand-cyan transition-colors mobile-link">Drone Fleet</a>
            <a href="blog.html" class="hover:text-brand-cyan transition-colors mobile-link">Blog</a>
            <button id="mobile-menu-theme-toggle" class="p-4 rounded-full bg-gray-200 dark:bg-gray-800 text-3xl">
                <span id="mobile-theme-icon">??</span>
            </button>
            <a href="contact.html" class="w-full py-4 bg-brand-cyan text-white dark:text-black rounded-lg text-center mt-4">Contact Us</a>
        </div>
    </div>
"""

mobile_menu_js = """
    <script>
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenuClose = document.getElementById('mobile-menu-close');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileLinks = document.querySelectorAll('.mobile-link');
        const mobileThemeToggle = document.getElementById('mobile-menu-theme-toggle');
        const mobileThemeIcon = document.getElementById('mobile-theme-icon');

        if (mobileMenuBtn && mobileMenu && mobileMenuClose) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.remove('hidden');
                mobileMenu.classList.add('flex');
                document.body.style.overflow = 'hidden';
            });

            mobileMenuClose.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                mobileMenu.classList.remove('flex');
                document.body.style.overflow = '';
            });

            mobileLinks.forEach(link => {
                link.addEventListener('click', () => {
                    mobileMenu.classList.add('hidden');
                    mobileMenu.classList.remove('flex');
                    document.body.style.overflow = '';
                });
            });
        }

        // Sync theme icon in mobile menu
        function updateMobileThemeIcon() {
            if (mobileThemeIcon) {
                mobileThemeIcon.innerText = document.documentElement.classList.contains('dark') ? '??' : '??';
            }
        }

        if (mobileThemeToggle) {
            mobileThemeToggle.addEventListener('click', () => {
                document.documentElement.classList.toggle('dark');
                const isDark = document.documentElement.classList.contains('dark');
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
                updateMobileThemeIcon();
                // Sync main theme icon if it exists
                const themeIcon = document.getElementById('theme-icon');
                if (themeIcon) themeIcon.innerText = isDark ? '??' : '??';
            });
            updateMobileThemeIcon();
        }
    </script>
"""

count = 0
for f in files_to_update:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Update OG
    content = update_og(content)
    
    # 2. Add Mobile Menu Btn to nav
    if '</nav>' in content and 'id="mobile-menu-btn"' not in content:
        content = content.replace('</nav>', hamburger_btn + '</nav>')
    
    # 3. Add Mobile Menu Overlay
    if 'id="mobile-menu"' not in content:
        if '</body>' in content:
            content = content.replace('</body>', mobile_menu_overlay + '</body>')
    
    # 4. Add Mobile Menu JS
    if 'mobileMenuBtn' not in content:
        if '</body>' in content:
            content = content.replace('</body>', mobile_menu_js + '</body>')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    count += 1
    print(f'Updated {f}')

print(f'Done. Updated {count} files.')
