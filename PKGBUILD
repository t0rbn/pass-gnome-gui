# Maintainer: Your Name <your.email@example.com>
pkgname=pass-gnome-gui
pkgver=1.0.1
pkgrel=1
pkgdesc="A GTK4 GUI for the pass password manager"
arch=('any')
url="https://github.com/t0rbn/pass-gnome-gui"
license=('WTFPL')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'pass' 'wl-clipboard')

package() {
    cd "$startdir"

    # Install Python modules to a package directory
    install -dm755 "$pkgdir/usr/lib/pass-gnome-gui"
    install -Dm644 src/application.py "$pkgdir/usr/lib/pass-gnome-gui/application.py"
    install -Dm644 src/window.py "$pkgdir/usr/lib/pass-gnome-gui/window.py"
    install -Dm644 src/password_store.py "$pkgdir/usr/lib/pass-gnome-gui/password_store.py"
    install -Dm644 src/password_card.py "$pkgdir/usr/lib/pass-gnome-gui/password_card.py"
    install -Dm755 src/pass_gui.py "$pkgdir/usr/lib/pass-gnome-gui/pass_gui.py"

    # Install launcher script
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/pass-gtk" << 'EOF'
#!/bin/sh
exec python3 /usr/lib/pass-gnome-gui/pass_gui.py "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/pass-gtk"

    # Install desktop entry
    install -Dm644 pass-gnome-gui.desktop "$pkgdir/usr/share/applications/pass-gnome-gui.desktop"

    # Install icon
    install -Dm644 icon.png "$pkgdir/usr/share/pixmaps/pass-gnome-gui.png"
}
