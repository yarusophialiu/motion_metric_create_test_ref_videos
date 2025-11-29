import re
import os
from pathlib import Path

# =============================
# 🔧 EDIT THESE
# =============================
# Rename frames like ...reweightedColor.00120.png to 00000.png
# Set this to the folder that directly contains many subfolders like dist_type/level/
# Example: r"D:\motion-metric\all_sequences\bistro"
#  dlss_rr motion_noise motion_resolution
# scene_dir = Path(r"D:\motion-metric\all_sequences\subway\dlss_rr")

# If you want to only rename a single folder, set it here and set `recursive = False`
single_folder = None  # e.g. Path(r"D:\...\bistro\H264\level1")

recursive = True      # True = process all dist_type/level subfolders; False = only `single_folder`
start_index = 0       # first index (00000)
pad_width = 5         # digits in the new names
ext = ".png"          # expected extension; rename only these
dry_run = False       # True = just print what would happen
# =============================


def numeric_suffix(path: Path):
    """
    Extract the trailing integer in the stem like ...reweightedColor.00120 from filename.
    Returns an int if found, else None.
    """
    # Consider filenames like "zeroday....00120.png" or possibly without extension handled by Path.stem
    # We look for the last group of digits in the *whole name* excluding extension.
    m = re.search(r'(\d+)$', path.stem)
    return int(m.group(1)) if m else None


def find_target_dirs():
    if not recursive and single_folder:
        return [Path(single_folder)]
    # Heuristic: any folder under scene_dir containing PNGs is a target
    targets = []
    for d in scene_dir.rglob("*"):
        if d.is_dir():
            try:
                has_png = any(p.is_file() and p.suffix.lower() == ext for p in d.iterdir())
            except PermissionError:
                has_png = False
            if has_png:
                targets.append(d)
    return sorted(targets)


def rename_folder(folder: Path):
    files = sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ext])

    if not files:
        print(f"🔎 No {ext} files in: {folder}")
        return

    # Sort by numeric suffix if present; otherwise by name
    with_suffix = []
    without_suffix = []
    for f in files:
        num = numeric_suffix(f)
        (with_suffix if num is not None else without_suffix).append((num, f))

    if with_suffix:
        ordered = [f for _, f in sorted(with_suffix, key=lambda x: x[0])]
        if without_suffix:
            # append any without numeric suffix after, in name order
            ordered += [f for _, f in sorted([(None, f) for f in without_suffix], key=lambda x: x[1].name)]
    else:
        ordered = sorted([f for _, f in without_suffix], key=lambda p: p.name)

    # Build mapping
    mapping = []
    for i, src in enumerate(ordered, start=start_index):
        dst = src.with_name(str(i).zfill(pad_width) + ext)
        mapping.append((src, dst))

    print(f"\n📁 Folder: {folder}")
    print(f"   Files detected: {len(files)} → Will rename to {pad_width}-digit sequential names starting at {str(start_index).zfill(pad_width)}")

    # Phase 1: rename to temporaries to avoid collisions
    temps = []
    for idx, (src, dst) in enumerate(mapping):
        tmp = src.with_name(f"__tmp_renaming_{idx}__{src.name}")
        temps.append((src, tmp, dst))
        if dry_run:
            print(f"DRY-RUN: {src.name}  ->  {tmp.name}")
        else:
            os.replace(src, tmp)

    # Phase 2: rename temporaries to final names
    for src, tmp, dst in temps:
        if dry_run:
            print(f"DRY-RUN: {tmp.name}  ->  {dst.name}")
        else:
            os.replace(tmp, dst)

    print("   ✅ Done." + (" (dry-run)" if dry_run else ""))


def main():
    base = single_folder if (not recursive and single_folder) else scene_dir
    if not base or not Path(base).exists():
        raise SystemExit(f"Path not found: {base}")

    targets = find_target_dirs()
    if not targets:
        print("No target folders found.")
        return

    for t in targets:
        rename_folder(t)


if __name__ == "__main__":
    scenes = ['attic', 'bistro_exterior', 'classroom', 'landscape', 'marbles', 'pink_room']
    root = r'D:\motion-metric\all_sequences'
    for scene in scenes:
        print(f'\n============ scene {scene}============')
        for dist_type in ["dlss_rr", "motion_noise", "motion_resolution"]:
            scene_dir = Path(f"{root}/{scene}/{dist_type}")
            print(f'scene_dir {scene_dir}')
            main()
