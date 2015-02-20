from itertools import chain
from nose.tools import assert_raises

T = True
F = False

class LogicError(Exception):
    pass

class Node(object):
    """Base class for logic nodes.

    A node forms an expression tree for a sentence of symbolic logic."""

    def __init__(self, *children):
        self.children = children

    def eval(self, model):
        """Evaluates the logic tree rooted at this node against a supplied model.

        Model is an assignment of truth values to atoms (dict of string -> bool)."""
        raise NotImplementedError

    def tree_print(self, d=0):
        """Recursively prints the logic tree to stdout."""
        raise NotImplementedError

    @property
    def l(self):
        return self.children[0]

    @property
    def r(self):
        try:
            return self.children[1]
        except IndexError:
            return None

class AndNode(Node):
    def eval(self, model):
        return all([n.eval(model) for n in self.children])
    def tree_print(self, d=0):
        print("  "*d + "&")
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class OrNode(Node):
    def eval(self, model):
        return any([n.eval(model) for n in self.children])
    def tree_print(self, d=0):
        print("  "*d + "v")
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class NotNode(Node):
    def eval(self, model):
        if len(self.children) != 1:
            raise LogicError("NOT is undefined for multiple children.")
        return not self.l.eval(model)
    def tree_print(self, d=0):
        print("  "*d +"~")
        self.l.tree_print(d+1)

class AtomNode(Node):
    """These nodes will always form the leaves of a logic tree.

    They are the only node whose children are strings, not other nodes."""
    def eval(self, model):
        return model[self.l]
    def tree_print(self, d=0):
        print("  "*d + self.l)

def test_single_node_eval():
    a = AtomNode("a")
    b = AtomNode("b")
    model = {"a": T, "b": F}
    assert a.eval(model)
    assert not b.eval(model)
    assert OrNode(a, a).eval(model)
    assert OrNode(a, b).eval(model)
    assert OrNode(b, a).eval(model)
    assert not OrNode(b, b).eval(model)
    assert AndNode(a, a).eval(model)
    assert not AndNode(a, b).eval(model)
    assert not AndNode(b, a).eval(model)
    assert not AndNode(b, b).eval(model)
    assert not NotNode(a).eval(model)
    assert NotNode(b).eval(model)

def test_compound_node_eval():
    a = AtomNode("a")
    b = AtomNode("b")
    model = {"a": T, "b": F}
    assert NotNode(NotNode(a)).eval(model)
    assert NotNode(AndNode(a, b)).eval(model)
    assert not NotNode(OrNode(a, b)).eval(model)
    assert OrNode(NotNode(AndNode(a,b)), NotNode(OrNode(a, b))).eval(model)
    assert NotNode(OrNode(b, b))

def test_many_ands():
    a = AtomNode("A")
    b = AtomNode("B")
    model = {"A": T, "B": F}
    assert AndNode(a, a, a).eval(model)
    assert AndNode(a, a, a, a).eval(model)
    assert not AndNode(a, a, b).eval(model)
    assert not AndNode(a, b, a).eval(model)
    assert not AndNode(b, a, a).eval(model)

def test_many_ors():
    a = AtomNode("A")
    b = AtomNode("B")
    model = {"A": T, "B": F}
    assert OrNode(b, b, a).eval(model)
    assert OrNode(b, a, a).eval(model)
    assert OrNode(a, b, a).eval(model)
    assert OrNode(a, a, b).eval(model)
    assert not OrNode(b, b, b).eval(model)

def test_single_not():
    n = NotNode(AtomNode("A"), AtomNode("B"))
    model = {"A": True, "B": True}
    assert_raises(LogicError, n.eval, model)

