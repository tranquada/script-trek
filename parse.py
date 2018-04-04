import json                            # Python json handling
import pandas as pd                    # Data handling
import numpy as np                     # More data handling


# MODULE INTRODUCTION
"""This module contains functions for script text parsing."""


# GLOBAL VARIABLES
BYTE_MAPPINGS = 'byte_mappings.csv'  # Byte to character and signature codes
MAPPINGS = pd.read_csv(BYTE_MAPPINGS, index_col='bytes')  # Loads codes to df

SCRIPTS = './scripts/'  # Specifies scripts folder location
PATH = SCRIPTS + '{}'  # Specifies path to script folder for loading files

TABS = [9]                             # Byte code for tab
SPACES = [32]                          # Byte code for space
QUOTES = [34]                          # Byte code for double quote
APOSTROPHES = [39]                     # Byte code for single quote
PARENTHESES = [40, 41]                 # Byte codes for parentheses
COMMAS = [44]                          # Byte code for comma
HYPHENS = [45]                         # Byte code for hyphen
PERIOD = [46]                          # Byte code for period
SLASHES = [47]                         # Byte code for forward slash
COLONS = [58]                          # Byte code for colon
NUMS = [x for x in range(48, 58)]      # Byte code range for numbers
UPPERS = [x for x in range(65, 91)]    # Byte code range for uppercase chars
LOWERS = [x for x in range(97, 123)]   # Byte code range for lowercase chars
EXOTICS = [x for x in range(128, 256)]  # Byte code range for exotic chars

# PANDAS UTILITY FUNCTIONS


# PARSING UTILITY functions
def encode(data, code):
    """Produces the type signature of the input string using the appropriate
    code mapping specified."""
    return [MAPPINGS[code].iloc[char] for char in data]


# TxtLoader OBJECT
class TxtLoader(object):
    """Class used to load episode scripts from the original text files."""

    def __init__(self, file):
        # Initialize internal data store as dict
        self.data = {}
        # Open file and read all lines into an array
        with open(PATH.format(file), encoding="latin-1") as f:
            self.data['raw'] = np.array(f.readlines())
        # Convert raw strings into bytearrays
        self.data['bytes'] = np.array(
            [bytearray(x, encoding="latin-1") for x in self.data['raw']]
        )
        # Convert raw strings into lists of tokens
        self.data['tokens'] = np.array([x.split() for x in self.data['raw']])

    def encode_sig(self, code):
        """Creates a new signature encoding for all lines based on the given
        code and adds it to the data dictionary. Signature code must be one of
        the columns included in the BYTE_MAPPINGS file."""

        self.data[code] = pd.DataFrame(
            [encode(x, code) for x in self.data['bytes']]
        )

    def export_csv(self, file):
        """Exports the raw line string data to a CSV file. Must pass the
        desired filename for CSV export."""

        pd.DataFrame(self.data['raw']).to_csv(file)
