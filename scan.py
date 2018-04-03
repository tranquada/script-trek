from collections import Counter
import pandas as pd
import numpy as np


# GLOBAL VARIABLES


# CLASS: Scanner
class Scanner(object):
    """Object for scanning text files to examine character frequencies."""

    def __init__(self, file, encoding="latin-1"):
        self.data = {}
        with open(file, encoding=encoding) as f:
            self.data['raw'] = np.array(f.readlines())
        self.data['bytes'] = np.array(
            [bytearray(x, encoding="latin-1") for x in self.data['raw']]
        )
        self.data['counts'] = Counter()
        for x in self.data:
            for c in x:
                self.data['counts'][c] += 1
        self.data['df'] = pd.DataFrame(self.data['counts'])
