from Settings import *
import random
import shutil

num_of_participants = 75
num_of_repeatitions = 3

"""
Usage:
put texts in 'Texts" directory.
change above parameters accordingly.
run.
"""

# All files and folders in "Texts" directory
files_folders = os.listdir(TEXTS_PATH)

# Just files
files = list(filter(lambda f: os.path.isfile(os.path.join(TEXTS_PATH, f)), files_folders))

# Number of files
num_of_files = len(files)

# Create "SplitedTexts" directory
if not os.path.exists(os.path.join(TEXTS_PATH, "SplitedTexts")):
    os.mkdir(os.path.join(TEXTS_PATH, "SplitedTexts"))

# Create directories for each participant
for i in range(1, num_of_participants + 1):
    if not os.path.exists(os.path.join(TEXTS_PATH, "SplitedTexts", str(i))):
        os.mkdir(os.path.join(TEXTS_PATH, "SplitedTexts", str(i)))

# Calculate number of files per participant
files_per_participant = num_of_files * num_of_repeatitions / num_of_participants

# If division is int
if files_per_participant == int(files_per_participant):

    # Shuffle files
    random.shuffle(files)

    # Casting
    files_per_participant = int(files_per_participant)

    file_counter = 0

    # Split files for each participant
    for i in range(1, num_of_participants + 1):

        # Files for current participant
        current_files = files[file_counter : file_counter + files_per_participant]

        # Advance file_counter by number of files per participant
        file_counter += files_per_participant

        # Looping files
        if file_counter == num_of_files:
            file_counter = 0

        # Copying files
        for file in current_files:
            shutil.copyfile(os.path.join(TEXTS_PATH, file), os.path.join(TEXTS_PATH, "SplitedTexts", str(i), file))

else:
    print("Not int division")