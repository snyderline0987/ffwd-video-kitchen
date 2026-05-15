# AGENTS.md — Video Kitchen Box

You are a video production agent. This skill bundle gives you everything you need to turn raw footage into broadcast-ready video.

## Skills

Load these in order when a video task comes in:

1. **film-editing-theory** — Cut rules (Murch, Dmytryk, Eisenstein, Menke). Read this BEFORE making any cut decisions.
2. **video-kitchen** — Core pipeline: analyze source → match recipe → build composition → render.
3. **video-kitchen-recipe-creator** — Create new recipe formats when needed.
4. **hyperframes** — HTML-based video compositions, animations, rendering.
5. **open-design** — CI elements, motion templates, brand assets.

## Workflow

```
Raw footage → analyze-source.py → manifest.json → pick recipe → build HyperFrames composition → render → output
```

1. **Analyze** — Run `analyze-source.py` on the source video. It uses PySceneDetect for content-aware scene detection.
2. **Transcribe** — Transcribe the extracted audio for captions/voiceover timing.
3. **Pick a recipe** — Match the footage to one of the 6 built-in recipes (or create a new one).
4. **Build composition** — Create a HyperFrames HTML composition following the recipe's style and film theory rules.
5. **Render** — Output the final video.

## Recipes

| Recipe | Ratio | Duration | Theory |
|--------|-------|----------|--------|
| News Overview 30s | 16:9 | 30s | Dmytryk |
| On Air Promo | 16:9 | 40s | Menke |
| Social Clip | 9:16 | 15-25s | Eisenstein |
| Gen AI Remake | 16:9 | 30s | Eisenstein |
| Meme Culture React | 9:16 | 15s | Eisenstein |
| Product Landing | 16:9 | 20s | Dmytryk |

## Key Files

- `skills/video-kitchen/recipes/` — Recipe configs + compositions
- `skills/video-kitchen/recipes/analyze-source.py` — Source analyzer (PySceneDetect)
- `skills/video-kitchen/recipes/server.js` — Recipe dashboard API
- `skills/hyperframes/` — Composition framework
- `workspace/` — Default workspace with SOUL.md and IDENTITY.md

## Dashboard

```bash
cd skills/video-kitchen/recipes && npm install && node server.js
# → http://localhost:8080/dashboard.html
```
