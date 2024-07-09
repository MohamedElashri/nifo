from pathlib import Path
import os
import pathspec
import mimetypes

class FileScanner:
    IGNORED_FILES = {
        'LICENSE', 'LICENSE.txt', 'LICENSE.md',
        'README', 'README.txt', 'README.md',
        'CHANGELOG', 'CHANGELOG.txt', 'CHANGELOG.md',
        'CONTRIBUTING', 'CONTRIBUTING.md',
        'CODE_OF_CONDUCT', 'CODE_OF_CONDUCT.md',
        '.gitignore', '.editorconfig', '.travis.yml', '.gitlab-ci.yml',
        'package.json', 'package-lock.json', 'yarn.lock',
        'Gemfile', 'Gemfile.lock', 'requirements.txt',
        'Pipfile', 'Pipfile.lock',
        'Makefile', 'CMakeLists.txt',
        'Dockerfile', 'docker-compose.yml',
    }

    IGNORED_DIRS = {
        '.git', 'docs', 'doc', 'build', 'dist', 'out',
        'node_modules', 'vendor'
    }

    def __init__(self, directory, include_hidden=False, count_binary=False):
        self.directory = Path(directory)
        self.include_hidden = include_hidden
        self.count_binary = count_binary
        self.gitignore_spec = self.load_gitignore()
        self.binary_count = 0
        self.image_count = 0


    def load_gitignore(self):
        gitignore_file = self.directory / '.gitignore'
        if gitignore_file.exists():
            with gitignore_file.open() as f:
                return pathspec.PathSpec.from_lines('gitwildmatch', f)
        return None
    
    def is_ignored(self, path):
        relative_path = path.relative_to(self.directory)
        
        # Check if any part of the path is in IGNORED_DIRS
        if any(part in self.IGNORED_DIRS for part in relative_path.parts):
            return True
        
        # Check if the file name is in IGNORED_FILES
        if path.is_file() and path.name in self.IGNORED_FILES:
            return True
        
        if self.gitignore_spec:
            return self.gitignore_spec.match_file(str(relative_path))
        return False


    def is_binary_or_image(self, file_path):
        mime, _ = mimetypes.guess_type(file_path)
        
        if mime:
            if mime.startswith('image/'):
                self.image_count += 1
                return True
            elif not mime.startswith('text/'):
                self.binary_count += 1
                return True
        
        # Check for shell scripts that might be misidentified
        try:
            with open(file_path, 'r') as f:
                first_line = f.readline()
                if first_line.startswith('#!'):
                    return False
        except UnicodeDecodeError:
            # If we can't read it as text, it's probably binary
            self.binary_count += 1
            return True
        
        return False

    def scan(self):
        files = []
        for root, dirs, filenames in os.walk(self.directory):
            root_path = Path(root)

            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRS and 
                       not self.is_ignored(root_path / d) and 
                       (self.include_hidden or not d.startswith('.'))]

            for filename in filenames:
                file_path = root_path / filename
                if (self.include_hidden or not filename.startswith('.')) and not self.is_ignored(file_path):
                    if not self.is_binary_or_image(file_path) or self.count_binary:
                        files.append(file_path)

        return files