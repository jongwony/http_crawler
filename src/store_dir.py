import os

from virtualenv import PathEnv


class ProjectDir:
    def __init__(self, working_dir):
        self.name = working_dir

        if not os.path.isdir(self.data_dir()):
            os.makedirs(self.data_dir())

        if not os.path.isdir(self.log_dir()):
            os.makedirs(self.log_dir())

    def data_dir(self):
        return os.path.join(PathEnv.SCRIPT_DIR, 'data', self.name)

    def log_dir(self):
        return os.path.join(PathEnv.SCRIPT_DIR, 'log', self.name)
