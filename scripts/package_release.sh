#!/usr/bin/env bash
export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

VERSION=$(grep -o '"version": *"[^"]*"' wails.json | head -1 | cut -d'"' -f4)
if [ -n "$1" ]; then
    VERSION="$1"
fi

PKG_NAME="vaultlingo-v${VERSION}-linux-x86_64"
DIST_DIR="dist/${PKG_NAME}"

echo "=========================================="
echo "🚀 Building & Packaging VaultLingo v${VERSION}"
echo "=========================================="

echo "🔨 Building VaultLingo Desktop (Production)..."
wails build -clean -tags webkit2_41

echo "🔨 Building VaultLingo CLI (vl)..."
go build -ldflags="-s -w" -o build/bin/vl ./cmd/vl

echo "📦 [1/3] Creating Release Tarball (${PKG_NAME}.tar.gz)..."
rm -rf "$DIST_DIR" "dist/${PKG_NAME}.tar.gz"
mkdir -p "$DIST_DIR"

cp build/bin/VaultLingo "$DIST_DIR/vaultlingo"
cp build/bin/vl "$DIST_DIR/vl"
cp vaultlingo.desktop "$DIST_DIR/vaultlingo.desktop"
if [ -f "build/appicon.png" ]; then
    cp build/appicon.png "$DIST_DIR/vaultlingo.png"
elif [ -f "frontend/src/assets/images/pegasus-logo.png" ]; then
    cp frontend/src/assets/images/pegasus-logo.png "$DIST_DIR/vaultlingo.png"
fi
cp scripts/install.sh "$DIST_DIR/install.sh"
chmod +x "$DIST_DIR/install.sh" "$DIST_DIR/vaultlingo" "$DIST_DIR/vl"

cd dist
tar -czvf "${PKG_NAME}.tar.gz" "${PKG_NAME}"
cd ..

echo "📦 [2/3] Creating Debian Package (.deb)..."
chmod +x scripts/package_deb.sh
./scripts/package_deb.sh

echo "📦 [3/3] Updating AUR Packaging & .SRCINFO..."
chmod +x scripts/package_aur.sh
./scripts/package_aur.sh "${VERSION}"

echo ""
echo "=========================================="
echo "🎉 ALL PACKAGES CREATED SUCCESSFULLY!"
echo "=========================================="
echo "Artifacts in dist/:"
ls -lh dist/*.tar.gz dist/*.deb
echo "AUR directories ready in packaging/aur/:"
ls -la packaging/aur/vaultlingo-bin
ls -la packaging/aur/vaultlingo
echo "=========================================="
