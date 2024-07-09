class ConfigDetector:
    def __init__(self, directory):
        self.directory = directory

    def detect(self):
        config_files = []
        for file_path in self.directory.rglob("*"):
            if file_path.is_file() and (file_path.name.startswith('.') or file_path.name.lower() in ['config', 'secret']):
                config_files.append(file_path)
        return config_files