# 🍳 Video Kitchen 2.1 — Hyperframes Teaser Production

## Philosophy

**Kein Python. Keine Diagramme. Kein ffmpeg-Concat.**  
Video-Clips + Voiceover + Musik — gebaut als Hyperframes HTML-Composition, gerendert deterministisch.

## Standard Teaser Setup (IMMER dieses Format)

Jeder Teaser in Video Kitchen 2.1 wird als **Hyperframes Composition** gebaut:

```
Projektstruktur:
├── index.html          ← Composition (Video + Audio + GSAP)
├── hyperframes.json    ← Config
├── assets/
│   ├── scene1.mp4      ← Video-Clips (OHNE Audio!)
│   ├── scene2.mp4
│   ├── ...
│   ├── opener.webm     ← Transparentes Overlay (Konvertiert aus OPENER_GLEICH.mov)
│   ├── vo_00.mp3       ← Voiceover-Segmente
│   ├── ...
│   └── music.mp3       ← Hintergrundmusik (Immer der Standard-Track)
```

### Track-Layout (IMMER so)

```
Timeline (0s → Dauer)
├─ Track 0 (Video):  [scene1]──[scene2]──[scene3]──[scene4]──[scene5]
│                    data-track-index="0"
│                    ⚠️  Video-Clips IMMER muted + ohne Audio-Track (-an)
│
├─ Track 1 (VO):     [vo_0]────[vo_1]────[vo_2]────[vo_3]────[vo_4]
│                    data-track-index="1"
│                    data-volume="1.0"
│
├─ Track 2 (Music):  [───────────────────────────── Dauer ───────────]
│                    data-track-index="2"
│                    data-volume="0.15" (15%)
│
└─ Track 3 (Overlay):[opener]
                     data-track-index="3"
                     (Nur die ersten 4s, transparentes WebM)
```

### index.html Template

```html
<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1280, height=720" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1280px; height: 720px; overflow: hidden; background: #000; }
      video { width: 100%; height: 100%; object-fit: cover; }
      .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div id="root"
      data-composition-id="TEASER_NAME"
      data-start="0"
      data-duration="DAUER"
      data-width="1280" data-height="720">

      <!-- TRACK 0: Video (muted, kein Audio-Track) -->
      <video id="scene1" data-start="0" data-duration="7"
             data-track-index="0" src="assets/scene1.mp4" muted playsinline></video>
      <video id="scene2" data-start="7" data-duration="7"
             data-track-index="0" src="assets/scene2.mp4" muted playsinline></video>
      <!-- ... weitere Szenen -->

      <!-- TRACK 1: Voiceover -->
      <audio id="vo0" data-start="0" data-duration="7"
             data-track-index="1" data-volume="1.0" src="assets/vo_00.mp3"></audio>
      <audio id="vo1" data-start="7" data-duration="7"
             data-track-index="1" data-volume="1.0" src="assets/vo_01.mp3"></audio>
      <!-- ... weitere VO-Segmente -->

      <!-- TRACK 2: Hintergrundmusik (15% Volume) -->
      <audio id="bgmusic" data-start="0" data-duration="DAUER"
             data-track-index="2" data-volume="0.15" src="assets/music.mp3"></audio>

      <!-- TRACK 3: Opener Overlay (transparent WebM) -->
      <video id="opener" data-start="0" data-duration="4"
             data-track-index="3" src="assets/opener.webm" class="overlay" muted playsinline></video>

    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["TEASER_NAME"] = tl;
    </script>
  </body>
</html>
```

## Pipeline

```
User sendet URL / Video
        │
        ▼
┌─ INGEST & PRE-CUT ───────────────────────────┐
│ 1. web_fetch Artikel → Topic, Kontext       │
│ 2. Video download + ffprobe                  │
│ 3. PySceneDetect für exakte Szenen           │
│ 4. "source"-Comp (mit allen Szenen) in       │
│    Hyperframes anlegen & publishen           │
│ 5. Film-Strip + Cloud-Link an User senden    │
└──────────────────────────────────────────────┘
        │
        ▼
┌─ UNDERSTAND (Gemini 3.1 Pro) ────────────────┐
│ 1. Exakt 1 Frame pro erkannter Szene ziehen │
│ 2. Alle Frames + Artikel → 3.1 Pro          │
│ 3. Output: Thema, Arc, beste Szenen, VO     │
└──────────────────────────────────────────────┘
        │
        ▼
┌─ RECOMMEND ──────────────────────────────────┐
│ Storyboard-Karte an User:                    │
│ - Szenen-Auswahl + Schnittpunkte             │
│ - VO-Text pro Szene                          │
│ User bestätigt → BUILD                       │
└──────────────────────────────────────────────┘
        │
        ▼
┌─ BUILD & PREVIEW (Hyperframes) ──────────────┐
│ 1. Im selben Projekt NEUE Comp anlegen       │
│    (z.B. teaser-v1.html)                     │
│ 2. Clips (-an), VO, Musik, Opener einbauen   │
│ 3. hyperframes.json aktualisieren            │
│ 4. hyperframes publish --yes → Cloud Studio  │
│ 5. Cloud-URL an User senden                  │
└──────────────────────────────────────────────┘
        │
        ▼
┌─ ITERATION ──────────────────────────────────┐
│ 1. Wenn User Änderungen will: NEUE Comp      │
│    (z.B. teaser-v2.html) im selben Projekt   │
│ 2. Wieder publish, Cloud-Link senden         │
└──────────────────────────────────────────────┘
```

## Build-Regeln

### Szenen-Erkennung & Pre-Publish (NEU)
Um exakte, saubere Schnitte zu bekommen und den User direkt ins Projekt zu holen:

