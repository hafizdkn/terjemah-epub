from datetime import datetime
from pathlib import Path
import zipfile
import os

from utilities.clean_string import clean_string


class ExtractEpub:
    def __init__(self, src, dst, f_epub):
        self.src = src
        self.dst = dst
        self.path_oebps = None
        self.f_epub = f_epub

    def format_to_zip(self):
        epub_file = Path(self.src)
        self.src = epub_file.rename(epub_file.with_suffix(".zip"))

    def format_to_epub(self):
        epub_file = Path(self.src)
        self.src = epub_file.rename(epub_file.with_suffix(".epub"))

    def create_dst(self):
        if not os.path.exists(self.dst):
            os.makedirs(self.dst, exist_ok=True)
        else:
            folder_name = self.f_epub
            print(f"[XX] Folder sudah ada -> {folder_name}")
            print(f"[OK] Hapus folder -> {folder_name}")
            os.system(f"rm -rf {self.dst}")

    def move_min_js(self):
        path_src_min_js = Path().cwd() / "jquery.min.js"
        path_dst_min_js = Path(self.dst) / self.path_oebps
        os.system(f"cp '{path_src_min_js}' '{path_dst_min_js}'")

    def unzip(self):
        self.format_to_zip()
        folder_name = self.f_epub
        tgl = datetime.now().strftime("%d-%m-%Y")

        self.dst = Path(self.dst) / f"translated_{tgl}_{folder_name}"
        self.create_dst()

        with zipfile.ZipFile(self.src, "r") as zip_ref:
            zip_ref.extractall(self.dst)

    def extract_epub(self):
        print("[..] Ektrak epub...")
        self.unzip()
        self.format_to_epub()
        print("[OK] Ektrak epub success!")
        return self.dst
