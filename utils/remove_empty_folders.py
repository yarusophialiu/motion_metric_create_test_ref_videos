import os

root = r"D:\motion-metric\pilot-videos\subway"

empty_dir = []
# Walk from bottom up so subfolders are removed before parents
for dirpath, dirnames, filenames in os.walk(root, topdown=False):
    # If no files and no subdirectories left, remove this folder
    if not dirnames and not filenames:
        try:
            os.rmdir(dirpath)
            empty_dir.append(dirpath)
            print(f"🗑️ Removed empty folder: {dirpath}")
        except OSError as e:
            print(f"⚠️ Could not remove {dirpath}: {e}")
print(f'empty_dir {empty_dir}')
print("✅ Finished removing empty folders.")
