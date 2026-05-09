# Open Design Integration for Hyperframes

## Description
Integrates `https://github.com/nexu-io/open-design` into the Video Kitchen and Hyperframes workflow. 
Open Design is used to parse, transform, and render UI designs and graphic mockups directly into Hyperframes-compatible HTML/CSS/SVG compositions.

## Usage
When a user asks to convert a UI or graphic layout into a video composition:
1. Fetch or parse the Open Design graphic definitions.
2. Translate the Open Design structural properties into deterministic Hyperframes HTML/CSS elements.
3. Apply standard Hyperframes CSS animations (or GSAP) to the translated elements to bring the design to life.
4. Save the generated layout into the respective `video-kitchen` recipe's blueprint (e.g., as `template.html` or an overlay module).

## Principles
- **No external heavy dependencies:** Render Open Design shapes via native HTML/CSS/SVG inside the Hyperframes DOM.
- **Determinism:** Ensure any auto-layout or responsive behavior from Open Design is locked to the exact 16:9 or 9:16 aspect ratio defined in the Video Kitchen recipe.

## Examples & Code Snippets
The `examples/` directory contains a fully functional prototype of translating an Open Design JSON (`mock-octopus.json`) into a deterministic Hyperframes Component (`lower-third.html`) using a Node.js parsing script (`parse.js`). 
This logic is used by the agent to automatically convert CI elements (like lower thirds) from design files directly into the Video Kitchen recipes.
