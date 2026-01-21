# Maintainer: Your Name <your.email@example.com>
pkgname=pass-gnome-gui
pkgver=1.0.0
pkgrel=1
pkgdesc="A GTK4 GUI for the pass password manager"
arch=('any')
url="https://github.com/yourusername/pass-gnome-gui"
license=('GPL3')
depends=('python' 'python-gobject' 'gtk4' 'libadwaita' 'pass')
source=('src/pass_gui.py'
        'src/application.py'
        'src/window.py'
        'src/password_store.py'
        'src/password_card.py'
        'pass-gnome-gui.desktop'
        'icon.png')
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    # Install Python modules to a package directory
    install -dm755 "$pkgdir/usr/lib/pass-gnome-gui"
    install -Dm644 "$srcdir/application.py" "$pkgdir/usr/lib/pass-gnome-gui/application.py"
    install -Dm644 "$srcdir/window.py" "$pkgdir/usr/lib/pass-gnome-gui/window.py"
    install -Dm644 "$srcdir/password_store.py" "$pkgdir/usr/lib/pass-gnome-gui/password_store.py"
    install -Dm644 "$srcdir/password_card.py" "$pkgdir/usr/lib/pass-gnome-gui/password_card.py"
    install -Dm755 "$srcdir/pass_gui.py" "$pkgdir/usr/lib/pass-gnome-gui/pass_gui.py"

    # Install launcher script
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/pass-gnome-gui" << 'EOF'
#!/bin/sh
exec python3 /usr/lib/pass-gnome-gui/pass_gui.py "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/pass-gnome-gui"

    # Install desktop entry
    install -Dm644 "$srcdir/pass-gnome-gui.desktop" "$pkgdir/usr/share/applications/pass-gnome-gui.desktop"

    # Install icon
    install -Dm644 "$srcdir/icon.png" "$pkgdir/usr/share/pixmaps/pass-gnome-gui.png"
}
