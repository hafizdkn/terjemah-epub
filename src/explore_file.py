from pathlib import Path
import os


class ExploreFile:
    def __init__(self, dst):
        self.dst = dst
        self.path_oebps = None

    def finding_file(self):
        target_format = [".html", "xhtml"]
        target_file = ["nav"]

        list_file = []
        root_path = ""
        for root, dirs, files in os.walk(self.dst):
            for file in files:
                for target in target_format:
                    if file.endswith(target) and file.split(".")[0] not in target_file:
                        list_file.append(f"{root}/{file}")
                        root_path = root

        self.path_oebps = root_path
        return list_file, root_path

    def get_path_oebps(self):
        return self.path_oebps
