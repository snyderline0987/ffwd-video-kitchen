const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const workspaceRoot = path.join(__dirname, '..');

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
    const projects = [];
    const dirs = fs.readdirSync(workspaceRoot, { withFileTypes: true })
                   .filter(dirent => dirent.isDirectory() && dirent.name.endsWith('-test'))
                   .map(dirent => dirent.name);
                   
    dirs.forEach(dir => {
        const hfPath = path.join(workspaceRoot, dir, 'my-video', 'hyperframes.json');
        if (fs.existsSync(hfPath)) {
            const hfData = readJsonSafe(hfPath);
            let comps = [];
            if(hfData && hfData.compositions) {
                comps = hfData.compositions.map(c => c.id);
            }
            
            let url = "";
            if(dir === 'hafen-wien-test') url = "https://hyperframes.dev/p/8b1b8da0-6156-4a77-86e7-33f599d9a4b3?claim_token=h0sD3qyiyMfdN-oRRIot91Ky3uyiTYjJ";
            if(dir === 'sign-performance-test') url = "https://hyperframes.dev/p/aeadd474-4763-4822-b67b-64e2e81a6567?claim_token=6xXLRAQKa4_J--uo-tijC-Wsg1EZA4oX";
            if(dir === 'urania-test') url = "https://hyperframes.dev/p/514c18c5-79ae-4a0b-b0a3-b501fe9969f1?claim_token=9yhAcTU3wph6_qJ0rKqq0WHu0KGfwQ-4";
            if(dir === 'ceenema-test') url = "https://hyperframes.dev/p/87835f07-41e2-4d3a-8f14-9c829b353e3b?claim_token=K2olYZB2xur5OstK0bHsKp2mz8cldRw5";
            if(dir === 'kulinarik-test') url = "https://hyperframes.dev/p/81adba10-81a0-4c58-9e69-12c108ac0452?claim_token=APeHWGwSvguqBRn1CavMA3wgpeZpxn3v";
            if(dir === 'w24-spezial-test') url = "https://hyperframes.dev/p/407784eb-8093-4efe-8bf3-a69575cd988f?claim_token=i5dnjImt9M1YeSdZFMN9z00qt-cbsIKR";

            projects.push({
                id: dir,
                compositions: comps,
                cloudUrl: url
            });
        }
    });
    res.json(projects);
});

app.listen(8080, () => console.log('Listening on port 8080'));