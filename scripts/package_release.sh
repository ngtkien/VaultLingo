#!/bin/bash
export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
set -e

VERSION="0.1.3"
PKG_NAME="vaultlingo-v${VERSION}-linux-x86_64"
DIST_DIR="dist/${PKG_NAME}"

echo "🔨 Building VaultLingo Desktop (Production)..."
wails build

echo "🔨 Building VaultLingo CLI (vl)..."
go build -ldflags="-s -w" -o build/bin/vl ./cmd/vl

echo "📦 Creating Release Package ${PKG_NAME}..."
rm -rf "$DIST_DIR" "dist/${PKG_NAME}.tar.gz"
mkdir -p "$DIST_DIR"

cp build/bin/VaultLingo "$DIST_DIR/vaultlingo"
cp build/bin/vl "$DIST_DIR/vl"
cp vaultlingo.desktop "$DIST_DIR/vaultlingo.desktop"
cp frontend/src/assets/images/pegasus-logo.png "$DIST_DIR/vaultlingo.png"
cp scripts/install.sh "$DIST_DIR/install.sh"
chmod +x "$DIST_DIR/install.sh" "$DIST_DIR/vaultlingo" "$DIST_DIR/vl"

cd dist
tar -czvf "${PKG_NAME}.tar.gz" "${PKG_NAME}"
cd ..

echo "🎉 Release package created successfully at: dist/${PKG_NAME}.tar.gz"
ls -lh "dist/${PKG_NAME}.tar.gz"
