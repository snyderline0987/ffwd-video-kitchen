---
name: motion-template-creator
description: Create, design, and publish motion templates for Video Kitchen. Mimics FCPX Motion Templates and Adobe Essential Graphics workflows. Use when the user asks to create a new motion template, name insert, lower third, opener, ticker, transition, or any reusable animated element. Asks about CI, fonts, colors, aspect ratio, and animation style. Saves to skills/video-kitchen/motion-templates/{id}/.
---

# Motion Template Creator

This skill guides the agent through creating **professional motion templates** for Video Kitchen — reusable animated elements like lower thirds, name inserts, openers, tickers, transitions, and overlays.

Think of it as building an **FCPX Motion Template** or **Adobe Essential Graphic** — but as HTML + GSAP that renders deterministically via HyperFrames.

## Workflow

When asked to create a motion template, follow these steps in order. **Ask the user questions at each step before proceeding.**

---

### Step 1: Discover the Template Type

Ask the user what they need. Common types:

| Type | Description | Example |
|------|-------------|---------|
| **Name Insert** | Person name + role overlay | "Steffen Hofmann · Mittelfeldspieler" |
| **Lower Third** | Title bar with text, bottom of screen | "BREAKING NEWS" |
| **Opener / Bumper** | Full-screen intro animation | Show logo reveal + title |
| **Ticker** | Scrolling text bar | News headlines crawl |
| **Transition** | Clip-to-clip transition effect | Wipe, dissolve, glitch |
| **Call to Action** | End card with CTA text + URL | "Follow us @ffwd" |
| **Score Bug** | Live score overlay | "AUT 3:2 GER" |
| **Sidebar** | Vertical info bar | Social media handles, hashtags |
| **Countdown** | Timer animation | "Coming up in 10... 9... 8..." |
| **Watermark / Bug** | Persistent logo overlay | Channel logo, corner badge |

If the user doesn't specify, **show this list and ask them to pick.**

---

### Step 2: Gather Requirements

