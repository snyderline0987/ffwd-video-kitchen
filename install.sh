#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Video Kitchen Box — Installer
#  Choose your agent backend and get cooking.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
set -e

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

REPO="https://github.com/snyderline0987/video-kitchen-box.git"
AGENT=""

# ─── Helpers ──────────────────────────────────────────────────

info()  { echo -e "${CYAN}  ℹ${NC} $1"; }
ok()    { echo -e "${GREEN}  ✓${NC} $1"; }
warn()  { echo -e "${YELLOW}  ⚠${NC} $1"; }
die()   { echo -e "${RED}  ✗${NC} $1"; exit 1; }

banner() {
  echo ""
  echo -e "${BOLD}  🍳 Video Kitchen Box — Installer${NC}"
  echo -e "  ${DIM}Agent-driven video production pipeline${NC}"
  echo ""
  echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
}

# ─── Check Dependencies ──────────────────────────────────────

check_deps() {
  info "Checking dependencies..."
  
  command -v docker >/dev/null 2>&1 || die "Docker is required. Install: https://docs.docker.com/get-docker/"
  command -v git >/dev/null 2>&1 || die "git is required."
  
  if ! docker info >/dev/null 2>&1; then
    die "Docker daemon is not running. Start it first."
  fi
  
  ok "Docker + git available"
}

# ─── Agent Selection ─────────────────────────────────────────

choose_agent() {
  echo -e "  ${BOLD}Choose your agent backend:${NC}"
  echo ""
  echo -e "  ${GREEN}1)${NC} ${BOLD}OpenClaw${NC}    — Full-featured AI agent (Telegram/Discord/Signal)"
  echo -e "              ${DIM}Best for: production use, chat-driven video editing${NC}"
  echo ""
  echo -e "  ${GREEN}2)${NC} ${BOLD}Agent0${NC}      — Open-source autonomous agent framework"
  echo -e "              ${DIM}Best for: headless automation, custom pipelines${NC}"
  echo ""
  echo -e "  ${GREEN}3)${NC} ${BOLD}Hermes${NC}      — Multi-model agent orchestration"
  echo -e "              ${DIM}Best for: multi-model workflows, API-driven setups${NC}"
  echo ""
  
  while true; do
    read -rp "  Enter choice [1/2/3]: " choice < /dev/tty
    case $choice in
      1) AGENT="openclaw"; break;;
      2) AGENT="agent0"; break;;
      3) AGENT="hermes"; break;;
      *) echo -e "  ${RED}Please enter 1, 2, or 3${NC}";;
    esac
  done
  
  echo ""
  echo -e "  ${BOLD}Selected: ${AGENT}${NC}"
  echo ""
}

# ─── Clone Repo ──────────────────────────────────────────────

clone_repo() {
  local target="$1"
  
  if [ -d "$target" ] && [ -d "$target/.git" ]; then
    info "Existing repo found at $target — pulling latest..."
    cd "$target"
    git pull --rebase 2>/dev/null || warn "git pull failed, continuing with local version"
    cd - >/dev/null
  else
    info "Cloning Video Kitchen Box..."
    git clone "$REPO" "$target"
    ok "Cloned to $target"
  fi
}

# ─── Configure .env ──────────────────────────────────────────

setup_env() {
  local target="$1"
  
  if [ -f "$target/.env" ]; then
    info ".env already exists — leaving it untouched"
    return
  fi
  
  info "Creating .env from template..."
  cat > "$target/.env" << 'ENVEOF'
# ─── API Keys ───
GEMINI_API_KEY=
OPENAI_API_KEY=
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=

# ─── Chat Integration (OpenClaw only) ───
TELEGRAM_BOT_TOKEN=
DISCORD_TOKEN=
SIGNAL_PHONE=

# ─── Footage Mount ───
# Point this to your raw footage directory on the host
RAW_FOOTAGE_PATH=./raw_footage

# ─── Remote Access (optional) ───
TS_AUTHKEY=
ENVEOF
  
  ok ".env created — edit it to add your API keys"
  echo ""
  echo -e "  ${YELLOW}  → Edit $target/.env and add your API keys${NC}"
  echo ""
}

# ─── Setup Docker Compose ────────────────────────────────────

setup_compose() {
  local target="$1"
  local compose_src="$target/docker/docker-compose.${AGENT}.yml"
  local compose_dst="$target/docker-compose.yml"
  
  if [ ! -f "$compose_src" ]; then
    die "docker-compose.${AGENT}.yml not found in docker/"
  fi
  
  cp "$compose_src" "$compose_dst"
  ok "docker-compose.yml → ${AGENT} variant"
}

# ─── Build & Start ───────────────────────────────────────────

build_and_start() {
  local target="$1"
  cd "$target"
  
  info "Building containers..."
  docker compose build 2>&1 | tail -3
  
  info "Starting Video Kitchen..."
  docker compose up -d 2>&1 | tail -3
  
  ok "Containers started"
}

# ─── Print Success ───────────────────────────────────────────

print_success() {
  local target="$1"
  
  echo ""
  echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo -e "  ${BOLD}${GREEN}✓ Video Kitchen is running!${NC}"
  echo ""
  echo -e "  ${BOLD}Dashboard:${NC}  http://localhost:8080/dashboard.html"
  echo -e "  ${BOLD}Preview:${NC}    http://localhost:3002"
  
  case "$AGENT" in
    openclaw)
      echo -e "  ${BOLD}Agent:${NC}     http://localhost:3000"
      echo ""
      echo -e "  ${DIM}Send a video to your OpenClaw bot on Telegram/Discord${NC}"
      ;;
    agent0)
      echo -e "  ${BOLD}Agent:${NC}     Agent0 (headless)"
      echo ""
      echo -e "  ${DIM}Configure Agent0 to use /skills/ and /workspace/${NC}"
      ;;
    hermes)
      echo -e "  ${BOLD}Agent:${NC}     http://localhost:4000"
      echo ""
      echo -e "  ${DIM}Configure Hermes via /workspace/hermes.yaml${NC}"
      ;;
  esac
  
  echo ""
  echo -e "  ${DIM}Logs: docker compose logs -f${NC}"
  echo -e "  ${DIM}Stop:  docker compose down${NC}"
  echo -e "  ${DIM}Config: ${target}/.env${NC}"
  echo ""
}

# ─── Main ─────────────────────────────────────────────────────

main() {
  banner
  check_deps
  choose_agent
  
  TARGET_DIR="${2:-./video-kitchen-box}"
  
  clone_repo "$TARGET_DIR"
  setup_env "$TARGET_DIR"
  setup_compose "$TARGET_DIR"
  build_and_start "$TARGET_DIR"
  print_success "$TARGET_DIR"
}

main "$@"
