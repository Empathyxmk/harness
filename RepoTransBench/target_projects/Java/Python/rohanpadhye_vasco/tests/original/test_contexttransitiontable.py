import pytest

class Context:
    def __init__(self, method, id_, extra_false=None):  # Accept extra_false to simulate generic signature
        self.method = method
        self.id = id_
    def getId(self): return self.id
    def getMethod(self): return self.method
    def __eq__(self, other):
        return isinstance(other, Context) and self.method == other.method and self.id == other.id
    def __hash__(self):
        return hash((self.method, self.id))

class CallSite:
    def __init__(self, context, node):
        self.context = context
        self.node = node
    def __eq__(self, other):
        return isinstance(other, CallSite) and self.context == other.context and self.node == other.node
    def __hash__(self):
        return hash((self.context, self.node))

class ContextTransitionTable:
    def __init__(self):
        self.transitions = {}
        self.callers = {}
        self.default_call_sites = set()
        self.call_sites_of_context = {}

    def addTransition(self, call_site, ctx):
        self.transitions.setdefault(call_site, set()).add(ctx)
        if ctx is not None:
            self.callers.setdefault(ctx, set()).add(call_site)
        else:
            # Default/unknown transition
            self.default_call_sites.add(call_site)

    def getCalledContexts(self, call_site, method=None):
        ctxs = self.transitions.get(call_site)
        if ctxs is None:
            return None if method else set()
        if method is not None:
            for ctx in ctxs:
                if ctx and ctx.method == method:
                    return ctx
            return None
        return ctxs

    def hasCallers(self, ctx):
        return ctx in self.callers and bool(self.callers[ctx])

    def isDefaultCallSite(self, call_site):
        return call_site in self.default_call_sites

    def getDefaultCallSites(self):
        return self.default_call_sites

    def addCallSiteToContext(self, ctx, call_site):
        self.call_sites_of_context.setdefault(ctx, set()).add(call_site)

    def getCallSitesOfContext(self, ctx):
        return self.call_sites_of_context.get(ctx, set())

    def getCallers(self, ctx):
        return self.callers.get(ctx, set())

def test_add_and_query_transitions():
    table = ContextTransitionTable()
    ctxA = Context("foo", 1)
    ctxB = Context("bar", 2)
    site1 = CallSite(ctxA, "node1")
    site2 = CallSite(ctxB, "node2")
    # initially nothing
    assert not table.hasCallers(ctxB)
    assert table.getCalledContexts(site1, "bar") is None

    table.addTransition(site1, ctxB)
    called = table.getCalledContexts(site1)
    assert ctxB in called
    assert table.getCalledContexts(site1, "bar") == ctxB
    assert table.hasCallers(ctxB)

    # Adding again with a different context for site2 and null target
    table.addTransition(site2, None) # default/unknown transition
    assert table.isDefaultCallSite(site2)
    assert site2 in table.getDefaultCallSites()

def test_call_sites_of_context():
    table = ContextTransitionTable()
    ctxA = Context("foo", 1)
    site1 = CallSite(ctxA, "node1")
    table.addCallSiteToContext(ctxA, site1)
    s = table.getCallSitesOfContext(ctxA)
    assert site1 in s

def test_get_callers():
    table = ContextTransitionTable()
    ctxA = Context("foo", 1)
    ctxB = Context("bar", 2)
    site1 = CallSite(ctxA, "node1")
    table.addTransition(site1, ctxB)
    callers = table.getCallers(ctxB)
    assert site1 in callers