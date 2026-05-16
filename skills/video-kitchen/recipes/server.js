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

        // Check for hyperframes.json at project root or studio subfolder
        let hfPath = path.join(workspaceRoot, dir, 'hyperframes.json');
        let projectLabel = dir;
        let compDir = path.join(workspaceRoot, dir);
        if (!fs.existsSync(hfPath)) {
            hfPath = path.join(workspaceRoot, dir, 'studio', 'my-video', 'hyperframes.json');
            compDir = path.join(workspaceRoot, dir, 'studio', 'my-video');
        }
        if (!fs.existsSync(hfPath)) {
            // Also check my-video direct subfolder
            hfPath = path.join(workspaceRoot, dir, 'my-video', 'hyperframes.json');
            compDir = path.join(workspaceRoot, dir, 'my-video');
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
        const rendersDir = path.join(compDir, 'renders');
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

        // Build studio URL pointing to project composition
        const tunnelBase = process.env.HF_TUNNEL_URL || null;
        let studioUrl = null;
        if (tunnelBase) {
            // HF studio serves at / with project path
            const relPath = path.relative(workspaceRoot, compDir);
            studioUrl = tunnelBase.replace(/\/$/, '') + '/studio/' + relPath + '/';
        }

        projects.push({
            id: dir,
            label: projectLabel,
            compositions: comps,
            renderCount,
            lastRender,
            meta: meta || {},
            cloudUrl: studioUrl,
            localPath: compDir
        });
    });

    // Sort by last render time (newest first)
    projects.sort((a, b) => (b.lastRender || '').localeCompare(a.lastRender || ''));
    console.log('Projects found:', projects.length, projects.map(p => p.id));
    res.json(projects);
    } catch(e) { console.error('Projects error:', e); res.json([]); }
});

app.get('/api/reference-renders', (req, res) => {
    const references = [];
    const refDir = path.join(__dirname, 'reference-renders');
    if (!fs.existsSync(refDir)) {
        res.json(references);
        return;
    }
    fs.readdirSync(refDir, { withFileTypes: true })
        .filter(d => d.isDirectory())
        .forEach(dirent => {
            const dir = dirent.name;
            const metaPath = path.join(refDir, dir, 'meta.json');
            const meta = readJsonSafe(metaPath) || {};
            // Find video files
            const files = fs.readdirSync(path.join(refDir, dir))
                .filter(f => f.endsWith('.mp4') || f.endsWith('.webm'));
            if (files.length > 0 || meta.title) {
                references.push({
                    id: dir,
                    title: meta.title || dir,
                    description: meta.description || '',
                    recipe: meta.recipe || '',
                    theory: meta.theory || '',
                    bpm: meta.bpm || '',
                    duration: meta.duration || '',
                    files: files,
                    hasComp: fs.existsSync(path.join(refDir, dir, 'composition.html')),
                    ...meta
                });
            }
        });
    res.json(references);
});

app.use('/reference-renders', express.static(path.join(__dirname, 'reference-renders')));

// Motion Templates API
const motionTemplatesDir = path.join(__dirname, '..', 'motion-templates');
app.get('/api/motion-templates', (req, res) => {
    try {
        const templates = [];
        if (!fs.existsSync(motionTemplatesDir)) return res.json(templates);
        const dirs = fs.readdirSync(motionTemplatesDir, { withFileTypes: true })
                       .filter(d => d.isDirectory());
        dirs.forEach(d => {
            const configPath = path.join(motionTemplatesDir, d.name, 'config.json');
            const config = readJsonSafe(configPath);
            if (!config) return;
            const hasTemplate = fs.existsSync(path.join(motionTemplatesDir, d.name, 'template.html'));
            templates.push({
                ...config,
                id: config.id || d.name,
                hasTemplate
            });
        });
        res.json(templates);
    } catch(e) {
        res.status(500).json({ error: e.message });
    }
});

// Serve motion template files
app.use('/motion-templates', express.static(motionTemplatesDir));

app.post('/api/start-studio', (req, res) => {
    const { projectId } = req.body;
    if (!projectId) return res.status(400).json({ error: 'projectId required' });

    // Find project dir
    let compDir = null;
    const checks = [
        path.join(workspaceRoot, projectId),
        path.join(workspaceRoot, projectId, 'studio', 'my-video'),
        path.join(workspaceRoot, projectId, 'my-video')
    ];
    for (const d of checks) {
        if (fs.existsSync(path.join(d, 'hyperframes.json'))) { compDir = d; break; }
    }
    if (!compDir) return res.status(404).json({ error: 'Project not found' });

    // Check if studio already running
    const { execSync } = require('child_process');
    try {
        const running = execSync('lsof -i :3002 -t 2>/dev/null || true').toString().trim();
        if (running) {
            // Already running — return URL
            const tunnelBase = process.env.HF_TUNNEL_URL || 'http://localhost:3002';
            const relPath = path.relative(workspaceRoot, compDir);
            return res.json({ url: tunnelBase.replace(/\/$/, '') + '/studio/' + relPath + '/', running: true });
        }
    } catch(e) {}

    // Start studio in background
    const { spawn } = require('child_process');
    const studio = spawn('npx', ['hyperframes', 'preview', '--port', '3002'], {
        cwd: compDir,
        detached: true,
        stdio: 'ignore'
    });
    studio.unref();

    const tunnelBase = process.env.HF_TUNNEL_URL || 'http://localhost:3002';
    const relPath = path.relative(workspaceRoot, compDir);
    res.json({ url: tunnelBase.replace(/\/$/, '') + '/studio/' + relPath + '/', running: false });
});

app.listen(8080, () => console.log('Listening on port 8080'));