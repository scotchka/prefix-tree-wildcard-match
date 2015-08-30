import sys

data = [line.strip() for line in sys.stdin.readlines()]

n_patterns = int(data[0])

pattern_strings = data[1:1 + n_patterns]

data = data[1 + n_patterns:]

n_paths = int(data[0])

path_strings = data[1:1 + n_paths]

pattern_tree = {}

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
    def __init__(self, string):
        self.tokens = [item.strip() for item in string.split(',')]
        self.length = len(self.tokens)
        self.wildcards = len([item for item in self.tokens if item == '*'])

    def __repr__(self):
        return ','.join(self.tokens)

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
    suffix = [item.strip() for item in path.split('/') if item.strip()]
    queue = [(pattern_tree, [], suffix)]
    patterns = []
    while len(queue) > 0:
        tree, prefix, suffix = queue.pop(0)
        if len(suffix) == 0:
            break

        if len(suffix) == 1:
            if suffix[0] in tree and tree[suffix[0]].get('is_leaf'):
                string = ','.join(prefix + suffix[0:1])
                patterns.append(Pattern(string))

            if '*' in tree and tree['*'].get('is_leaf'):
                string = ','.join(prefix + ['*'])
                patterns.append(Pattern(string))

        if suffix[0] in tree:
            queue.append((tree[suffix[0]], prefix + suffix[0:1], suffix[1:]))
        if '*' in tree:
            queue.append((tree['*'], prefix + ['*'], suffix[1:]))

    if len(patterns) > 0:
        return sorted(patterns)[0]
    else:
        return 'NO MATCH'


for line in path_strings:
    print find_pattern(line)
