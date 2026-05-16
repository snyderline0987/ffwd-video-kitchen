# Video Kitchen — Agent Knowledge Base

> This file teaches any agent how to cook videos with Video Kitchen.
> Read this when you need to create teasers, motion templates, compositions, or recipes.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Creating a Motion Template](#creating-a-motion-template)
3. [Creating a HyperFrames Composition](#creating-a-hyperframes-composition)
4. [Creating a Recipe](#creating-a-recipe)
5. [Template HTML Patterns](#template-html-patterns)
6. [Animation Conventions](#animation-conventions)
7. [Fonts & CI](#fonts--ci)
8. [URL Parameters](#url-parameters)
9. [Common Pitfalls](#common-pitfalls)
10. [Film Theory Quick Reference](#film-theory-quick-reference)

---

## Project Structure

```
skills/video-kitchen/
├── SKILL.md                        # Core skill instructions
├── KNOWLEDGE.md                    # This file
├── recipes/                        # Recipe blueprints
│   ├── {recipe-id}/
│   │   ├── config.json             # Recipe metadata
│   │   └── composition.html        # Template composition
│   ├── public/                     # Dashboard + static assets
│   │   ├── index.html              # Main dashboard
│   │   ├── fonts/                  # Wiener Melange WOFF2/WOFF
│   │   └── media/                  # Shared media assets
│   ├── reference-renders/          # Rendered reference videos
│   ├── server.js                   # Express API server
│   └── manifest.json               # Auto-generated recipe list
└── motion-templates/               # Reusable motion elements
    └── {template-id}/
        ├── config.json             # Template metadata
        ├── template.html           # The actual template
        └── media/                  # Template-specific assets
```

---

## Creating a Motion Template

A motion template is a self-contained HTML file with GSAP animations that can be embedded in compositions or previewed standalone.

### Step 1: Create the folder

```bash
mkdir -p skills/video-kitchen/motion-templates/my-template/media
```

### Step 2: Write config.json

```json
{
  "id": "my-template",
  "title": "My Template",
  "description": "What it does, when to use it.",
  "aspect_ratio": "16:9",
  "resolution": "1920x1080",
  "duration": "5s",
  "params": ["name", "role", "color"],
  "defaults": { "color": "#FF5A64" },
  "palette": ["#FF5A64", "#AAAAFA"],
  "tags": ["lower-third", "name-insert"]
}
```

**Fields:**
- `aspect_ratio`: `"16:9"` or `"9:16"` — determines iframe sizing in dashboard
- `params`: URL parameters the template accepts (shown in Copy Tag)
- `defaults`: Default values for params
- `palette`: Color swatches shown in dashboard (optional)
- `tags`: For filtering/searching

### Step 3: Write template.html

Use the patterns below. The template must:
1. Load GSAP from CDN
2. Build a GSAP timeline
3. Expose `window.__timelines` and `window.__duration`
4. Listen for `hf-seek` events (for HyperFrames rendering)
5. Support URL parameter configuration
6. Optionally show a config panel on `E` key press

### Step 4: Include media

Copy any fonts, videos, or images into the template's `media/` folder. Reference them with relative paths: `media/my-video.webm`.

The dashboard auto-discovers new templates via the `/api/motion-templates` API.

---

## Creating a HyperFrames Composition

A composition is an HTML file that HyperFrames renders frame-by-frame to produce a video.

### Minimal composition

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #000; overflow: hidden; width: 1920px; height: 1080px; }
</style>
</head>
<body>

<div data-composition-id="main">

  <!-- Video clips on alternating tracks for crossfade -->
  <video src="clip1.mp4" muted playsinline
    data-track-index="0" data-start="0" data-duration="4"></video>
  <video src="clip2.mp4" muted playsinline
    data-track-index="1" data-start="3.5" data-duration="5"></video>

  <!-- Text overlay -->
  <div class="headline" data-track-index="0" data-start="0" data-duration="4">
    Breaking Story
  </div>

</div>

<script>
  var tl = gsap.timeline({ paused: true });
  // ... animations ...

  window.__timelines = [tl];
  window.__duration = 30;
</script>
</body>
</html>
```

### Required attributes

| Attribute | On | Purpose |
|-----------|-----|---------|
| `data-composition-id` | Root div | HyperFrames identifies compositions |
| `data-track-index` | All timed elements | Alternating 0/1 for crossfade |
| `data-start` | Video/audio elements | When the element appears (seconds) |
| `data-duration` | Video/audio elements | How long it plays (seconds) |
| `muted playsinline` | All `<video>` | Required for autoplay in Chromium |

### Track layout

```
Track 0: [clip1]──────[clip3]──────[clip5]
Track 1: ──────[clip2]──────[clip4]──────
```

Alternate `data-track-index` between 0 and 1. Overlapping clips on the same track will conflict.

### Crossfade pattern

```javascript
// Fade out track 0 clip, fade in track 1 clip
tl.to('#clip1', { opacity: 0, duration: 0.5 }, 3.5)  // start fading at 3.5s
  .from('#clip2', { opacity: 0, duration: 0.5 }, 3.5); // fade in at same time
```

---

## Creating a Recipe

A recipe defines the structure, pacing, and editing theory for a video format.

### config.json

```json
{
  "id": "my-recipe",
  "title": "My Recipe Format",
  "aspect_ratio": "16:9",
  "duration": "30s",
  "description": "What this recipe produces.",
  "theory": "Dmytryk (Seven Rules of Cutting)",
  "prompt": "Detailed instructions for the agent on how to structure this format.",
  "vo_pref": "Nova (warm, authoritative)",
  "music_pref": "Orchestral / Dramatic (15% Vol)",
  "cut_style": "Dmytryk clean cuts. Never cut on the same frame twice. Emotion > continuity.",
  "structure": [
    { "section": "Hook", "duration": "4s", "description": "Strongest shot + bold headline" },
    { "section": "Context", "duration": "8s", "description": "Establishing shots + context VO" },
    { "section": "Facts", "duration": "14s", "description": "Rapid-fire clips + supporting VO" },
    { "section": "CTA", "duration": "4s", "description": "Call to action + outro card" }
  ],
  "clip_count": { "min": 5, "max": 8 },
  "colors": {
    "primary": "#e50914",
    "background": "#0a0a0a",
    "text": "#ffffff"
  }
}
```

---

## Template HTML Patterns

### Viewport setup

**16:9 (landscape):**
```css
body { background: transparent; overflow: hidden; width: 1920px; height: 1080px; }
```

**9:16 (vertical):**
```css
body { background: transparent; overflow: hidden; font-family: 'WienerMelange', sans-serif; }
.canvas { position: relative; width: 100vw; height: 100vh; overflow: hidden; }
```

### Transparency grid (shows checkerboard when background is transparent)

```css
.trans-grid {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background-image:
    linear-gradient(45deg, #e0e0e0 25%, transparent 25%),
    linear-gradient(-45deg, #e0e0e0 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #e0e0e0 75%),
    linear-gradient(-45deg, transparent 75%, #e0e0e0 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
  opacity: 0.4;
  pointer-events: none;
}
```

### Text overlay (name + role)

```html
<div id="text-overlay">
  <div id="bb-name">Vorname Name</div>
  <div id="bb-role">Position</div>
</div>
```

```css
#text-overlay {
  position: absolute;
  display: flex; flex-direction: column; justify-content: center;
  opacity: 0; /* GSAP handles visibility */
}
#bb-name {
  color: #fff;
  font-size: clamp(28px, 4.5vw, 80px);
  font-weight: 800;
  line-height: 1.1;
}
#bb-role {
  color: rgba(255,255,255,0.9);
  font-size: clamp(14px, 2.2vw, 40px);
  font-weight: 400;
  margin-top: 2px;
}
```

### Config panel (press E to toggle)

```html
<div class="config" id="config-panel">
  <h3>Configure</h3>
  <label>Name</label>
  <input id="cfg-name" value="Vorname Name" />
  <label>Role</label>
  <input id="cfg-role" value="Position" />
  <button onclick="applyConfig()">Apply</button>
  <button class="secondary" onclick="replayAnimation()">▶ Replay</button>
</div>
```

```css
.config {
  position: fixed; top: 20px; right: 20px;
  background: rgba(0,0,0,0.92); border: 1px solid #333;
  border-radius: 12px; padding: 24px;
  pointer-events: all; display: none;
  color: #fff; backdrop-filter: blur(12px); z-index: 100;
}
.config.show { display: block; }
```

---

## Animation Conventions

### GSAP timeline setup

```javascript
var tl = gsap.timeline({ paused: true });

// Build animation
tl.from('#element', { opacity: 0, x: -100, duration: 0.6, ease: 'power3.out' })
  .to('#element', { opacity: 0, duration: 0.3 }, '+=2');

// Required for HyperFrames
window.__timelines = [tl];
window.__duration = 5;  // total seconds
```

### hf-seek listener (required for rendering)

```javascript
window.addEventListener('hf-seek', function(e) {
  var t = (e && e.detail && e.detail.time != null) ? e.detail.time : 0;
  if (tl) { tl.time(t); tl.pause(); }
  // Also seek any videos
  document.querySelectorAll('video').forEach(v => { v.currentTime = t; });
});
```

### Crop reveal (slide in from left)

```javascript
tl.fromTo('#bb-bar',
  { clipPath: 'inset(0 100% 0 0)' },
  { clipPath: 'inset(0 0% 0 0)', duration: 0.5, ease: 'power3.out' }
);
```

### Fade in/out text

```javascript
tl.to('#text-overlay', { opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.4)
  .to('#text-overlay', { opacity: 0, duration: 0.3, ease: 'power2.in' }, 4.2);
```

### Loop badge (for looping templates)

```html
<div class="loop-badge">↻ LOOP</div>
```

---

## Fonts & CI

### Wiener Melange

The primary display font for all FFWD / Wien-branded templates.

**Files:** `public/fonts/WienerMelange_W_Rg.woff2`, `WienerMelange_W_Bd.woff2`, `WienerMelange_W_ExBd.woff2`

```css
@font-face {
  font-family: 'WienerMelange';
  src: url('fonts/WienerMelange_W_Rg.woff2') format('woff2'),
       url('fonts/WienerMelange_W_Rg.woff') format('woff');
  font-weight: 400;
}
@font-face {
  font-family: 'WienerMelange';
  src: url('fonts/WienerMelange_W_ExBd.woff2') format('woff2'),
       url('fonts/WienerMelange_W_ExBd.woff') format('woff');
  font-weight: 800;
}
```

**Usage:** `font-family: 'WienerMelange', sans-serif;`

### Stadt Wien CI Palette

For templates using the official Stadt Wien corporate identity:

| Color | Hex |
|-------|-----|
| Coral Red | `#FF5A64` |
| Lavender | `#AAAAFA` |
| Deep Purple | `#462346` |
| Mint Green | `#82D282` |
| Golden Yellow | `#E6C828` |
| Warm Gray | `#D6D1CA` |

### FFWD Brand

- Primary red: `#e50914`
- Background: `#0a0a0a`
- Card background: `#1a1a1a`

---

## URL Parameters

Templates accept configuration via URL query params:

```
template.html?name=Max+Mustermann&role=B%C3%BCrgermeister&color=%23FF5A64
```

**Reading params in JS:**

```javascript
var params = new URLSearchParams(window.location.search);
if (params.get('name')) {
  document.getElementById('bb-name').textContent = params.get('name');
}
if (params.get('color')) {
  document.getElementById('bb-bar').style.background = params.get('color');
}
```

**Common params:**

| Param | Used by | Example |
|-------|---------|---------|
| `name` | All inserts | `Max+Mustermann` |
| `role` | All inserts | `B%C3%BCrgermeister` |
| `color` | Stadt Wien, Bauchbinde | `%23FF5A64` |
| `title` | Opener, Teaser | `Breaking+News` |
| `subtitle` | Opener | `Live+aus+Wien` |

---

## Common Pitfalls

### ❌ Don't use Tailwind dynamic classes in innerHTML

```javascript
// BAD — Tailwind can't process this
element.innerHTML = `<div class="w-[${width}px]">...</div>`;

// GOOD — use inline styles
element.innerHTML = `<div style="width:${width}px">...</div>`;
```

### ❌ Don't set opacity: 0 in static CSS

```css
/* BAD — HyperFrames won't see the element */
#my-element { opacity: 0; }

/* GOOD — let GSAP handle it */
gsap.set('#my-element', { opacity: 0 });
```

### ❌ Don't forget muted playsinline on video elements

```html
<!-- BAD — video won't autoplay in headless Chromium -->
<video src="clip.mp4">

<!-- GOOD -->
<video src="clip.mp4" muted playsinline>
```

### ❌ Don't use relative paths outside the template folder

```html
<!-- BAD — breaks when served from new location -->
<video src="../../public/media/rapid-fill.webm">

<!-- GOOD — media lives in the template's own folder -->
<video src="media/rapid-fill.webm">
```

### ❌ Don't forget data-track-index

Every timed element in a composition needs `data-track-index`. Without it, HyperFrames doesn't know which track to place it on.

### ✅ Source clips need dense keyframes

```bash
ffmpeg -i input.mp4 -g 30 -keyint_min 30 -an output.mp4
```

This ensures frame-accurate seeking during rendering.

### ✅ window.__timelines must be a GSAP timeline

Not a plain object, not an array of numbers. It must be a `gsap.timeline()` instance.

---

## Film Theory Quick Reference

When building cuts, follow one of these frameworks:

### Walter Murch — Rule of Six
Rank cuts by: Emotion (6) > Story (5) > Rhythm (4) > Eye-trace (3) > 2D plane (2) > 3D space (1). If the cut serves emotion, it's justified even if it breaks everything else.

### Edward Dmytryk — Seven Rules
1. Don't cut unless there's a reason
2. Never cut on the same frame twice
3. Emotion > continuity
4. Cut on action, not stillness
5. Fresh angle every cut
6. Close-ups carry emotion
7. Action matching across cuts

### Sergei Eisenstein — Five Methods of Montage
1. **Metric** — cuts at regular intervals (beat sync)
2. **Rhythmic** — cuts follow movement within frame
3. **Tonal** — cuts follow emotional tone
4. **Overtonal** — cuts follow abstract associations
5. **Intellectual** — cuts create conceptual meaning

### Sally Menke — Tarantino's Editor
- Dialogue cuts should feel natural, not mechanical
- Hold on reactions — the response is often more important than the line
- Use long takes to build tension before cutting
- Sound design drives cut rhythm as much as visuals

---

## Quick Start Checklist

When building a new video, ask:

1. ✅ What recipe? (defines structure, theory, pacing)
2. ✅ What aspect ratio? (16:9 or 9:16)
3. ✅ How many clips? (check recipe's clip_count range)
4. ✅ Need VO? (check recipe's vo_pref)
5. ✅ Need music? (check recipe's music_pref)
6. ✅ Need motion templates? (lower thirds, inserts, openers)
7. ✅ All videos have dense keyframes? (`-g 30 -keyint_min 30`)
8. ✅ All elements have `data-track-index`?
9. ✅ `window.__timelines` is a GSAP timeline?
10. ✅ `hf-seek` listener is wired up?
