# prefix-tree-wildcard-match

Given list of directory patterns possibly including wildcards and list of directories, find the best matching
pattern for each path. In case of multiple matching patterns, prefer fewest wildcards and then most specific pattern.

Example:

a/b/c matches a,\*,\* and \*,b,\* and \*,\*,c

a,\*,\* is most specific
