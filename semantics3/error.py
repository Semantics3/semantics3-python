class Semantics3Error(Exception):
    def __init__(self, expr, msg):
        Exception.__init__(self, msg)
        self.expr = expr
        self.msg = msg
