from pathlib import Path, PurePath
import sys
import os

from utilities.clean_string import clean_string
from utilities.read_config import ReadConfig
from src.extract_epub import ExtractEpub
from src.explore_file import ExploreFile
from src.go_translate import GoTranslate

config_path = "./config.ini"
abs_config_path = Path(config_path).absolute()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=====" * 5)
    config = ReadConfig(abs_config_path)

    if len(sys.argv) <= 1:
        exit("Masukkan file epub yang ingin di-run!")
    src = Path(sys.argv[1]).absolute()

    dst = config.get_value("Path", "dst")
    f_epub = "".join(PurePath(src).parts[-2:])
    f_epub = clean_string(f_epub)

    if not str(src).endswith(".epub"):
        return "File yang di-run harus berupa file epub!"

    print(f"[==] Output file         : {dst}")

    extract_epub = ExtractEpub(src, dst, f_epub)
    dst = extract_epub.extract_epub()

    explore_file = ExploreFile(dst)
    list_file, _ = explore_file.finding_file()
    path_oebps = explore_file.get_path_oebps()

    extract_epub.path_oebps = path_oebps
    extract_epub.move_min_js()

    print(f"[..] Terjemahkan Epub    : {f_epub}")

    try:
        translate = GoTranslate(list_file, abs_config_path)
    except (KeyboardInterrupt, Exception) as e:
        print(f"error {e}")
        print(f"[..] Hapus folder {dst}")
        os.system(f"rm -rf '{dst}'")
    else:
        translate.run()
        extract_epub.create_epub()
    print("=====" * 5)


if __name__ == "__main__":
    main()
