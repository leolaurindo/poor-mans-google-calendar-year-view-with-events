import os
import glob

folder_path = 'calendars'

files = sorted(glob.glob(os.path.join(folder_path, '*')), key=os.path.getctime, reverse=True)

for file in files[1:]:
    os.remove(file)