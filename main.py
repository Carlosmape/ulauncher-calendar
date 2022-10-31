import gi
gi.require_version('Gdk', '3.0')

from extension.AlmanacExtension import AlmanacExtension


if __name__ == '__main__':
    AlmanacExtension().run()
