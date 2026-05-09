---
name: video-kitchen-recipe-creator
description: Create, document, and publish new video recipes for Video Kitchen 2.1. A recipe defines the format, emotional arc, editing theory (using film-editing-theory), and Hyperframes HTML template for a specific video style. Also maintains a local website listing all recipes in FFWD style. Use this when the user asks to create a new video recipe, template, or format for Video Kitchen.
---

# Video Kitchen Recipe Creator

This skill guides the agent in creating **new, repeatable video recipes** for Video Kitchen 2.1. 

A "Recipe" is a blueprint for generating a specific type of video. It defines the narrative arc, the editing philosophy, and the exact Hyperframes HTML template needed to render it.

## 1. Recipe Generation Workflow

When asked to create a new recipe, follow these steps exactly:

### Step 1: Define the Purpose and Arc
- What is the goal of this video format? (e.g., Sales, News, TikTok meme, Explainer)
- What is the target duration and aspect ratio?
- Define the narrative arc (e.g., Hook → Problem → Solution → CTA).

### Step 2: Apply Film Editing Theory
Read the `film-editing-theory` skill (`/workspace/.agents/skills/film-editing-theory/SKILL.md`).
- Decide which canonical framework governs this recipe:
  - **Murch:** Emotion-driven, hiding cuts on action/blinks (good for documentaries, emotional promos).
  - **Dmytryk:** Substance first, holding shots (good for news, informational content).
  - **Eisenstein:** Metric/Rhythmic montage, collision (good for social media, viral hooks, intense teasers).
  - **Menke/Tarantino:** Dialogue/beat driven, mini-films (good for on-air promos, episodic content).
- Explicitly state the editing rules for this recipe based on the theory.

### Step 3: Design the Hyperframes Template
Create the boilerplate `index.html` structure for this recipe.
- Define the necessary tracks (e.g., Track 0: B-Roll, Track 1: VO, Track 2: Music, Track 3: Overlays).
- Add the necessary GSAP timeline (`window.__timelines`) with placeholder animations (e.g., Ken Burns effect, text overlays, transitions).
- Keep it aligned with the Video Kitchen 2.1 standards (no audio in video clips, TTS on separate track).

### Step 4: Write the Recipe File
Save the complete recipe as a Markdown file in `/workspace/video-kitchen-2.1/recipes/RECIPE_NAME.md`.
It must include: Purpose, Editing Theory (with citations), Pipeline modifications, and the HTML Template code block.

### Step 5: Update the Recipe Gallery Website
We maintain a local, visually appealing "FFWD style" website to list all available recipes.
- Update or create `/workspace/video-kitchen-2.1/recipes/index.html`.
- This file should be a dark-mode, modern dashboard (Tailwind CSS via CDN is recommended) displaying cards for each recipe.
- Each card should show: Recipe Title, Duration, Aspect Ratio, Editing Framework used, and a short description.
- To view the gallery, the user can start a local server (e.g., `python3 -m http.server 8080` in the `recipes` folder) or open the HTML file.

---

## FFWD Style Gallery Template (Example)

When updating the gallery `index.html`, ensure it looks premium, dark, and cinematic (FFWD style).

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Kitchen 2.1 - Recipe Gallery</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0a0a0a; color: #ededed; }
        .recipe-card { background-color: #1a1a1a; border: 1px solid #333; transition: all 0.3s ease; }
        .recipe-card:hover { border-color: #e50914; transform: translateY(-2px); box-shadow: 0 10px 20px -10px rgba(229,9,20,0.3); }
        .badge { background: #333; color: #aaa; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
        .theory-badge { background: rgba(229,9,20,0.1); color: #e50914; border: 1px solid rgba(229,9,20,0.3); }
    </style>
</head>
<body class="p-10 font-sans antialiased">
    <header class="mb-12 border-b border-gray-800 pb-6">
        <h1 class="text-4xl font-bold tracking-tight mb-2">🍳 Video Kitchen <span class="text-red-600">Recipes</span></h1>
        <p class="text-gray-400">Available templates and editing frameworks for automated video generation.</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="recipe-grid">
        <!-- Recipe Card Example -->
        <div class="recipe-card p-6 rounded-lg">
            <div class="flex justify-between items-start mb-4">
                <h2 class="text-xl font-bold">News Overview 30s</h2>
                <div class="flex gap-2">
                    <span class="badge">16:9</span>
                    <span class="badge">30s</span>
                </div>
            </div>
            <p class="text-gray-400 mb-4 text-sm">A fast-paced summary of a news piece. Hook → Context → Key Fact → Wrap.</p>
            <div class="mb-4">
                <span class="badge theory-badge">Theory: Dmytryk (Substance First)</span>
            </div>
            <a href="news_overview_30s.md" class="text-red-500 hover:text-red-400 text-sm font-semibold flex items-center gap-1">
                View Template Details &rarr;
            </a>
        </div>
        <!-- Add new recipes here -->
    </div>
</body>
</html>
```

## Agent Instructions during execution:
1. "I will read the film-editing-theory skill to define the cutting rules."
2. "I am designing the Hyperframes template."
3. "I have created the recipe markdown file."
4. "I have updated the Recipe Gallery index.html. You can view it by running `cd /workspace/video-kitchen-2.1/recipes && python3 -m http.server 8080` and opening http://localhost:8080".
