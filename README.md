# Video Kitchen in a Box 🎬📦

A fully local, agentic video production studio powered by OpenClaw and Hyperframes. Ship it in Docker, feed it footage, get broadcast-ready video.

## What It Does

Video Kitchen turns raw footage into edited videos using AI-powered agent skills:
- **6 recipe formats** — News, On-Air Promo, Social Clip, Gen AI Remake, Meme React, Product Landing
- **Motion templates** — Animated openers, lower thirds, CI elements (GSAP-powered)
- **Film theory engine** — Every cut follows editing rules (Dmytryk, Menke, Eisenstein, Murch)
- **100% local** — No footage uploads. Your data stays on your machine.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/snyderline0987/video-kitchen-box.git
cd video-kitchen-box

# 2. Configure
cp .env.example .env
# Edit .env with your API keys (Gemini, OpenAI, or OpenRouter)

# 3. Launch
docker-compose up -d

# 4. Use
# Dashboard: http://localhost:8080
# Agent Chat: http://localhost:3000
```

## Architecture

```
┌─────────────────────────────────────────────┐
│  Docker Container                           │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │  OpenClaw    │  │  Recipe Dashboard    │  │
│  │  Agent       │  │  :8080               │  │
│  │  :3000       │  │                      │  │
│  └──────┬───────┘  └──────────────────────┘  │
│         │                                    │
│  ┌──────┴───────────────────────────────┐    │
│  │  Skills                              │    │
│  │  ├ video-kitchen/    (core pipeline) │    │
│  │  ├ hyperframes/      (compositions)  │    │
│  │  ├ film-editing-theory/ (cut rules)  │    │
│  │  ├ open-design/      (CI elements)   │    │
│  │  └ recipe-creator/   (make recipes)  │    │
│  └──────────────────────────────────────┘    │
│         │                                    │
│  ┌──────┴───────────────────────────────┐    │
│  │  Recipes (modular)                   │    │
│  │  ├ news_overview_30s/                │    │
│  │  ├ on_air_promo_longform/            │    │
│  │  ├ social_clip_9x16/                 │    │
│  │  ├ gen_ai_remake/                    │    │
│  │  ├ meme_culture_react/               │    │
│  │  ├ product_landing_page/             │    │
│  │  └ public/  (motion templates)       │    │
│  └──────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Recipes

Each recipe is a folder with:
- `config.json` — Metadata (theory, duration, aspect ratio, prompt, cut style)
- `composition.html` — Hyperframes HTML example showing the visual style

| Recipe | Ratio | Duration | Theory | Style |
|--------|-------|----------|--------|-------|
| News Overview 30s | 16:9 | 30s | Dmytryk | Clean hard cuts, editorial |
| On Air Promo | 16:9 | 40s | Menke | Cinematic, rhythmic |
| Social Clip | 9:16 | 15-25s | Eisenstein | Fast metric montage |
| Gen AI Remake | 16:9 | 30s | Eisenstein | Before/after, glitch effects |
| Meme Culture React | 9:16 | 15s | Eisenstein | Zoom, bold text, punchline |
| Product Landing | 16:9 | 20s | Dmytryk | Clean, modern, sales |

### Add / Remove Recipes

Recipes are modular folders:
```bash
# Add: create folder + config + composition
mkdir skills/video-kitchen/recipes/my-recipe
# ... add config.json and composition.html

# Update index
cd skills/video-kitchen/recipes && python3 build-manifest.py

# Remove: delete the folder, rebuild manifest
```

## Motion Templates

Animated CI elements (GSAP-powered, Hyperframes-compatible):
- **FFWD Opener** — 5s animated logo open
- **FFWD Lower Third** — Name + title bar with skew animation

Add templates as `public/composition-*.html` and rebuild manifest.

## Development Mode

For hacking on skills without rebuilding Docker:

```bash
# Use the dev override in docker-compose.yml
# Uncomment video-kitchen-dev, comment out video-kitchen
docker-compose up -d
```

Skills mount live from your local folder — changes take effect on agent restart.

## Ports

| Port | Service |
|------|---------|
| 3000 | OpenClaw Agent (chat interface) |
| 8080 | Recipe Dashboard |
| 3002 | Hyperframes Preview Studio |

## Requirements

- Docker + Docker Compose
- At least one AI provider API key (Gemini, OpenAI, or OpenRouter)
- Raw video footage (mount via `RAW_FOOTAGE_PATH`)

## License

MIT
