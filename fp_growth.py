import typing
from collections import Counter, defaultdict
from itertools import combinations
from pprint import pprint

T = typing.TypeVar('T')


class Node:
    def __init__(
            self,
            value: T,
            count: int,
            parent: typing.Optional['Node']):
        self.value: T = value
        self.count: int = count
        self.parent: Node = parent
        self.link: typing.Optional[Node] = None
        self.children: typing.List[Node] = []

    def __contains__(self, value: T) -> bool:
        return self[value] is not None

    def append(self, value: T) -> 'Node':
        child = Node(value, 1, self)
        self.children.append(child)
        return child

    def __getitem__(self, value: T) -> typing.Optional['Node']:
        for node in self.children:
            if node.value == value:
                return node
        return None


class FPTree(object):
    def __init__(
            self,
            transactions: typing.List[typing.Tuple],
            threshold: float,
            root_value: T,
            root_count: int
    ):
        self.threshold = threshold
        self.frequent = self.find_frequent_items(
            transactions, self.threshold)
        self.headers: typing.Dict[T, Node] = {
            k: None for k in self.frequent.keys()}
        self.root = self.build_tree(
            transactions, root_value, root_count)

    @staticmethod
    def find_frequent_items(
            transactions, threshold) -> typing.Dict[T, int]:
        items = Counter()

        for transaction in transactions:
            for item in transaction:
                items[item] += 1

        return {x: items[x] for x in items if items[x] >= threshold}

    def build_tree(
            self, transactions, root_value, root_count) -> Node:
        root = Node(root_value, root_count, None)

        for transaction in transactions:
            items = sorted(
                [x for x in transaction if x in self.frequent],
                key=lambda x: self.frequent[x],
                reverse=True
            )
            self.insert_tree(items, root)
        return root

    def insert_tree(self, items: typing.List[T], parent: Node):
        while items:
            first, *items = items
            if first in parent:
                parent[first].count += 1
            else:
                child = parent.append(first)
                child.link = self.headers[first]
                self.headers[first] = child
            parent = parent[first]

    @staticmethod
    def tree_has_single_path(node: Node) -> bool:
        while True:
            num = len(node.children)
            if num > 1:
                return False
            elif num == 0:
                return True
            node = node.children[0]

    def generate_pattern_list(self) -> typing.Dict[tuple, int]:
        patterns = {}
        items = self.frequent.keys()
        suffix_value: typing.List[T] = []
        if self.root.value is not None:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in combinations(items, i):
                patterns[
                    tuple(sorted(list(subset) + suffix_value))
                ] = min([self.frequent[x] for x in subset])
        return patterns

    def mine_tree(self) -> typing.Dict[tuple, int]:
        patterns: typing.Dict[tuple, int] = defaultdict(int)
        order = sorted(
            self.frequent.keys(), key=lambda x: self.frequent[x])
        for item in order:
            cond_tree = []
            node = self.headers[item]
            while node is not None:
                path = []
                parent = node.parent
                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent
                path = tuple(path)
                for i in range(node.count):
                    cond_tree.append(path)
                node = node.link
            subtree = FPTree(
                cond_tree, self.threshold, item, self.frequent[item])
            subtree_pattern = subtree.mine_patterns()
            for pattern in subtree_pattern.keys():
                patterns[pattern] += subtree_pattern[pattern]
        return dict(patterns)

    def mine_patterns(self) -> typing.Dict[tuple, int]:
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            patterns = self.mine_tree()
            suffix = self.root.value
            if suffix is not None:
                new_patterns = {}
                for key in patterns.keys():
                    new_patterns[
                        tuple(sorted(list(key) + [suffix]))
                    ] = patterns[key]
                patterns = new_patterns
            return patterns

    @property
    def patterns(self) -> typing.Dict[tuple, int]:
        return self.mine_patterns()


class RuleRet:
    def __init__(self, d: typing.List):
        self.d = d

    @staticmethod
    def _p(_s):
        return '{{{}}}'.format(', '.join(str(k) for k in _s))

    def __repr__(self):
        return '\n'.join(['{} => {}'.format(self._p(k[0]), self._p(k[1])) for k in self.d])


def association_rules(patterns, min_confidence) -> RuleRet:
    rules = []
    for itemset, upper in patterns.items():
        for i in range(1, len(itemset)):
            for fore in combinations(itemset, i):
                # fore = tuple(sorted(fore))
                back = tuple(
                    sorted(set(itemset) - set(fore)))

                if fore in patterns:
                    confidence = float(upper) / patterns[fore]
                    if confidence >= min_confidence:
                        rules.append([fore, back, confidence])

    return RuleRet(rules)


def fp_growth(transactions: typing.List[tuple],
              min_support: float,
              min_confidence: float) -> (typing.Dict[tuple, int], RuleRet):
    tree = FPTree(transactions, min_support * len(transactions), None, 0)
    _p = tree.patterns
    return _p, association_rules(_p, min_confidence)


if __name__ == '__main__':
    s = [(1, 2, 5), (2, 4), (2, 3), (1, 2, 4),
         (1, 3), (2, 3), (1, 3), (1, 2, 3, 5), (1, 2, 3)]
    # s = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4],
    #      [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
    pprint(fp_growth(s, 0.2, 0.5))