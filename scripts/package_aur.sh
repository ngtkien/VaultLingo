#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

VERSION=$(grep -o '"version": *"[^"]*"' wails.json | head -1 | cut -d'"' -f4)
if [ -n "$1" ]; then
    VERSION="$1"
fi

PKG_TAR="dist/vaultlingo-v${VERSION}-linux-x86_64.tar.gz"

echo "=========================================="
echo "📦 Updating AUR Packages for VaultLingo v${VERSION}"
echo "=========================================="

# 1. Update vaultlingo-bin
BIN_DIR="${ROOT_DIR}/packaging/aur/vaultlingo-bin"
if [ -f "$PKG_TAR" ]; then
    SHA256=$(sha256sum "$PKG_TAR" | cut -d' ' -f1)
    echo "✔ Release tarball found: $PKG_TAR (SHA256: ${SHA256:0:16}...)"
else
    echo "⚠️  Release tarball $PKG_TAR not found yet, will use 'SKIP' for sha256."
    SHA256="SKIP"
fi

sed -i "s/^pkgver=.*/pkgver=${VERSION}/" "${BIN_DIR}/PKGBUILD"
if [ "$SHA256" != "SKIP" ]; then
    sed -i "s/^sha256sums_x86_64=(.*/sha256sums_x86_64=('${SHA256}')/" "${BIN_DIR}/PKGBUILD"
fi

(
    cd "${BIN_DIR}"
    if command -v makepkg >/dev/null 2>&1; then
        makepkg --printsrcinfo > .SRCINFO
        echo "✔ Generated ${BIN_DIR}/.SRCINFO"
    fi
)

# 2. Update vaultlingo (source)
SRC_DIR="${ROOT_DIR}/packaging/aur/vaultlingo"
sed -i "s/^pkgver=.*/pkgver=${VERSION}/" "${SRC_DIR}/PKGBUILD"

(
    cd "${SRC_DIR}"
    if command -v makepkg >/dev/null 2>&1; then
        makepkg --printsrcinfo > .SRCINFO
        echo "✔ Generated ${SRC_DIR}/.SRCINFO"
    fi
)

echo "=========================================="
echo "🎉 AUR packages updated successfully!"
echo "=========================================="
