# Video Kitchen in a Box 🎬📦

A skill bundle for AI agents — turn raw footage into edited video with film theory, motion templates, and 6 recipe formats.

Works with **any agent** that supports skill directories. Tested with OpenClaw, Agent0, and Hermes.

## What It Does

- **6 recipe formats** — News, On-Air Promo, Social Clip, Gen AI Remake, Meme React, Product Landing
- **Motion templates** — Animated openers, lower thirds, CI elements (GSAP-powered)
- **Film theory engine** — Every cut follows editing rules (Dmytryk, Menke, Eisenstein, Murch)
- **100% local** — No footage uploads. Your data stays on your machine.

## Install

```bash
git clone https://github.com/snyderline0987/video-kitchen-box.git
```

### OpenClaw

```bash
# Copy skills into OpenClaw's skill directory
cp -r video-kitchen-box/skills/* /usr/local/lib/node_modules/openclaw/skills/

# Or mount in Docker
docker run -v ./video-kitchen-box/skills:/usr/local/lib/node_modules/openclaw/skills openclaw/openclaw
```

### Agent0

```bash
# Point Agent0 at the skills directory
export AGENT0_SKILLS_DIR=./video-kitchen-box/skills
```

### Hermes

```yaml
# hermes.yaml
skills:
  - ./video-kitchen-box/skills
```

## Skills Included

| Skill | What it does |
|-------|-------------|
| `video-kitchen` | Core pipeline — source analysis, recipe matching, composition building |
| `video-kitchen-recipe-creator` | Create new recipe formats |
| `hyperframes` | HTML-based video compositions, animations, rendering |
| `film-editing-theory` | Cut decisions based on Murch, Dmytryk, Eisenstein, Menke |
| `open-design` | CI elements, motion templates, brand assets |

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

The recipe dashboard is a standalone Node server:

```bash
cd skills/video-kitchen/recipes
npm install
node server.js
# → http://localhost:8080/dashboard.html
```

## Requirements

- An agent that supports skill directories (OpenClaw, Agent0, Hermes, etc.)
- At least one AI provider API key (Gemini, OpenAI, or OpenRouter)
- Raw video footage

## License

MIT
