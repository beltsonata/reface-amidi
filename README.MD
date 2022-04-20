# Reface AMIDI

A quick pair of scripts for saving and loading patches on Yamaha Reface CS / CP / DX / YC on your Linux box. 
Or anything else that runs amidi, probably.

## Notes

Only the Reface CS has been tested (all I have access to).
PRs welcome.

## Requirements

Python 3 (3.8 was tested)
amidi (1.2.2 was tested)

# Python Dependencies

None

## Usage

There are two scripts. 

save_patch.py - Saves a patch on the Reface to a .sysex file.
load_patch.py - Loads a patch from a .sysex file onto the Reface

Both are very simple. To save a patch:

    python save_patch.py <path>

Optionally pass in the '-s' switch to skip prompting for overwrite when the file already exists.

To load a patch:

    python load_patch.py <path>


If you have more than one midi Reface connected then you will be prompted to select one.
