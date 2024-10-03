import os
import shutil
from pathlib import Path
import time

def sync_directories(src_dir, dst_dir):
    # Ensure src and dst directories exist
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    if not src_dir.is_dir():
        print(f"Source directory '{src_dir}' does not exist.")
        return

    if not dst_dir.is_dir():
        print(f"Destination directory '{dst_dir}' does not exist, creating it.")
        dst_dir.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src_dir):
        rel_path = Path(root).relative_to(src_dir)
        dst_subdir = dst_dir / rel_path

        if not dst_subdir.exists():
            dst_subdir.mkdir(parents=True)

        for file in files:
            src_file = Path(root) / file
            dst_file = dst_subdir / file

            # Check if a file exists in destination or needs an update
            if not dst_file.exists() or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                print(f"Copying {src_file} to {dst_file}")
                shutil.copy2(src_file, dst_file)

def main():
    #src_dir = input("Enter the source directory path: ")
    #dst_dir = input("Enter the destination directory path: ")

    src_dir = "H:\Repo\C2_py"
    dst_dir = "H:\Repo\C2_py\outcoming"

    start_time = time.time()
    sync_directories(src_dir, dst_dir)
    end_time = time.time()

    print(f"Sync completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
