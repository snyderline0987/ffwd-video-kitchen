#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Video Kitchen Box — Installer
#  Usage: bash install.sh [openclaw|agent0|hermes]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
set -euo pipefail

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

REPO="https://github.com/snyderline0987/video-kitchen-box.git"
VALID_AGENTS="openclaw agent0 hermes"

info()  { echo -e "${CYAN}  ℹ${NC} $1"; }
ok()    { echo -e "${GREEN}  ✓${NC} $1"; }
warn()  { echo -e "${YELLOW}  ⚠${NC} $1"; }
die()   { echo -e "${RED}  ✗${NC} $1"; exit 1; }

echo ""
echo -e "${BOLD}  🍳 Video Kitchen Box — Installer${NC}"
echo -e "  ${DIM}Agent-driven video production pipeline${NC}"
echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─── Parse Agent ──────────────────────────────────────────────

AGENT="${1:-}"

if [ -z "$AGENT" ]; then
  echo -e "  ${RED}Usage: bash install.sh [openclaw|agent0|hermes]${NC}"
  echo ""
  echo -e "  ${GREEN}openclaw${NC}  — Full-featured AI agent (Telegram/Discord/Signal)"
  echo -e "             ${DIM}Best for: production use, chat-driven video editing${NC}"
  echo ""
  echo -e "  ${GREEN}agent0${NC}    — Open-source autonomous agent framework"
  echo -e "             ${DIM}Best for: headless automation, custom pipelines${NC}"
  echo ""
  echo -e "  ${GREEN}hermes${NC}    — Multi-model agent orchestration"
  echo -e "             ${DIM}Best for: multi-model workflows, API-driven setups${NC}"
  echo ""
  echo -e "  ${DIM}Example: curl -sL .../install.sh | bash -s -- openclaw${NC}"
  echo ""
  exit 1
fi

# Validate
FOUND=0
for a in $VALID_AGENTS; do
  [ "$a" = "$AGENT" ] && FOUND=1
done
[ "$FOUND" = "0" ] && die "Unknown agent '$AGENT'. Choose: openclaw, agent0, hermes"

echo -e "  ${BOLD}Agent: ${AGENT}${NC}"
echo ""

# ─── Check Dependencies ──────────────────────────────────────

info "Checking dependencies..."
command -v docker >/dev/null 2>&1 || die "Docker is required. https://docs.docker.com/get-docker/"
command -v git >/dev/null 2>&1 || die "git is required."
docker info >/dev/null 2>&1 || die "Docker daemon not running. Start it first."
ok "Docker + git"

# ─── Clone / Update ──────────────────────────────────────────

TARGET="./video-kitchen-box"

if [ -d "$TARGET" ] && [ -d "$TARGET/.git" ]; then
  info "Updating existing repo..."
  cd "$TARGET" && git pull --rebase 2>/dev/null && cd - >/dev/null
  ok "Repo updated"
else
  info "Cloning..."
  git clone "$REPO" "$TARGET"
  ok "Cloned to $TARGET"
fi

# ─── Setup Docker Compose ────────────────────────────────────

COMPOSE_SRC="$TARGET/docker/docker-compose.${AGENT}.yml"
COMPOSE_DST="$TARGET/docker-compose.yml"

[ -f "$COMPOSE_SRC" ] || die "docker-compose.${AGENT}.yml not found"
cp "$COMPOSE_SRC" "$COMPOSE_DST"
ok "docker-compose.yml → ${AGENT}"

# ─── Configure .env ──────────────────────────────────────────

if [ -f "$TARGET/.env" ]; then
  info ".env exists — skipping"
else
  cp "$TARGET/.env.example" "$TARGET/.env"
  ok ".env created — edit it to add API keys"
fi

# ─── Build & Start ───────────────────────────────────────────

cd "$TARGET"

info "Building containers..."
docker compose build 2>&1 | tail -3

info "Starting Video Kitchen..."
docker compose up -d 2>&1 | tail -3

ok "Containers started"

# ─── Success ─────────────────────────────────────────────────

echo ""
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "  ${BOLD}${GREEN}✓ Video Kitchen is running!${NC}"
echo ""
echo -e "  ${BOLD}Dashboard:${NC}  http://localhost:8080/dashboard.html"

case "$AGENT" in
  openclaw) echo -e "  ${BOLD}Agent:${NC}     http://localhost:3000" ;;
  agent0)   echo -e "  ${BOLD}Agent:${NC}     Agent0 (headless)" ;;
  hermes)   echo -e "  ${BOLD}Agent:${NC}     http://localhost:4000" ;;
esac

echo ""
echo -e "  ${DIM}Logs:   docker compose logs -f${NC}"
echo -e "  ${DIM}Stop:   docker compose down${NC}"
echo -e "  ${DIM}Config: $TARGET/.env${NC}"
echo ""
