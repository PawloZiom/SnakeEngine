import os, sys, shutil


def delete_pycache(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir == "__pycache__":
                pycache_path = os.path.join(root, dir)
                print(f"Deleting {pycache_path}")
                shutil.rmtree(pycache_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deletePyCache.py <path to directory>")
        sys.exit(1)

    current_directory = sys.argv[1]
    delete_pycache(current_directory)
