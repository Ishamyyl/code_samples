#!/usr/bin/env python3

import sys
from pathlib import Path
import re
from collections import Counter

def run():
    file_name = sys.argv[1]
    with Path(file_name).open('r') as f:
        file_raw = f.read()
    most_common_word, most_common_count = Counter(w for w in re.split('\W+', file_raw) if w).most_common(1)[0]
    print(f'"{most_common_word}" at {most_common_count} times')
    
if __name__ == '__main__':
    run()
