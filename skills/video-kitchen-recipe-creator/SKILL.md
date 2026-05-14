---
name: video-kitchen-recipe-creator
description: Create, document, and publish new video recipes for Video Kitchen. A recipe defines the format, emotional arc, editing theory (using film-editing-theory), and Hyperframes HTML template for a specific video style. Also maintains the dashboard listing all recipes. Use this when the user asks to create a new video recipe, template, or format for Video Kitchen.
---

# Video Kitchen Recipe Creator

This skill guides the agent in creating **new, repeatable video recipes** for Video Kitchen.

A "Recipe" is a modular blueprint for generating a specific type of video. Each recipe is a folder containing:
- `config.json` — Metadata (title, duration, theory, prompt, etc.)
- `composition.html` — A Hyperframes HTML example showing the visual style

## Architecture: Modular Recipes

Recipes live in `skills/video-kitchen/recipes/` as self-contained folders:

```
recipes/
├── manifest.json              # Auto-generated index of all recipes + templates
├── build-manifest.py          # Run after adding/removing recipes
├── server.js                  # Optional API server (port 8080)
├── public/
│   ├── index.html             # Self-contained dashboard
│   ├── composition-opener.html    # Motion template
│   └── composition-lower-third.html
├── news_overview_30s/
│   ├── config.json
│   └── composition.html       # Example Hyperframes composition
├── on_air_promo_longform/
│   ├── config.json
│   └── composition.html
└── [new-recipe]/              # Drop-in: add folder = new recipe
    ├── config.json
    └── composition.html
```

**Add a recipe** = create folder with config.json + composition.html
**Remove a recipe** = delete the folder
**After any change** = run `python3 build-manifest.py` to update the index

## Recipe Generation Workflow

### Step 0: Source Analysis (ALWAYS FIRST)
Every Video Kitchen production starts by analyzing the source material.

**Run the source analyzer:**
```bash
python3 skills/video-kitchen/recipes/analyze-source.py source_video.mp4
```

This creates an `analysis/` directory with:
- `thumbnails/` — mid-frame JPGs for each segment (vision analysis input)
- `audio.wav` — extracted audio for transcription
- `manifest.json` — structured clip data (timestamps, brightness, motion)

**Then analyze thumbnails with the vision model:**
- Feed thumbnails to the image model (max 20 per call)
- For each clip, determine:
  - `content_type`: `talking_head` (skip for teasers) | `crowd` (atmosphere) | `action` (energy)
  - `teaser_rating`: 1-5 (5 = hero shot, 1 = skip)
  - `description`: 1-2 sentence visual description
- Update `manifest.json` with ratings

**Transcribe audio:**
```bash
npx hyperframes transcribe analysis/audio.wav
```
- Adds time-stamped text to the manifest
- Used for context understanding and potential captions

**Clip selection rules (based on ratings):**
- ⭐⭐⭐⭐⭐ (5) — Hero shots, openers, key moments
- ⭐⭐⭐⭐ (4) — Strong atmosphere, good energy
- ⭐⭐⭐ (3) — Usable as B-roll, transitions
- ⭐⭐ (2) — Talking heads, only if needed for context
- ⭐ (1) — Skip unless essential for narrative
- **Never** open a teaser with clip rating ≤ 2
- **Always** prefer `action` > `crowd` > `talking_head`
- **Prioritize** night/low-light clips for drama, day clips for context

**Output:** A rated, described manifest with transcription → feed to recipe step.

### Step 1: Define the Purpose and Arc
- What is the goal of this video format? (e.g., Sales, News, TikTok meme, Explainer)
- What is the target duration and aspect ratio?
- Define the narrative arc (e.g., Hook → Problem → Solution → CTA).

### Step 2: Apply Film Editing Theory
Read the `film-editing-theory` skill.
- Decide which canonical framework governs this recipe:
  - **Murch:** Emotion-driven, hiding cuts on action/blinks (documentaries, emotional promos)
  - **Dmytryk:** Substance first, holding shots (news, informational content)
  - **Eisenstein:** Metric/Rhythmic montage, collision (social media, viral hooks, intense teasers)
  - **Menke/Tarantino:** Dialogue/beat driven, mini-films (on-air promos, episodic content)
- Explicitly state the editing rules for this recipe based on the theory.

### Step 3: Create config.json
Save to `skills/video-kitchen/recipes/RECIPE_ID/config.json`:

```json
{
  "id": "recipe_id",
  "title": "Recipe Title",
  "aspect_ratio": "16:9",
  "duration": "30s",
  "description": "Short description of what this recipe produces.",
  "theory": "Framework (Detail)",
  "prompt": "AI prompt for generating content with this recipe.",
  "vo_pref": "Voice preference",
  "music_pref": "Music preference",
  "cut_style": "Description of cutting rules."
}
```

### Step 4: Create composition.html
Create a Hyperframes HTML example in the same folder. This is the visual reference for the recipe.

**Required structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>Recipe Name — FFWD Video Kitchen</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  body { background: #0a0a0a; overflow: hidden; width: 1920px; height: 1080px; }
</style>
</head>
<body>
  <!-- Scenes with placeholder content -->

  <script>
  (function() {
    var tl = gsap.timeline({ paused: false });
    window.__timelines = window.__timelines || [];
    window.__timelines.push(tl);
    
    // GSAP animations following the recipe's theory
    
    window.addEventListener('hf-seek', function(e) {
      var t = (e && e.detail && e.detail.time != null) ? e.detail.time : 0;
      tl.time(t);
      tl.pause();
    });
  })();
  </script>
</body>
</html>
```

**Style guide:**
- Dark background (#0a0a0a) or transparent for overlays
- FFWD red accent (#e50914)
- GSAP for all animations, `window.__timelines` + `hf-seek` for Hyperframes compatibility
- Tailwind CSS via CDN
- Vary eases, speeds, directions, and staggers (see hyperframes motion-principles)
- Duration should match the recipe config
- Use placeholder content (no real footage)

### Step 5: Update Manifest
After creating (or removing) any recipe, regenerate the manifest:
```bash
cd skills/video-kitchen/recipes && python3 build-manifest.py
```

### Step 6: Update Dashboard (if needed)
The dashboard at `public/index.html` is self-contained — it reads from `manifest.json` when the server isn't running, or from `/api/recipes` when it is. No dashboard edits needed for new recipes.

## Motion Templates
Motion templates (lower thirds, openers, bumpers) live in `public/` as `composition-*.html` files. Follow the same Hyperframes structure but with transparent backgrounds and shorter durations (3-5s).

To add a new motion template:
1. Create `public/composition-template-name.html`
2. Run `python3 build-manifest.py`
3. Add a card in the dashboard's Motion Templates tab (edit `public/index.html`)