1. **Szenen-Erkennung mit PySceneDetect:**
```bash
scenedetect -i source.mp4 list-scenes save-images -n 1
```
2. **Film-Strip erstellen (Collage aus den Szenen-Frames):**
```bash
# ACHTUNG: Bei sehr vielen Szenen (z.B. > 16) bricht montage oder convert oft das Layout. 
# Besser: Eine fixe Matrix wie 6x6 oder 5x7 erzwingen, damit alle reinpassen, oder mehrere kleine Strips machen.
montage source-Scene-*.jpg -geometry 320x180+2+2 -tile 5x filmstrip_exact.jpg
```
3. **Source-Comp anlegen:**
Eine `source.html` in Hyperframes anlegen, in der alle extrahierten Szenen hintereinander liegen, und in der `hyperframes.json` eintragen.
4. **Publish & Preview:**
Das Projekt per `hyperframes publish` hochladen. Dem User den Film-Strip in Telegram plus den Cloud-Link senden. Der User hat jetzt Zugriff auf das Projekt und alle Rohszenen.

### Teaser Bauen & Iteration
1. **Neue Composition:** Wenn das Storyboard steht, überschreiben wir NICHT die `index.html` der Source. Wir erzeugen stattdessen die Haupt-Composition in `index.html` (damit sie als Default im Studio lädt) und benennen die alte `index.html` in `source.html` um (oder behalten sie einfach, aber `index.html` ist immer die aktuellste Iteration).
2. **Config Update:** In der `hyperframes.json` fügen wir die neue Comp hinzu:
```json
{
  "project": { "name": "mein-video" },
  "compositions": [
    { "id": "teaser-v1", "entry": "index.html", "width": 1280, "height": 720, "duration": 30 },
    { "id": "source-video", "entry": "source.html", "width": 1280, "height": 720, "duration": 150 }
  ]
}
```
*Tipp: Der erste Eintrag im Array ist der, der beim Öffnen des Cloud Studios standardmäßig geladen wird.*
3. Nach jedem Build wird wieder `hyperframes publish --yes` aufgerufen und dem User der Cloud-Link gesendet. Änderungen passieren immer in neuen Compositions, aber `index.html` sollte immer den aktuellen Teaser repräsentieren.

### Video-Clips schneiden & "Lip Flap" Regel (WICHTIG)
- **Kein Lip Flap:** Wenn Personen im Bild in ein Mikrofon sprechen, MUSS ihr Originalton zu hören sein. Lege niemals Voiceover oder nur Musik über sprechende Gesichter.
- **Interviews vermeiden:** Generell Szenen mit sprechenden Personen meiden. Lieber starkes B-Roll / Schnittbilder zeigen.
- **Ausnahme für O-Ton:** Nur wenn ein Statement zwingend für die Story nötig ist, darf es rein. Dann aber MIT Original-Audio (ohne `-an`) und das VO macht Pause.
- Für normales B-Roll (Standard):
```bash
# IMMER -an (Audio entfernen), IMMER -c:v libx264
ffmpeg -y -i source.mp4 -ss START -to ENDE -c:v libx264 -an -movflags +faststart assets/sceneN.mp4
```

### VO-Segmente
- Pro Szene ein VO-Segment
- MP3 Format
- Dauer passt zur Szene (oder kürzer, dann Pause am Ende)

### Musik
- IMMER den Standard-Track aus der Library (`shelter_to_the_valley.mp3`) verwenden. Keine dynamische Musik-Auswahl mehr.
- IMMER `data-volume="0.15"` (15%)
- Läuft durchgehend über die ganze Dauer

### Opener Overlay
- Das Overlay `OPENER_GLEICH.mov` wird immer über den Clip gelegt.
- Format: Muss für Hyperframes als transparentes WebM vorliegen (bereits konvertiert unter `assets/opener.webm`).

### Lint & Render
```bash
npx hyperframes lint        # Validierung
npx hyperframes render      # Lokaler Render
npx hyperframes publish     # Cloud Studio URL
```

## Recipes

### `news_overview_30s`
- ~30s, 4-6 Szenen, 16:9
- Arc: hook → context → key_fact → human_element → wrap
- Musik: 15%, subtle
- VO: Ein Key Fact pro Szene

### `on_air_promo`
- 30-45s, 5-8 Szenen, 16:9
- Arc: teaser → setup → tension → reveal → CTA
- Musik: 20-25%, energetisch
- VO: Dramatisch, fragenbasiert

### `social_clip_9x16`
- 15-25s, 3-5 Szenen, 9:16
- Arc: hook → moment → punchline → CTA
- Musik: 15%, upbeat
- VO: Minimal

## Model Strategy

| Model | Role |
|-------|------|
| **Gemini 3.1 Pro** | Overall context, frame analysis, story arc |
| **Gemma 4** (free) | Per-scene scoring, VO writing |
| **Hyperframes** | Composition, Timeline, Render |

## Musik Library

```
/workspace/video-kitchen-2.0/music_library/
├── shelter_to_the_valley.mp3   (epic/cinematic)
└── (mehr Tracks TBD)
```

## Workspace

```
/workspace/video-kitchen-2.1/
├── SKILL.md                    ← Dieses File
└── <projekt-name>/
    └── my-video/
        ├── source.html         ← Roh-Composition mit allen Clips
        ├── teaser-v1.html      ← Erster Teaser-Schnitt
        ├── teaser-v2.html      ← Iterationen
        ├── hyperframes.json    ← Config (referenziert alle HTMLs)
        ├── assets/
        │   ├── scene*.mp4      (video only, -an)
        │   ├── vo_*.mp3
        │   ├── opener.webm
        │   └── music.mp3
        └── output.mp4
```

## Cloud Studio

Nach jedem Build: `npx hyperframes publish --yes`
→ User bekommt URL mit claim_token zum Bearbeiten im Browser.
