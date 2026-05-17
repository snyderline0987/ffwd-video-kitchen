# FFWD Video Kitchen 🎬📦

An agentic video studio — turn raw footage into edited video with film theory, motion templates, and recipe formats.

Built for **AI agents** that support skill directories. Tested with OpenClaw, Agent0, and Hermes.

## What It Does

- **6 recipe formats** — News, On-Air Promo, Social Clip, Gen AI Remake, Meme React, Product Landing
- **Motion templates** — Animated openers, lower thirds, CI elements (GSAP-powered)
- **Film theory engine** — Every cut follows editing rules (Dmytryk, Menke, Eisenstein, Murch)
- **100% local** — No footage uploads. Your data stays on your machine.
- **Self-contained dashboard** — Browse recipes, preview templates, no cloud required

## Quick Start

```bash
git clone https://github.com/snyderline0987/ffwd-video-kitchen.git
```

### OpenClaw

```bash
# Copy skills into OpenClaw's skill directory
cp -r ffwd-video-kitchen/skills/* /usr/local/lib/node_modules/openclaw/skills/

# Or mount in Docker
docker run -v ./ffwd-video-kitchen/skills:/usr/local/lib/node_modules/openclaw/skills openclaw/openclaw
```

### Agent0

```bash
# Point Agent0 at the skills directory
export AGENT0_SKILLS_DIR=./ffwd-video-kitchen/skills
```

### Hermes

```yaml
# hermes.yaml
skills:
  - ./ffwd-video-kitchen/skills
```

## How to Cook a Video 🍳

Video Kitchen is an agent-driven pipeline. You bring the ingredients — a source video and a recipe — and your AI agent handles the rest.

### 1. Drop a Video

Send your source footage to the agent — any format, any length. Drag a file into chat, paste a URL, or point to an existing file on disk.

```
# via Telegram / Discord / CLI
"make a 30s teaser from this video" + 📎 source.mp4
```

### 2. Pick a Recipe

Choose a recipe blueprint that matches your format. Each recipe defines the structure, pacing, aspect ratio, and editing theory for the final video.

| Recipe | Ratio | Duration | Theory | Style |
|--------|-------|----------|--------|-------|
| 📰 News Overview 30s | 16:9 | 30s | Dmytryk | Hook → Context → Facts → CTA |
| 📱 Social Clip | 9:16 | 15-25s | Eisenstein | Hook → Punchline → CTA |
| 🎬 On Air Promo | 16:9 | 40s | Menke | Cinematic, rhythmic |
| 🧠 Gen AI Remake | 16:9 | 30s | Eisenstein | Before → AI → Reveal |
| 😂 Meme Culture React | 9:16 | 15s | Eisenstein | Zoom, bold text, punchline |
| 🛍️ Product Landing | 16:9 | 20s | Dmytryk | Clean, modern, sales |

### 3. Agent Analyzes

The agent automatically extracts thumbnails, rates each shot for teaser value, transcribes audio, and identifies the best moments — hero shots, emotional beats, key facts.

```
Extracting thumbnails   ✓ 27 frames @ 5s interval
Vision rating           ✓ 8 hero · 8 strong · 11 skip
Transcription           ✓ 1,381 chars German
Shot selection          ✓ 6 clips picked
```

### 4. Composition Built

The agent writes a HyperFrames HTML composition — video clips, text overlays, GSAP animations, all timed to the frame. Film theory (Murch, Eisenstein, Dmytryk) drives the cut decisions.

```html
<div data-composition-id="main">
  <video src="clip-hook.mp4"
         data-start="0" data-duration="4" />
  <div class="headline">Breaking Story</div>
  <script> gsap.timeline()... </script>
</div>
```

### 5. Render & Serve

HyperFrames renders the composition frame-by-frame via headless Chromium, encodes to MP4, and the agent delivers the finished video back to you.

```
$ hyperframes render --output teaser.mp4 --fps 24
720 frames · 1080x1920 · 30.0s
✓ Render complete — 10.7 MB
```

### 6. Iterate

Not perfect? Tell the agent what to change. Adjust timing, swap clips, rewrite text, change colors, tweak animations. The composition is code — every detail is editable by conversation.

```
You:   "swap the 3rd clip for something more energetic"
Agent: Replaced clip with ⭐5 crowd shot. Re-rendering...
```

> The entire pipeline runs locally. No cloud APIs, no uploads. Your footage stays on your machine.

---

## Dashboard

The recipe dashboard is a standalone Node server with a live preview of all motion templates:

```bash
cd skills/video-kitchen/recipes
npm install
node server.js
# → http://localhost:8080/dashboard.html
```

