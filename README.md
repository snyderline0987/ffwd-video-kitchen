# Video Kitchen in a Box 🎬📦

A fully local, collaborative video production agent powered by OpenClaw and Hyperframes. 
Designed for newsrooms, editorial teams, and creators who need fast, consistent, and automated video workflows without uploading gigabytes of raw footage to the cloud.

## 🌟 Core Concept

Die "Video Kitchen in a Box" ist ein eigenständiges Docker-Setup, das auf jedem PC, Mac Studio oder lokalen Server gestartet werden kann. 

### 1. 100% Local & Privacy First
Anstatt riesige Video-Dateien in die Cloud zu laden, mountet der Docker-Container einfach euer lokales Netzlaufwerk oder eure externe SSD (z.B. `/Volumes/RawFootage`). Der KI-Agent (OpenClaw) arbeitet direkt auf dem Material. Eure Daten verlassen niemals das Haus.

### 2. Multi-User Redaktion (LAN / Tailscale)
Das System stellt ein **Web-Dashboard (Port 8080)** und das **Agent-Interface (Port 3000)** im lokalen Netzwerk bereit.
- Im Büro: Redakteure greifen über die lokale IP-Adresse zu (z.B. `http://192.168.1.100:8080`).
- Remote: Durch die native Tailscale-Integration von OpenClaw können Mitarbeiter von zu Hause sicher im VPN auf den Agenten zugreifen. Keine unsicheren Serveo-Tunnel mehr!

### 3. "Video as a Service" via Discord (Optional)
Der Agent kann mit einem Discord-Bot-Token gestartet werden. Das Redaktionsteam zieht Material einfach in den Discord-Kanal und taggt den Agenten: *"@openclaw mach aus diesem Interview einen 30s Social Clip"*.

### 4. Hardware-Accelerated Rendering
Da das System lokal läuft, kann es die volle Power eurer GPU (Apple Silicon, NVIDIA) nutzen, um die Hyperframes-Compositions in rasender Geschwindigkeit in echtes MP4 zu rendern (`npx hyperframes render`). Das externe Cloud Studio wird für komplexe Renderings nicht mehr zwingend benötigt.

---

## 🛠️ Repository Structure

Dieses Repository enthält die "Skills", die OpenClaw beibringen, wie man Videos schneidet und wie das Dashboard funktioniert:
- `skills/video-kitchen/` - Der Kern-Skill zum Generieren der Hyperframes-Videos.
- `skills/video-kitchen-recipe-creator/` - Der Skill zum Betreiben des lokalen Rezept-Dashboards.
- `skills/film-editing-theory/` - Ein Theoriesatz, den der Agent als Regelwerk beim Schneiden nutzt (Dmytryk, Menke, etc.).
- `skills/hyperframes/` - Die Kern-Engine für HTML/CSS basierte Video-Compositions.
- `skills/open-design/` - Integration von nexu-io/open-design zur Generierung von UI- und Grafik-Overlays direkt aus Design-Files.
- `docker-compose.yml` - Das Rezept, um die ganze "Box" mit einem Klick zu starten.

## 🚀 Quick Start (Deploying the Agent)

1. **Repository klonen:**
   ```bash
   git clone https://github.com/snyderline0987/video-kitchen-box.git
   cd video-kitchen-box
   ```

2. **Umgebungsvariablen anlegen (.env):**
   Erstelle eine `.env` Datei mit den API-Keys für das Vision-Model (Gemini/OpenAI) und optional Discord.

3. **Docker Compose starten:**
   ```bash
   docker-compose up -d
   ```

4. **Loslegen:**
   - Agent Chat: `http://localhost:3000`
   - Recipe Dashboard: `http://localhost:8080`
