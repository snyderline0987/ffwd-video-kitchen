const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const workspaceRoot = process.env.VK_WORKSPACE || path.join(__dirname, '..', '..', '..', '..');

function readJsonSafe(filePath) {
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch(e) {
        return null;
    }
}

app.get('/api/recipes', (req, res) => {
    const recipes = [];
    const dirs = fs.readdirSync(__dirname, { withFileTypes: true })
                   .filter(dirent => dirent.isDirectory() && !['node_modules', 'public', 'lib'].includes(dirent.name))
                   .map(dirent => dirent.name);
                   
    dirs.forEach(dir => {
        const configPath = path.join(__dirname, dir, 'config.json');
        if (fs.existsSync(configPath)) {
            const configData = readJsonSafe(configPath);
            if(configData) {
                configData.has_composition = fs.existsSync(path.join(__dirname, dir, 'composition.html'));
                recipes.push(configData);
            }
        }
    });
    res.json(recipes);
});

app.post('/api/recipes/:id', (req, res) => {
    const recipeId = req.params.id;
    const dirPath = path.join(__dirname, recipeId);
    const configPath = path.join(dirPath, 'config.json');
    
    // Create directory if it doesn't exist
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
    
    // Save config
    fs.writeFileSync(configPath, JSON.stringify(req.body, null, 2));
    
    res.json({ success: true, message: 'Recipe saved' });
});

app.get('/api/projects', (req, res) => {
    try {
    const projects = [];

    // Scan workspace root for dirs with hyperframes.json (any name)
    const allDirs = fs.readdirSync(workspaceRoot, { withFileTypes: true })
                      .filter(dirent => dirent.isDirectory())
                      .map(dirent => dirent.name);

    const skipDirs = ['node_modules', '.git', 'lib', 'public', 'skills', 'media', 'analysis', 'clips', 'renders'];

    allDirs.forEach(dir => {
        if (skipDirs.some(s => dir === s || dir.startsWith('.'))) return;

        // Check for hyperframes.json at project root or my-video subfolder
        let hfPath = path.join(workspaceRoot, dir, 'hyperframes.json');
        let projectLabel = dir;
        if (!fs.existsSync(hfPath)) {
            hfPath = path.join(workspaceRoot, dir, 'my-video', 'hyperframes.json');
        }
        if (!fs.existsSync(hfPath)) return;

        const hfData = readJsonSafe(hfPath);
        let comps = [];
        if(hfData && hfData.compositions) {
            comps = hfData.compositions.map(c => c.id);
        }

        // Read meta.json for nicer display
        const metaPath = path.join(workspaceRoot, dir, 'meta.json');
        const meta = readJsonSafe(metaPath);
        if (meta && meta.title) projectLabel = meta.title;

        // Check for rendered videos
        const rendersDir = path.join(workspaceRoot, dir, 'renders');
        let renderCount = 0;
        let lastRender = null;
        try {
            const renders = fs.readdirSync(rendersDir).filter(f => f.endsWith('.mp4'));
            renderCount = renders.length;
            if (renders.length > 0) {
                const stat = fs.statSync(path.join(rendersDir, renders[renders.length - 1]));
                lastRender = stat.mtime.toISOString();
            }
        } catch(e) {}

        projects.push({
            id: dir,
            label: projectLabel,
            compositions: comps,
            renderCount,
            lastRender,
            meta: meta || {}
        });
    });

    // Sort by last render time (newest first)
    projects.sort((a, b) => (b.lastRender || '').localeCompare(a.lastRender || ''));
    console.log('Projects found:', projects.length, projects.map(p => p.id));
    res.json(projects);
    } catch(e) { console.error('Projects error:', e); res.json([]); }
});

app.listen(8080, () => console.log('Listening on port 8080'));