**Dashboard Features:**
- **Recent Projects** — View your latest renders
- **Recipe Blueprints** — Browse all 6 recipe formats with descriptions
- **Motion Templates** — Live preview of all lower thirds and inserts
- **How to Cook** — Step-by-step workflow guide
- **Config Panel** — Press `E` on any template to edit name, role, colors, duration

## Skills Included

| Skill | What it does |
|-------|-------------|
| `video-kitchen` | Core pipeline — source analysis, recipe matching, composition building |
| `video-kitchen-recipe-creator` | Create new recipe formats |
| `hyperframes` | HTML-based video compositions, animations, rendering |
| `film-editing-theory` | Cut decisions based on Murch, Dmytryk, Eisenstein, Menke |
| `css-animations`, `gsap`, `animejs`, `lottie` | Animation adapters for HyperFrames |

## Contributing

### Contributing a New Recipe

Recipes are the blueprints that tell the agent how to structure a video. A recipe consists of:

1. **`config.json`** — Metadata, editing theory, prompts, preferences
2. **`composition.html`** — A HyperFrames template composition (optional, for complex layouts)

**Recipe Structure:**

```
skills/video-kitchen/recipes/{recipe-id}/
├── config.json           # Recipe metadata
└── composition.html      # Template composition (optional)
```

**Step 1: Create the folder**

```bash
cd skills/video-kitchen/recipes
mkdir my_new_recipe
cd my_new_recipe
```

**Step 2: Write `config.json`**

```json
{
  "id": "my_new_recipe",
  "title": "My New Recipe",
  "aspect_ratio": "16:9",
  "duration": "30s",
  "description": "Brief description of what this recipe does.",
  "theory": "Dmytryk (Substance First) | Eisenstein (Montage) | Murch (Emotion First) | Menke (Dialogue Rhythm)",
  "prompt": "Instructions for the AI agent on how to analyze source and build this composition.",
  "vo_pref": "Voice preference (e.g., 'Nova (warm, friendly)')",
  "music_pref": "Music preference (e.g., 'upbeat, 20% volume')",
  "cut_style": "Cutting style description (e.g., 'Quick cuts, 2-3s per shot')"
}
```

**Step 3: Add a template composition (optional)**

If your recipe needs a specific layout (not just cuts from source), create `composition.html` as a HyperFrames composition. See [KNOWLEDGE.md](skills/video-kitchen/KNOWLEDGE.md) for patterns.

**Step 4: Rebuild the manifest**

```bash
cd skills/video-kitchen/recipes
python3 build-manifest.py
```

This regenerates `manifest.json` with your new recipe. The dashboard will pick it up automatically.

**Step 5: Test it**

Start the server and verify your recipe appears in the dashboard:

```bash
node server.js
# Open http://localhost:8080/dashboard.html
```

### Contributing a New Motion Template

Motion templates are reusable animated elements (lower thirds, title cards, CTAs, inserts) that can be parameterized via URL query.

**Template Structure:**

```
skills/video-kitchen/motion-templates/{template-id}/
├── config.json           # Template metadata
├── template.html         # The HyperFrames composition
└── media/                # Template-specific assets (fonts, videos, images)
```

**Step 1: Create the folder**

```bash
cd skills/video-kitchen/motion-templates
mkdir my_template
cd my_template
mkdir media
```

**Step 2: Write `config.json`**

```json
{
  "id": "my_template",
  "title": "My Template",
  "description": "Brief description of what this template does.",
  "aspect_ratio": "16:9",
  "resolution": "1920x1080",
  "duration": "5s",
  "params": ["name", "role", "color"],  // URL parameters this template accepts
  "tags": ["lower-third", "cta", "title-card"]
}
```

**Step 3: Create `template.html`**

Write a HyperFrames composition that reads URL parameters and renders dynamically:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Template</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body class="bg-black overflow-hidden">

  <div id="composition" class="w-full h-screen flex items-center">
    <div id="bar" class="h-20" style="width: 0px;"></div>
    <div id="text" class="text-white font-bold text-4xl px-8 opacity-0;">
      <span id="name"></span><br>
      <span id="role" class="text-2xl"></span>
    </div>
  </div>

  <script>
    // Read URL parameters
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name') || 'Default Name';
    const role = params.get('role') || 'Default Role';
    const color = params.get('color') || '#e50914';

    document.getElementById('name').textContent = name;
    document.getElementById('role').textContent = role;
    document.getElementById('bar').style.backgroundColor = color;

    // Register animations
    window.__timelines = {
      main: gsap.timeline()
        .to('#bar', { width: 300, duration: 0.8, ease: 'power2.out' })
        .to('#text', { opacity: 1, duration: 0.5 }, '-=0.3')
        .to('#composition', { opacity: 0, duration: 0.5 }, '+=2')
    };

    // hf-seek listener for rendering
    window.addEventListener('hf-seek', (e) => {
      window.__timelines.main.seek(e.detail);
    });
  </script>
