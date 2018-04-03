from collections import Counter
import numpy as np


# GLOBAL VARIABLES


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
