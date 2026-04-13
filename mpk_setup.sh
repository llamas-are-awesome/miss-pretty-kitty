#!/bin/bash
# ================================================
# Miss Pretty Kitty - Setup Script
# ================================================

set -e

GREEN='\033[0;32m'
PINK='\033[1;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; exit 1; }
info() { echo -e "   $1"; }
header() { echo -e "\n${PINK}========================================${NC}\n${PINK} $1${NC}\n${PINK}========================================${NC}\n"; }

header "Miss Pretty Kitty Setup 🐱✨"
echo "Grab a snack, this takes 5-10 minutes nya~"
read -p "Press ENTER to start..."

header "Step 1: System Update"
sudo apt-get update -qq || err "No internet connection!"
ok "Updated!"

header "Step 2: System Dependencies"
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg \
    curl \
    git \
    || err "Failed to install packages"
ok "Dependencies installed!"

header "Step 3: Python Virtual Environment"
MPK_DIR="$HOME/miss-pretty-kitty"
cd "$MPK_DIR"
python3 -m venv venv
source venv/bin/activate
ok "Virtual environment ready!"

header "Step 4: Python Packages"
pip install --upgrade pip -q
pip install requests numpy || err "pip install failed"
ok "Python packages installed!"

header "Step 5: Ollama"
if command -v ollama &> /dev/null; then
    warn "Ollama already installed, skipping..."
else
    info "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh || err "Ollama install failed"
    ok "Ollama installed!"
fi

info "Starting Ollama..."
ollama serve &> /tmp/ollama.log &
sleep 5
ok "Ollama running!"

header "Step 6: Download Miss Pretty Kitty's Brain"
info "Pulling gemma3:1b (~800MB) — go make coffee ☕"
ollama pull gemma3:1b || err "Model download failed!"
ok "Brain downloaded!"

header "Step 7: Brain Test"
RESULT=$(python3 - <<'EOF'
import requests
try:
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": [{"role": "user", "content": "say nya~ and nothing else"}],
            "stream": False
        },
        timeout=60
    )
    print("PASS:", r.json()["message"]["content"])
except Exception as e:
    print("FAIL:", e)
EOF
)

echo "$RESULT"
if echo "$RESULT" | grep -q "PASS"; then
    ok "Brain test passed!! Miss Pretty Kitty is ALIVE!!"
else
    warn "Brain test failed — try running manually later"
fi

header "Step 8: Launch Script"
cat > "$MPK_DIR/start.sh" << 'LAUNCH'
#!/bin/bash
cd "$HOME/miss-pretty-kitty"
source venv/bin/activate
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "Starting Ollama..."
    ollama serve &> /tmp/ollama.log &
    sleep 3
fi
echo "🐱 Starting Miss Pretty Kitty..."
python3 mpk_main.py
LAUNCH

chmod +x "$MPK_DIR/start.sh"
ok "Launch script created!"

echo ""
echo -e "${PINK}✨ Setup complete!! nya~ 🐱💕${NC}"
echo ""
echo -e "To start Miss Pretty Kitty:"
echo -e "  ${GREEN}cd ~/miss-pretty-kitty && ./start.sh${NC}"
echo ""
read -p "Launch her RIGHT NOW? (y/n): " go
if [ "$go" = "y" ]; then
    cd "$MPK_DIR"
    source venv/bin/activate
    python3 mpk_main.py
fi