</body>
</html>
```

**Key requirements for templates:**

- `window.__timelines` object with a `main` GSAP timeline
- `hf-seek` event listener for deterministic rendering
- All assets must be self-contained in the `media/` folder (fonts, images, videos)
- Use `clamp()` for responsive font sizing across aspect ratios

**Step 4: Test it**

Start the server and verify your template appears:

```bash
cd skills/video-kitchen/recipes
node server.js
# Open http://localhost:8080/dashboard.html
# Click your template tab to see live preview
```

**Step 5: Try customizing via URL**

```
http://localhost:8080/motion-templates/my_template/template.html?name=Daniel&role=Director&color=blue
```

## Project Structure

```
ffwd-video-kitchen/
├── skills/
│   ├── video-kitchen/
│   │   ├── SKILL.md              # Core skill instructions for agents
│   │   ├── KNOWLEDGE.md          # Agent knowledge base (patterns, conventions)
│   │   ├── recipes/              # Recipe blueprints
│   │   │   ├── {recipe-id}/
│   │   │   │   ├── config.json   # Recipe metadata
│   │   │   │   └── composition.html  # Template composition
│   │   │   ├── public/           # Dashboard + static assets
│   │   │   │   ├── index.html    # Main dashboard
│   │   │   │   └── fonts/        # Shared fonts (Wiener Melange)
│   │   │   ├── manifest.json     # Auto-generated recipe list
│   │   │   ├── build-manifest.py # Manifest generator
│   │   │   └── server.js         # Express API server
│   │   └── motion-templates/     # Reusable motion elements
│   │       └── {template-id}/
│   │           ├── config.json   # Template metadata
│   │           ├── template.html # The template composition
│   │           └── media/        # Template-specific assets
│   ├── video-kitchen-recipe-creator/
│   ├── hyperframes/
│   ├── film-editing-theory/
│   └── [other animation skills...]
└── README.md                     # This file
```

## Future Plans

### Short Term (Q2 2026)

- [ ] **Extended recipe library** — Add 8-12 new formats (explainer, event recap, interview teaser, playlist intro)
- [ ] **Motion template library** — Expand to 20+ templates (various CI styles, industry-specific inserts)
- [ ] **Audio reactivity** — Beat-sync animations, audio-reactive overlays (AudioMotion-analyzer integration)
- [ ] **Batch processing** — Process multiple videos in parallel, queue-based rendering

### Medium Term (Q3 2026)

- [ ] **Recipe marketplace** — Community-contributed recipes with ratings, previews, and one-click install
- [ ] **Auto-styles** — AI-generated motion templates based on brand colors, fonts, and reference videos
- [ ] **Multi-shot AI analysis** — Transcribe, summarize, and rank entire footage libraries automatically
- [ ] **Export options** — Preset export profiles (Instagram Reels, TikTok, YouTube Shorts, Twitter)

### Long Term (Q4 2026+)

- [ ] **Docker-first deployment** — Complete containerized stack with all dependencies pre-baked
- [ ] **Voiceover pipeline** — Integrated TTS (Kokoro/ElevenLabs) with voice-switching and timing sync
- [ ] **Subtitle engine** — Auto-generate captions with word-level timing and style matching
- [ ] **Live preview** — Real-time composition preview with seekable timeline and hot-reload
- [ ] **Collaborative editing** — Session-based composition sharing with real-time co-editing

## Requirements

- An agent that supports skill directories (OpenClaw, Agent0, Hermes, etc.)
- At least one AI provider API key (Gemini, OpenAI, or OpenRouter) for vision and transcription
- Raw video footage
- Node.js 16+ (for the dashboard)

## Brand

- **FFWD** — Red accent `#e50914`, dark bg `#0a0a0a`
- **Wiener Melange** — Custom font for CI elements (W_Rg, W_Bd, W_ExBd)

## License

MIT

## Credits

- Built with [OpenClaw](https://github.com/openclaw/openclaw) and [HyperFrames](https://github.com/openclaw/hyperframes)
- Film theory from Walter Murch, Edward Dmytryk, Sergei Eisenstein, and Sally Menke
- GSAP for animations, Tailwind CSS for styling