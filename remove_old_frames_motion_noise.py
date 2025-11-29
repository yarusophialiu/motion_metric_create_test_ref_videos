import os

algorithm = "motion_noise"

scenes = os.listdir(source_dir)

for scene in scenes:
    for level_idx in [0, 1, 2]:
        target_dir = "./" + scene + "/" + algorithm + "/level" + str(level_idx)
        
        for restir_file in os.listdir(target_dir):
            os.remove(os.path.join(target_dir, restir_file))
    print("Done with " + scene)