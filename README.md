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

## Recipes

Each recipe is a folder with `config.json` + `composition.html`:

| Recipe | Ratio | Duration | Theory | Style |
|--------|-------|----------|--------|-------|
| News Overview 30s | 16:9 | 30s | Dmytryk | Clean hard cuts, editorial |
| On Air Promo | 16:9 | 40s | Menke | Cinematic, rhythmic |
| Social Clip | 9:16 | 15-25s | Eisenstein | Fast metric montage |
| Gen AI Remake | 16:9 | 30s | Eisenstein | Before/after, glitch effects |
| Meme Culture React | 9:16 | 15s | Eisenstein | Zoom, bold text, punchline |
| Product Landing | 16:9 | 20s | Dmytryk | Clean, modern, sales |

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
