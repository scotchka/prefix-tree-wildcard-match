import sys
from collections import deque

# read input
data = [line.strip() for line in sys.stdin.readlines()]

n_patterns = int(data[0])

pattern_strings = data[1:1 + n_patterns]

data = data[1 + n_patterns:]

n_paths = int(data[0])

path_strings = data[1:1 + n_paths]

pattern_tree = {}

# built prefix tree of patterns using a nested dictionary
for line in pattern_strings:
    pattern = map(str.strip, line.split(','))
    level = pattern_tree
    while len(pattern) > 0:
        key = pattern.pop(0)
        if key not in level:
            level[key] = {}
        level = level[key]
    level['is_leaf'] = True


class Pattern(object):
    """
    pattern class with custom ordering
    """

    def __init__(self, string):
        self.tokens = [item.strip() for item in string.split(',')]
        self.length = len(self.tokens)
        self.wildcards = len([item for item in self.tokens if item == '*'])

    def __repr__(self):
        return ','.join(self.tokens)

    # less than operation. Based on pattern length, then number of wildcards, then position of left-most wildcard
    def __lt__(self, other):
        if self.length < other.length:
            return True
        elif self.length > other.length:
            return False

        if self.wildcards < other.wildcards:
            return True
        elif self.wildcards > other.wildcards:
            return False

        for a, b in zip(self.tokens, other.tokens):
            if a != '*':
                if b == '*':
                    return True
                if a < b:
                    return True
            elif b != '*':
                return False

        return False

    # all other comparison operators follow from less than and equals
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        return self.tokens == other.tokens

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


def find_pattern(path):
    """
    Breadth-first search for most specific pattern that matches path
    :param path: path string
    :return: most specific pattern, or NO MATCH
    """
    suffix = [item.strip() for item in path.split('/') if item.strip()]
    queue = deque()
    queue.append((pattern_tree, [], suffix))  # search queue maintains the subtree, prefix, and suffix
    patterns = []  # list of matching patterns
    while len(queue) > 0:
        tree, prefix, suffix = queue.popleft()
        if len(suffix) == 0:  # exhausted path, stop search
            break

        # check for matching patterns
        if len(suffix) == 1:
            if suffix[0] in tree and tree[suffix[0]].get('is_leaf'):
                string = ','.join(prefix + suffix[0:1])
                patterns.append(Pattern(string))

            if '*' in tree and tree['*'].get('is_leaf'):
                string = ','.join(prefix + ['*'])
                patterns.append(Pattern(string))

        # add subtrees to search queue
        if suffix[0] in tree:
            queue.append((tree[suffix[0]], prefix + suffix[0:1], suffix[1:]))
        if '*' in tree:
            queue.append((tree['*'], prefix + ['*'], suffix[1:]))

    if len(patterns) > 0:
        return min(patterns)  # minimum element based on custom comparison
    else:
        return 'NO MATCH'


for line in path_strings:
    print find_pattern(line)
