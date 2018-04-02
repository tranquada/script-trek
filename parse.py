import re                              # Python library regex module
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
def code(data, code):
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
        self.data['code8'] = np.array(
            [code(x, 'code8') for x in self.data['bytes']]
        )
        self.data['code10'] = np.array(
            [code(x, 'code10') for x in self.data['bytes']]
        )
        self.data['punc2'] = np.array(
            [code(x, 'punc2') for x in self.data['bytes']]
        )
        self.data['punc8'] = np.array(
            [code(x, 'punc8') for x in self.data['bytes']]
        )
        self.data['punc10'] = np.array(
            [code(x, 'punc10') for x in self.data['bytes']]
        )
