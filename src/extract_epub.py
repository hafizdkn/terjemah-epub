from datetime import datetime
from pathlib import Path
import zipfile
import shutil
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
            print(f"[XX] Folder sudah ada    : {folder_name}")
            print(f"[OK] Hapus folder        : {folder_name}")
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

    def remove(self):
        r = lambda x: shutil.rmtree(x) if Path(x).is_dir() else os.remove(x)
        f = [r(f) for f in Path(self.dst).iterdir() if not str(f).endswith(".epub")]
        print("[..] Hapus folder success : OK")

    def create_epub(self):
        print("[..] Proses membuat epub  : OK")
        cur_path = self.dst
        zip_file = str(cur_path / self.f_epub)
        shutil.make_archive(zip_file, "zip", cur_path)
        os.rename(f"{zip_file}.zip", f"{zip_file}.epub")
        print("[OK] Membuat epub success : OK")
        self.remove()

    def extract_epub(self):
        print("[..] Ektrak epub         : OK")
        self.unzip()
        self.format_to_epub()
        print("[..] Ektrak epub success : OK")
        return self.dst
