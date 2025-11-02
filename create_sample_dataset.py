import shutil
from pathlib import Path

root = Path(r"C:\Users\15142\Projects\motion-metric\all_sequences")
dst_root = Path(r"C:\Users\15142\Projects\motion-metric\test_all_sequences")

scenes = ["attic"]

IMG_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}

MAX_PER_FOLDER = 480

for scene in scenes:
    scene_dir = root / scene
    if not scene_dir.exists():
        print(f"[WARN] Scene folder not found: {scene_dir}")
        continue

    # Walk every directory under this scene (including the scene_dir itself)
    for folder in scene_dir.rglob("*"):
        if not folder.is_dir():
            continue

        # Collect images directly inside this folder (not recursive here)
        images = sorted([p for p in folder.iterdir() if p.suffix.lower() in IMG_EXTS and p.is_file()])

        if not images:
            continue  # nothing to copy from this folder

        # Determine destination folder by preserving path relative to scene_dir
        rel = folder.relative_to(scene_dir)  # e.g., reference/level0
        dst_folder = dst_root / scene / rel
        dst_folder.mkdir(parents=True, exist_ok=True)

        to_copy = images[:MAX_PER_FOLDER]  # deterministic: first 480 by name
        for src_img in to_copy:
            shutil.copy2(src_img, dst_folder / src_img.name)

        print(f"[OK] Copied {len(to_copy):4d} file(s) from {folder} -> {dst_folder}")
