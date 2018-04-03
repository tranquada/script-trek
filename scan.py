from collections import Counter
import pandas as pd
import numpy as np


# GLOBAL VARIABLES
CONTROLS = [x for x in range(0, 32)]
NUMS = [x for x in range(48, 58)]
UPPERS = [x for x in range(65, 91)]
LOWERS = [x for x in range(97, 123)]
PUNCS_1 = [x for x in range(32, 48)]
PUNCS_2 = [x for x in range(58, 65)]
PUNCS_3 = [x for x in range(91, 97)]
PUNCS_4 = [x for x in range(123, 128)]
EXOTICS = [x for x in range(128, 256)]
BASICS = [9, 10, 32, 46]
BRACKETS = [40, 41, 60, 62, 91, 93, 123, 125]
SPLITTERS = [47, 58, 92, 124]
HYPHENS = [45, 95]
COMMON_PUNC = [33, 34, 39, 44, 59, 63]
MISC_PUNC = [35, 36, 37, 38, 42, 43, 61, 64, 94, 96, 126]
OPERATORS = [37, 42, 43, 61, 45, 95]


# CLASS: Scanner
class Scanner(object):
    """Object for scanning text files to examine character frequencies."""

    def __init__(self, file, encoding="latin-1"):
        self.encoding = encoding
        self.data = {}
        try:
            with open(file, encoding=encoding) as f:
                self.data['raw'] = np.array(f.readlines())
        except:
            print('Python could not interpret file using {}.'.format(encoding))
        self.data['bytes'] = np.array(
            [bytearray(x, encoding="latin-1") for x in self.data['raw']]
        )
        self.data['counts'] = Counter()
        for x in self.data['bytes']:
            for c in x:
                self.data['counts'][c] += 1

        self.chars = pd.DataFrame()
        for x in self.data['counts']:
            self.chars[x] = [self.data['counts'][x]]
        self.chars = self.chars.reindex(sorted(self.chars.columns), axis=1)

    def group(self, types):
        return self.chars[[x for x in types if x in self.chars.columns]]
