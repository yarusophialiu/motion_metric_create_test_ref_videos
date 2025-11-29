import os

root = r"D:\motion-metric\all_sequences"

for scene_name in os.listdir(root):
    scene_path = os.path.join(root, scene_name)
    if not os.path.isdir(scene_path):
        continue

    for subfolder in os.listdir(scene_path):
        old_path = os.path.join(scene_path, subfolder)
        if os.path.isdir(old_path) and subfolder == "50_90_130":
            new_path = os.path.join(scene_path, "judder")
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {old_path} -> {new_path}")

print("🎉 All matching folders renamed successfully.")
