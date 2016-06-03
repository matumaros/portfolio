

import ntpath

import yaml


class Settings:
    def __init__(self, paths=None, default_path=None):
        """Load, write and store settings

        This model manages setting files (YAML).

        Keyword Arguments:
            paths {list or None} -- list of full or relative
                                    paths with filenames (default: {None})
            default_path {str or None} -- path to user settings, read last
                                          and default for writing
                                          (default: {None})
        """
        self.paths = paths or []
        self.default_path = default_path
        self.buffer = {}
        # Clear up paths / validate
        self.rectify_paths()
        # Load files
        self.reload()

    def add_path(self, path, reload=True):
        """Add path and clean up

        Adds a path that is loaded and some other validation

        Arguments:
            path {str} -- path to file which is to be read

        Keyword Arguments:
            reload {bool} -- reload files into buffer (default: {True})
        """
        self.paths.append(path)
        self.rectify_paths()
        if reload:
            self.reload()

    def get(self, key=None, default=None):
        """Get value or settings

        Returns the value corresponding to key or all settings if None.

        Keyword Arguments:
            key {immutable} -- key name of setting (default: {None})
            default {ANY} -- value to return if nothing found
                                (default: {None})

        Returns:
            dict or ANY -- entire buffer or value corresponding to key
        """
        if key is None:
            return self.buffer
        else:
            return self.buffer.get(key, default)

    def rectify_paths(self):
        """Rectify / clean up / validate paths

        Makes sure that paths are sorted and
        default_path (if set) is loaded last.
        """
        # Make sure paths are unique and sorted by file name
        self.paths = sorted(set(self.paths), key=lambda p: ntpath.basename(p))
        # Remove default_path from paths (look at next comment)
        try:
            self.paths.remove(self.default_path)
        except ValueError:
            pass
        # Readd default_path at the end to make sure it's loaded last
        if self.default_path is not None:
            self.paths.append(self.default_path)

    def reload(self):
        """Reload files into buffer

        Reloads the files specified in self.paths
        and writes them into the buffer.
        """
        # Clear settings to ensure no unwanted leftovers
        self.buffer.clear()
        # Load every path (sorted by filename, self.default_path last)
        for path in self.paths:
            with open(path, 'r') as f:
                content = f.read()
            self.buffer.update(yaml.load(content) or {})

    def write(self, key, value, path=None):
        """Write into file

        Writes key and value into the file specified
        by path (or self.default_path if None)

        Arguments:
            key {immutable} -- key to use (valid YAML key)
            value {ANY} -- value to save

        Keyword Arguments:
            path {str} -- path to save file (default: {None})
        """
        path = path or self.default_path
        assert path is not None

        with open(path, 'r') as f:
            settings = yaml.load(f.read()) or {}

        settings[key] = value
        self.buffer[key] = value

        with open(path, 'w') as f:
            f.write(yaml.dump(settings, default_flow_style=False))


if __name__ == '__main__':
    settings = Settings(
        ['test.yml', 'test2.yml', 'custem.bu', 'test3.test'],
        'custem.bu',
    )
    settings.add_path('test4.yml')
    settings.write('new_key', 'testing')
    print(settings.get())
