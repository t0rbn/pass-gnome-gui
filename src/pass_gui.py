#!/usr/bin/env python3
"""
pass-gnome-gui: A GTK4 GUI for the pass password manager.
"""

from application import PassGnomeApp


def main():
    app = PassGnomeApp()
    return app.run(None)


if __name__ == '__main__':
    main()
