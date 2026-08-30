#!/bin/bash
set -e

echo "🚀 Installing VaultLingo Desktop & CLI..."

INSTALL_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/512x512/apps"

# Install GUI Binary
if [ -f "VaultLingo" ]; then
  sudo cp VaultLingo "$INSTALL_DIR/vaultlingo"
  sudo chmod +x "$INSTALL_DIR/vaultlingo"
  echo "✔ Installed GUI to $INSTALL_DIR/vaultlingo"
elif [ -f "vaultlingo" ]; then
  sudo cp vaultlingo "$INSTALL_DIR/vaultlingo"
  sudo chmod +x "$INSTALL_DIR/vaultlingo"
  echo "✔ Installed GUI to $INSTALL_DIR/vaultlingo"
fi

# Install CLI Binary
if [ -f "vl" ]; then
  sudo cp vl "$INSTALL_DIR/vl"
  sudo chmod +x "$INSTALL_DIR/vl"
  echo "✔ Installed CLI to $INSTALL_DIR/vl"
fi

# Install Desktop Entry & Icon
if [ -f "vaultlingo.desktop" ]; then
  sudo mkdir -p "$DESKTOP_DIR"
  sudo cp vaultlingo.desktop "$DESKTOP_DIR/"
  echo "✔ Registered application launcher: $DESKTOP_DIR/vaultlingo.desktop"
fi

if [ -f "vaultlingo.png" ]; then
  sudo mkdir -p "$ICON_DIR"
  sudo cp vaultlingo.png "$ICON_DIR/"
  sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true
  echo "✔ Installed app icon to $ICON_DIR/vaultlingo.png"
fi

echo "🎉 VaultLingo installed successfully! Type 'vl <word>' or launch 'VaultLingo' from your app menu."