Ask these questions (adapt to context, don't ask obvious ones):

**Visual:**
- What aspect ratio? (16:9 landscape, 9:16 vertical, 1:1 square, or responsive?)
- Transparent background or solid? (Most inserts are transparent for compositing)
- What color scheme? (If CI exists, get the brand colors)
- Any reference? (Screenshot, existing template, FCPX screenshot, Figma link)

**CI / Brand:**
- Is there a corporate identity? (Stadt Wien, FFWD, custom)
- Which font? (Wiener Melange, Inter, custom — offer to use what we have)
- Colors? (Ask for hex values or describe. Check if palette exists in any config.json)
- Logo needed? (Ask for file or skip)

**Content:**
- What text fields? (name, role, title, subtitle, etc.)
- Default text values? (For preview — e.g., "Vorname Name" / "Position")
- Any media assets? (Fill video, logo file, background image)

**Animation:**
- How should it appear? (Slide in from left, fade up, crop reveal, scale up, glitch in)
- How should it disappear? (Reverse, fade out, slide off)
- Loop or one-shot?
- Duration? (Typical: 3-8 seconds)
- Easing? (Power out = smooth deceleration, Back out = overshoot, Elastic = bouncy)

**Behavior:**
- Should it have a live config panel? (Press E to edit — recommended for all inserts)
- URL params for remote config? (name, role, color, etc.)
- Video fill background? (Like the rapid insert — plays a video behind the overlay)

---

### Step 3: Check Existing Templates for Patterns

Before writing code, read the most relevant existing template for reference:

```bash
# List available templates
ls skills/video-kitchen/motion-templates/

# Read the closest match
cat skills/video-kitchen/motion-templates/{similar-template}/template.html
cat skills/video-kitchen/motion-templates/{similar-template}/config.json
```

Also read `skills/video-kitchen/KNOWLEDGE.md` for the template conventions and HTML patterns.

**Template mapping:**
- Name insert → read `stadt-wien-insert` or `composition-bauchbinde`
- Lower third → read `bauchbinde`
- Video-fill overlay → read `composition-rapid-insert` or `rapid-insert-16x9`
- Opener → ask user for specifics (usually custom)

---

### Step 4: Create the Template Folder

```bash
mkdir -p skills/video-kitchen/motion-templates/{template-id}/media
```

**Naming convention:** lowercase-with-hyphens, descriptive. Examples:
- `sport-ticker-16x9`
- `breakings-news-lower-third`
- `esc-score-bug`
- `wien-opener-9x16`

---

### Step 5: Write config.json

```json
{
  "id": "{template-id}",
  "title": "Human-Readable Title",
  "description": "What it does, when to use it, what it looks like.",
  "aspect_ratio": "16:9",
  "resolution": "1920x1080",
  "duration": "5s",
  "params": ["name", "role", "color"],
  "defaults": {
    "name": "Vorname Name",
    "role": "Position",
    "color": "#FF5A64"
  },
  "palette": ["#FF5A64", "#AAAAFA"],
  "fonts": ["WienerMelange"],
  "hasFillVideo": false,
  "tags": ["lower-third", "name-insert", "wien"]
}
```

**Field reference:**
- `aspect_ratio`: `"16:9"`, `"9:16"`, or `"1:1"` — controls dashboard card layout
- `resolution`: Native render resolution string
- `params`: URL params the template accepts (auto-generates Copy Tag URL)
- `defaults`: Default values (used in preview and Copy Tag)
- `palette`: Color swatches for the dashboard (optional, only if color is configurable)
- `fonts`: Which custom fonts are used (for dependency tracking)
- `hasFillVideo`: true if the template plays a background video
- `tags`: For search/filter (max 4-5)

---

### Step 6: Write template.html

Every template must follow this structure:

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>{Template Title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
  /* 1. Font faces */
  @font-face { font-family: 'WienerMelange'; src: url('fonts/WienerMelange_W_Rg.woff2')... }

  /* 2. Reset */
  * { margin: 0; padding: 0; box-sizing: border-box; }

  /* 3. Body — fixed dimensions for 16:9, viewport for 9:16 */
  body { background: transparent; overflow: hidden; width: 1920px; height: 1080px; }

  /* 4. Canvas wrapper */
  .canvas { position: relative; width: 100%; height: 100%; overflow: hidden; }

  /* 5. Transparency grid (if transparent bg) */
  .trans-grid { /* checkerboard pattern */ }

  /* 6. Element styles — NO opacity:0 in CSS, GSAP handles it */

  /* 7. Config panel */
  .config { position: fixed; top: 20px; right: 20px; display: none; }
  .config.show { display: block; }
</style>
</head>
<body>

<div class="canvas">
  <!-- Optional: transparency grid -->
  <div class="trans-grid"></div>

  <!-- Optional: fill video background -->
  <video id="fill-video" src="media/fill.webm" autoplay loop muted playsinline></video>

  <!-- Main animated elements -->
  <div id="main-element">
    <div id="text-name">Default Name</div>
    <div id="text-role">Default Role</div>
  </div>
</div>

<!-- Config panel (press E to toggle) -->
<div class="config" id="config-panel">
  <h3>{Template Name}</h3>
  <label>Name</label>
  <input id="cfg-name" value="Default Name" />
  <label>Role</label>
  <input id="cfg-role" value="Default Role" />
  <button onclick="applyConfig()">Apply</button>
  <button class="secondary" onclick="replayAnimation()">▶ Replay</button>
</div>

<!-- Loop badge if looping -->
<div class="loop-badge">↻ LOOP</div>

<script>
(function() {
  // 1. Read URL params
  var params = new URLSearchParams(window.location.search);

  // 2. Apply params to elements
  if (params.get('name')) { document.getElementById('text-name').textContent = params.get('name'); }

  // 3. Build GSAP timeline
  var tl = gsap.timeline({ paused: true, repeat: -1, repeatDelay: 1 });
  tl.from('#main-element', { clipPath: 'inset(0 100% 0 0)', duration: 0.5, ease: 'power3.out' })
    .to('#main-element', { opacity: 1, duration: 0.4 }, 0.2)
    .to('#main-element', { clipPath: 'inset(0 0% 0 0)', duration: 0.5, ease: 'power3.in' }, 4.0)
    .to('#main-element', { opacity: 0, duration: 0.3 }, 4.0);

  // 4. Expose for HyperFrames
  window.__timelines = [tl];
  window.__duration = 5;

  // 5. hf-seek listener (required for rendering)
  window.addEventListener('hf-seek', function(e) {
    var t = (e && e.detail && e.detail.time != null) ? e.detail.time : 0;
    if (tl) { tl.time(t); tl.pause(); }
    // Seek any videos
    var v = document.getElementById('fill-video');
    if (v) v.currentTime = t;
  });

  // 6. Play timeline
  tl.play();

  // 7. Config panel toggle (E key)
  document.addEventListener('keydown', function(e) {
    if (e.key === 'e' || e.key === 'E') {
      document.getElementById('config-panel').classList.toggle('show');
    }
  });

  // 8. Config apply function
  window.applyConfig = function() {
    document.getElementById('text-name').textContent = document.getElementById('cfg-name').value;
    document.getElementById('text-role').textContent = document.getElementById('cfg-role').value;
  };

  // 9. Replay function
  window.replayAnimation = function() {
    gsap.set('#main-element', { opacity: 0, clipPath: 'inset(0 100% 0 0)' });
    tl.restart();
  };
})();
</script>
</body>
</html>
```

---

### Step 7: Handle Media Assets

If the template uses any media:

```bash
# Copy assets into the template's media/ folder
cp /path/to/fill-video.webm skills/video-kitchen/motion-templates/{id}/media/
cp /path/to/logo.png skills/video-kitchen/motion-templates/{id}/media/
```

**Font handling:**
- Wiener Melange: reference via `url('fonts/WienerMelange_W_Rg.woff2')` — the dashboard serves these globally
- Custom fonts: copy the font files into the template's `media/` folder and reference them locally
- Google Fonts: use `@import url(...)` — works but adds network dependency

**Video assets:**
- Convert to VP9 WebM with alpha: `ffmpeg -i input.mov -c:v libvpx-vp9 -b:v 2M -an -pix_fmt yuva420p output.webm`
- Always include `muted playsinline` on `<video>` elements
- Reference as `media/filename.webm` (relative to template)

**Image assets:**
- PNG with transparency for logos/overlays
- SVG for scalable icons
- Reference as `media/filename.png`

---

### Step 8: Handle Fill Video Templates

If the template overlays text on a video (like FCPX's "draw on" effect):

1. The user provides the original video (MOV, MP4)
2. Convert to WebM: `ffmpeg -i input.mov -c:v libvpx-vp9 -b:v 2M -pix_fmt yuva420p media/fill.webm`
3. Position the text overlay to align with the video's bar/graphic area
4. Use percentage-based positioning so it works at any scale

The fill video already contains the graphic animation — **don't recreate it in CSS.** Just overlay text at the right position.

---

### Step 9: Verify the Template

After creation, verify:

1. **File structure:** `config.json` + `template.html` + `media/` exist
2. **Dashboard discovery:** restart the server and check `/api/motion-templates` includes it
3. **Preview works:** open `http://localhost:8080/motion-templates/{id}/template.html` in browser
4. **Config panel:** press E — inputs should update the template
5. **URL params:** test `?name=Test&role=Test` — values should apply
6. **Animation:** plays correctly, loops if intended
7. **HyperFrames ready:** `window.__timelines` is a GSAP timeline, `hf-seek` listener is wired

---

### Step 10: Commit and Push

```bash
cd /workspace/video-kitchen-box
git add skills/video-kitchen/motion-templates/{id}/
git commit -m "feat: add {template-name} motion template"
git push
```

The dashboard will auto-discover it next time the page loads.

---

## CI Presets

When the user mentions a brand, apply these presets automatically:

### Stadt Wien
- Colors: `#FF5A64`, `#AAAAFA`, `#462346`, `#82D282`, `#E6C828`, `#D6D1CA`
- Font: Wiener Melange
- Style: Clean, authoritative, bar-based inserts

### FFWD / W24
- Colors: `#e50914` (red), `#0a0a0a` (bg), `#ffffff` (text)
- Font: Wiener Melange for inserts, Inter for UI
- Style: Bold, cinematic, red accents

### ESC / Eurovision
- Colors: `#FF5A64` (coral), `#AAAAFA` (blue), gradient-heavy
- Font: Wiener Melange or Inter
- Style: Flashy, animated, gradient bars

### Custom
- Ask for: primary color, secondary color, accent, background, text color
- Ask for font preference
- Ask for reference images or Figma links

---

## Animation Style Presets

When the user doesn't specify animation style, offer these options:

| Style | Description | Best For |
|-------|-------------|----------|
| **Crop Reveal** | Clips in from left/right, text reveals | Name inserts, lower thirds |
| **Fade Up** | Text fades in from below | Subtitles, credits |
| **Slide In** | Entire element slides in from edge | Sidebars, tickers |
| **Scale Up** | Element grows from center | Opener, logo reveal |
| **Glitch** | Digital distortion effect | Gen AI, modern, tech |
| **Wipe** | Color bar wipes across | Transitions, openers |
| **Typewriter** | Text appears character by character | Headlines, codes |
| **Elastic** | Overshoot with bounce | Playful, social media |
| **Kinetic** | Fast, bold text motion | Social clips, memes |

---

## FCPX Motion Template Equivalents

Guide the user by mapping FCPX concepts to our templates:

| FCPX Template | Video Kitchen Equivalent |
|---------------|--------------------------|
| Title → Basic Title | `bauchbinde` (name + role) |
| Title → Lower Third | Custom — ask for style |
| Generator → Countdown | Custom — ask for style |
| Transition → Cross Dissolve | GSAP crossfade in composition |
| Title → Cinematic | `stadt-wien-insert` (full animation) |
| Effect → Color Correction | CSS filters on video elements |
| Title → Custom | Build new with this skill |
| Generator → Placeholder | Config panel + default values |

---

## Adobe Essential Graphic Equivalents

| After Effects / MOGRT | Video Kitchen Equivalent |
|------------------------|--------------------------|
| Text layer + expression | `<div>` + URL param |
| Shape layer | CSS/SVG in template.html |
| Pre-comp | Nested `<div>` with own animation |
| Master properties | URL params + config panel |
| Mask | `clip-path` CSS |
| Motion blur | GSAP `motionPath` or CSS filter |

---

## Agent Communication

During creation, tell the user what you're doing:

1. "I'll check existing templates for reference patterns."
2. "Building the {type} template with {CI} branding, {animation} style, {ratio}."
3. "Template created at `motion-templates/{id}/`. You can preview it at {url}."
4. "Press E in the preview to open the live config panel."
5. "Dashboard will show it automatically — refresh the Motion Templates tab."
