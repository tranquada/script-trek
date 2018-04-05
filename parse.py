import json                            # Python json handling
import re                              # Python regular expression handling
import pandas as pd                    # Data handling
import numpy as np                     # More data handling
from tqdm import tqdm_notebook as tq   # Progress bar for Jupyter Notebook


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
PERIODS = [46]                         # Byte code for period
SLASHES = [47]                         # Byte code for forward slash
COLONS = [58]                          # Byte code for colon
NUMS = [x for x in range(48, 58)]      # Byte code range for numbers
UPPERS = [x for x in range(65, 91)]    # Byte code range for uppercase chars
LOWERS = [x for x in range(97, 123)]   # Byte code range for lowercase chars
EXOTICS = [x for x in range(128, 256)]  # Byte code range for exotic chars
LETTERS = r'\w'                        # RegEx string for word chars
NONLETTERS = r'\W'                     # RegEx string for non-word chars
WHITESPACES = r'\s'                    # RegEx string for whitespace chars
NONWHITESPACES = r'\S'                 # RegEx string for non-whitespace chars


# PANDAS UTILITY FUNCTIONS


# PARSING UTILITY FUNCTIONS
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
        print("1 > Lines loaded from file to data['raw']")

        # Convert raw strings into bytearrays
        self.data['bytes'] = np.array(
            [bytearray(x, encoding="latin-1") for x in self.data['raw']]
        )
        print("2 > Bytearrays created and stored in data['bytes']")

        # Convert raw strings into lists of tokens
        self.data['tokens'] = np.array([x.split() for x in self.data['raw']])
        print("3 > Tokens created and stored in data['tokens']")

        # Count key characters for analysis
        print("4 > Writing metrics to data['metrics']")
        self.data['metrics'] = self.get_metrics()

    # Counting functions
    def byte_count(self, codelist, line):
        total = 0
        for x in codelist:
            total += self.data['bytes'][line].count(x)
        return total

    def regex_count(self, codestring, line):
        return len(re.findall(codestring, self.data['raw'][line]))

    def token_count(self, line):
        return len(self.data['tokens'][line])

    def get_metrics(self):
        """Method for extracting key line measurements for analysis. Loops over
        lines and calls counting functions to extract features."""

        results = pd.DataFrame()
        for i in tq(range(len(self.data['raw']))):
            metrics = {
                'line_idx': i,
                'chars': len(self.data['raw'][i]),
                'clean': self.data['raw'][i].strip(),
                'min_char': min(self.data['bytes'][i]),
                'max_char': max(self.data['bytes'][i]),
                'n_tab': self.byte_count(TABS, i),
                'n_space': self.byte_count(SPACES, i),
                'n_quote': self.byte_count(QUOTES, i),
                'n_apostrophe': self.byte_count(APOSTROPHES, i),
                'n_parenthesis': self.byte_count(PARENTHESES, i),
                'n_comma': self.byte_count(COMMAS, i),
                'n_hyphen': self.byte_count(HYPHENS, i),
                'n_period': self.byte_count(PERIODS, i),
                'n_slash': self.byte_count(SLASHES, i),
                'n_colon': self.byte_count(COLONS, i),
                'n_nums': self.byte_count(NUMS, i),
                'n_uppers': self.byte_count(UPPERS, i),
                'n_lowers': self.byte_count(LOWERS, i),
                'n_exotics': self.byte_count(EXOTICS, i),
                'n_letters': self.regex_count(LETTERS, i),
                'n_nonletters': self.regex_count(NONLETTERS, i),
                'n_whitespaces': self.regex_count(WHITESPACES, i),
                'n_nonwhitespaces': self.regex_count(NONWHITESPACES, i),
                'n_tokens': self.token_count(i),
            }
            results = results.append(metrics, ignore_index=True)
        cols = list(results.columns.values)
        for x in cols:
            if x != 'clean':
                results[x] = results[x].astype(int)
        return results.set_index('line_idx')

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

    def import_training(self, file):
        self.data['training'] = pd.read_csv(
            file, index_col='line_idx').drop(['line'], axis=1)
