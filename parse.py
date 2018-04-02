import json                            # Python json handling
import pandas as pd                    # Data handling
import numpy as np                     # More data handling


# MODULE INTRODUCTION
"""This module contains functions for script text parsing."""


# GLOBAL VARIABLES
BYTE_MAPPINGS = 'byte_mappings.csv'
MAPPINGS = pd.read_csv(BYTE_MAPPINGS, index_col='bytes')
SCRIPTS = './scripts/'
PATH = './scripts/{}'


# PANDAS UTILITY FUNCTIONS


# PARSING UTILITY functions
def encode(data, code):
    """Produces the type signature of the input string using the appropriate
    code mapping specified."""
    return np.array([MAPPINGS[code].iloc[char] for char in data])


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
        # Use bytearrays to parse line signatures
        self.encode_sig('code8')
        self.encode_sig('code10')
        self.encode_sig('punc2')
        self.encode_sig('punc8')
        self.encode_sig('punc10')

    def encode_sig(self, code):
        self.data[code] = np.array(
            [encode(x, code) for x in self.data['bytes']]
        )
