const fs = require('fs');

try {
    // Copy the favicon
    const sourceImage = 'C:\\Users\\Mike\\.gemini\\antigravity\\brain\\38945b9c-3397-48a1-a6fd-7fdd8c71ee70\\media__1772607306611.jpg';
    const destination1 = 'assets/favicon_q.png';
    const destination2 = 'assets/favicon_q.jpg';

    if (fs.existsSync(sourceImage)) {
        fs.copyFileSync(sourceImage, destination1);
        fs.copyFileSync(sourceImage, destination2);
        console.log('Favicon successfully copied to assets folder.');
    } else {
        console.error('Source favicon image not found!');
    }

    // Read index and blog HTML
    const indexHtml = fs.readFileSync('index.html', 'utf8');
    let blogHtml = fs.readFileSync('blog.html', 'utf8');

    if (!blogHtml.includes('id="canvas"')) {
        // Extract three.js imports and code block from indexHtml
        const importStart = indexHtml.indexOf('<script type="importmap">');
        const moduleStart = indexHtml.indexOf('<script type="module">');
        const moduleEnd = indexHtml.indexOf('</script>', moduleStart) + 9;
        const scriptBlock = indexHtml.substring(importStart, moduleEnd);

        // Extract style block from indexHtml
        const styleStart = indexHtml.indexOf('<style>');
        const styleEnd = indexHtml.indexOf('</style>') + 8;
        const styleBlock = indexHtml.substring(styleStart, styleEnd);

        // Inject styles
        blogHtml = blogHtml.replace(/<style>[\s\S]*?<\/style>/, styleBlock);

        // Inject canvas into body (first match of body)
        blogHtml = blogHtml.replace(/<body.*?>/, (match) => {
            return match + '\n    <!-- Background Animation Canvas -->\n    <canvas id="canvas"></canvas>';
        });

        // Inject script block at EOF
        blogHtml = blogHtml.replace('</body>', scriptBlock + '\n</body>');

        fs.writeFileSync('blog.html', blogHtml, 'utf8');
        console.log('Successfully injected three.js animation block into blog.html');
    } else {
        console.log('blog.html already contains the three.js animation block.');
    }

} catch (e) {
    console.error('Error during blog update:', e);
}
