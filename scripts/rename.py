# This is a small script designed to rename the script files
import re                              # Python regular expressions module
from os import listdir                 # Directory listing utility
from os import rename                  # File renaming utility

# Query names of all files in directory
scripts = listdir()
scripts.remove('.DS_Store')

# Define serial regex string
serial = re.compile(r'#\d{5}-\d{3}')

# Loop over all episodes
for episode in scripts:
    with open(episode) as f:  # Read in file
        data = f.read()

    # Look for regex match
    x = serial.search(data)

    # Extract result value
    number = data[x.start():x.end()][1:]

    # Rename file
    rename(episode, '{}.txt'.format(number))
