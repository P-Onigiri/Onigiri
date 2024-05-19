import os
import shutil

main_dir = 'training_data'
classes = ['fire', 'no_fire']

if not os.path.exists(main_dir):
    os.makedirs(main_dir)

for class_name in classes:
    class_dir = os.path.join(main_dir, class_name)
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

def move_images(source_dir, class_name):
    source_files = os.listdir(source_dir)
    for file_name in source_files:
        if file_name.endswith('.png'):  
            src = os.path.join(source_dir, file_name)
            dst = os.path.join(main_dir, class_name, file_name)
            shutil.copyfile(src, dst)

source_dir_fire = r'C:\VVCE Hakathon\Train\fire'
source_dir_no_fire = r'C:\VVCE Hakathon\Train\non_fire'

move_images(source_dir_fire, 'fire')
move_images(source_dir_no_fire, 'no_fire')

train_dir = main_dir

print("Directory setup completed.")
print("train_dir:", train_dir)
