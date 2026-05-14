FROM node:22-slim

# System deps for video processing
RUN apt-get update && apt-get install -y \
    python3 \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw
RUN npm install -g openclaw

# App directory
WORKDIR /app

# Copy recipe dashboard + server
COPY skills/video-kitchen/recipes/package*.json ./recipes/
RUN cd recipes && npm install --production

COPY skills/video-kitchen/recipes/ ./recipes/

# Copy skills into OpenClaw skill directory
RUN mkdir -p /usr/local/lib/node_modules/openclaw/skills
COPY skills/video-kitchen/ /usr/local/lib/node_modules/openclaw/skills/video-kitchen/
COPY skills/video-kitchen-recipe-creator/ /usr/local/lib/node_modules/openclaw/skills/video-kitchen-recipe-creator/
COPY skills/film-editing-theory/ /usr/local/lib/node_modules/openclaw/skills/film-editing-theory/
COPY skills/hyperframes/ /usr/local/lib/node_modules/openclaw/skills/hyperframes/
COPY skills/open-design/ /usr/local/lib/node_modules/openclaw/skills/open-design/

# Copy workspace defaults
COPY workspace/ /workspace/
COPY dashboard.html /app/dashboard.html

# Ports: OpenClaw agent (3000), Dashboard (8080), Hyperframes preview (3002)
EXPOSE 3000 8080 3002

# Start dashboard server + OpenClaw agent
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
