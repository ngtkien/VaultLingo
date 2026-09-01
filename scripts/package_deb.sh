#!/usr/bin/env bash
set -e

# Change directory to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

VERSION=$(grep -o '"version": *"[^"]*"' wails.json | head -1 | cut -d'"' -f4)
if [ -z "$VERSION" ]; then
    VERSION="0.3.0"
fi

ARCH="amd64"
PKG_NAME="vaultlingo"
DEB_NAME="${PKG_NAME}_${VERSION}_${ARCH}.deb"
DIST_DIR="${ROOT_DIR}/dist"
STAGE_DIR="${DIST_DIR}/deb-staging"

echo "=========================================="
echo "📦 Packaging Debian package (.deb)"
echo "   App:      ${PKG_NAME}"
echo "   Version:  ${VERSION}"
echo "   Arch:     ${ARCH}"
echo "=========================================="

# Build binaries if missing
if [ ! -f "build/bin/VaultLingo" ] || [ ! -f "build/bin/vl" ]; then
    echo "🔨 Binaries not found, compiling..."
    export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
    wails build
    go build -ldflags="-s -w" -o build/bin/vl ./cmd/vl
fi

# Clean stage directory
rm -rf "${STAGE_DIR}"
mkdir -p "${STAGE_DIR}/DEBIAN"
mkdir -p "${STAGE_DIR}/usr/bin"
mkdir -p "${STAGE_DIR}/usr/share/applications"
mkdir -p "${STAGE_DIR}/usr/share/icons/hicolor/512x512/apps"
mkdir -p "${STAGE_DIR}/usr/share/doc/${PKG_NAME}"

# Copy Binaries
cp "build/bin/VaultLingo" "${STAGE_DIR}/usr/bin/vaultlingo"
cp "build/bin/vl" "${STAGE_DIR}/usr/bin/vl"
chmod 755 "${STAGE_DIR}/usr/bin/vaultlingo"
chmod 755 "${STAGE_DIR}/usr/bin/vl"

# Copy Desktop Entry and Icon
cp "vaultlingo.desktop" "${STAGE_DIR}/usr/share/applications/vaultlingo.desktop"
chmod 644 "${STAGE_DIR}/usr/share/applications/vaultlingo.desktop"

if [ -f "build/appicon.png" ]; then
    cp "build/appicon.png" "${STAGE_DIR}/usr/share/icons/hicolor/512x512/apps/vaultlingo.png"
elif [ -f "frontend/src/assets/images/pegasus-logo.png" ]; then
    cp "frontend/src/assets/images/pegasus-logo.png" "${STAGE_DIR}/usr/share/icons/hicolor/512x512/apps/vaultlingo.png"
fi
chmod 644 "${STAGE_DIR}/usr/share/icons/hicolor/512x512/apps/vaultlingo.png"

# Copy copyright / doc if exists
if [ -f "README.md" ]; then
    cp "README.md" "${STAGE_DIR}/usr/share/doc/${PKG_NAME}/"
fi

# Calculate installed size in KB
INSTALLED_SIZE=$(du -sk "${STAGE_DIR}/usr" | cut -f1)

# Generate DEBIAN/control
cat <<EOF > "${STAGE_DIR}/DEBIAN/control"
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Essential: no
Installed-Size: ${INSTALLED_SIZE}
Maintainer: Zeder <ngtkien95@gmail.com>
Homepage: https://github.com/ngtkien/VaultLingo
Depends: libgtk-3-0, libwebkit2gtk-4.1-0 | libwebkit2gtk-4.0-37, libc6 (>= 2.31)
Description: Daily AI English & Obsidian Vault Sync
 VaultLingo is a modern English learning desktop application and CLI tool
 that syncs vocabulary, grammar drills, and dictations directly with your
 local Obsidian markdown vault.
EOF

# Generate DEBIAN/postinst
cat <<'EOF' > "${STAGE_DIR}/DEBIAN/postinst"
#!/bin/sh
set -e

if [ "$1" = "configure" ]; then
    if which gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true
    fi
    if which update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q /usr/share/applications >/dev/null 2>&1 || true
    fi
fi
exit 0
EOF
chmod 755 "${STAGE_DIR}/DEBIAN/postinst"

# Generate DEBIAN/postrm
cat <<'EOF' > "${STAGE_DIR}/DEBIAN/postrm"
#!/bin/sh
set -e

if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    if which gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor >/dev/null 2>&1 || true
    fi
    if which update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q /usr/share/applications >/dev/null 2>&1 || true
    fi
fi
exit 0
EOF
chmod 755 "${STAGE_DIR}/DEBIAN/postrm"

# Generate DEBIAN/md5sums
(
    cd "${STAGE_DIR}"
    find usr -type f -exec md5sum {} + > DEBIAN/md5sums
)
chmod 644 "${STAGE_DIR}/DEBIAN/md5sums"

mkdir -p "${DIST_DIR}"
OUTPUT_DEB="${DIST_DIR}/${DEB_NAME}"
rm -f "${OUTPUT_DEB}"

# Build debian package (using dpkg-deb if available, otherwise native ar + tar)
if command -v dpkg-deb >/dev/null 2>&1; then
    echo "⚙️  Building deb with dpkg-deb..."
    dpkg-deb --build --root-owner-group "${STAGE_DIR}" "${OUTPUT_DEB}"
else
    echo "⚙️  Building deb with native ar and tar..."
    TEMP_BUILD="${DIST_DIR}/deb-temp"
    rm -rf "${TEMP_BUILD}"
    mkdir -p "${TEMP_BUILD}"

    echo "2.0" > "${TEMP_BUILD}/debian-binary"

    # Create control.tar.gz
    (
        cd "${STAGE_DIR}/DEBIAN"
        tar --owner=0 --group=0 -czf "${TEMP_BUILD}/control.tar.gz" .
    )

    # Create data.tar.gz
    (
        cd "${STAGE_DIR}"
        tar --owner=0 --group=0 --exclude="./DEBIAN" -czf "${TEMP_BUILD}/data.tar.gz" ./usr
    )

    # Pack into .deb archive using ar
    (
        cd "${TEMP_BUILD}"
        ar -rc "${OUTPUT_DEB}" debian-binary control.tar.gz data.tar.gz
    )
    rm -rf "${TEMP_BUILD}"
fi

# Clean stage dir
rm -rf "${STAGE_DIR}"

echo "=========================================="
echo "🎉 Debian package created successfully!"
echo "   Path: ${OUTPUT_DEB}"
ls -lh "${OUTPUT_DEB}"
echo "=========================================="
