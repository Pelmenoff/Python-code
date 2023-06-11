import sys, os, shutil 
from pathlib import Path
from normalize import normalize


CATEGORIES = {"Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".mp4", ".mov", ".avi", ".mkv"],
              "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
              "Audio": [".mp3", ".aiff", ".ogg", ".wav", ".amr"],
              "Archives": [".zip", ".tar", ".gz"]}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}"))


def delete_empty_folders(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_dir():
            if len(os.listdir(item)) == 0:
                os.rmdir(item)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def unpack_archive(path: Path, sort: bool) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            file_ext = item.suffix.lower()
            for cat, exts in CATEGORIES.items():
                if file_ext in exts and cat == "Archives":
                    archive_folder_name = item.stem
                    unpack_path = item.parent / archive_folder_name
                    unpack_path.mkdir(exist_ok=True)
                    shutil.unpack_archive(str(item), extract_dir=str(unpack_path))
                    if sort == True:
                        sort_folder(unpack_path)
                        print(f"{item} - unpacked and sorted")
                    if sort == False:
                        print(f"{item} - unpacked")


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder {path} not found."
    
    sort_folder(path)
    print(f"[{path}] \nSorted")
    delete_empty_folders(path)
    print("Empty folders deleted")
    wait_sort = True

    while wait_sort:
        sort = input("Sort unpacked archives? Y - Yes, N - No : ")
        if sort == "Y" or sort == "y":
            sort = True
            unpack_archive(path, True)
            wait_sort = False
        elif sort == "N" or sort == "n":
            sort = False
            unpack_archive(path, False)
            wait_sort = False


if __name__ == "__main__":
    print(main())