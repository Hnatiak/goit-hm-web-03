import argparse
from pathlib import Path
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

def copy_file(file_path: Path) -> None:
    ext = file_path.suffix[1:]
    ext_folder = output / ext
    try:
        ext_folder.mkdir(exist_ok=True, parents=True)
        copyfile(file_path, ext_folder / file_path.name)
    except OSError as err:
        logging.error(err)

def process_folder(folder_path: Path) -> None:
    with ThreadPoolExecutor() as executor:
        futures = []
        for item in folder_path.iterdir():
            if item.is_file():
                futures.append(executor.submit(copy_file, item))
                print(f"Processing folder: {folder_path}")
            elif item.is_dir():
                futures.append(executor.submit(process_folder, item))
                print(f"Processing folder: {folder_path}")
        for future in futures:
            future.result()
            print(f"Future: {future}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    if source.is_dir():
        process_folder(source)
    else:
        logging.error("Invalid folder path.")




# import argparse
# from pathlib import Path
# from shutil import copyfile
# from concurrent.futures import ThreadPoolExecutor
# import logging

# parser = argparse.ArgumentParser(description="Sorting folder")
# parser.add_argument("--source", "-s", help="Source folder", required=True)
# parser.add_argument("--output", "-o", help="Output folder", default="dist")

# args = vars(parser.parse_args())
# source = Path(args.get("source"))
# output = Path(args.get("output"))

# def copy_file(file_path: Path) -> None:
#     ext = file_path.suffix[1:]
#     ext_folder = output / ext
#     try:
#         ext_folder.mkdir(exist_ok=True, parents=True)
#         copyfile(file_path, ext_folder / file_path.name)
#     except OSError as err:
#         logging.error(err)

# def process_folder(folder_path: Path) -> None:
#     with ThreadPoolExecutor() as executor:
#         for item in folder_path.iterdir():
#             if item.is_file():
#                 executor.submit(copy_file, item)
#                 print(f"Processing folder: {folder_path}")
#         for item in folder_path.iterdir():
#             if item.is_dir():
#                 process_folder(item)
#                 print(f"Processing folder: {folder_path}")

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

#     if source.is_dir():
#         process_folder(source)
#     else:
#         logging.error("Invalid  folder path.")
