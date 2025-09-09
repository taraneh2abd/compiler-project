class A(F):
    def __init__(self, name=None, id=None):
        super().__init__()
        self.name = name
        self.id = id
    def A(self, a1,a2):
        pass

class B(object):
    def __init__(self, f=None):
        self._f = f  # -- F
    def B(self):
        pass
    def B(self, b1,b2):
        pass
    def set_f(self, f_object):
        """Set associated F."""
        self._f = f_object

    def get_f(self):
        """Get associated F."""
        return self._f

    def clear_f(self):
        """Clear associated F."""
        self._f = None

class C(object):
    def __init__(self, a=None):
        self._a = a  # -- A
    def C(self):
        pass
    def set_a(self, a_object):
        """Set associated A."""
        self._a = a_object

    def get_a(self):
        """Get associated A."""
        return self._a

    def clear_a(self):
        """Clear associated A."""
        self._a = None

class X(object):
    def __init__(self, x=None):
        self._x = x  # -- X
    def X(self):
        pass
    def set_x(self, x_object):
        """Set associated X."""
        self._x = x_object

    def get_x(self):
        """Get associated X."""
        return self._x

    def clear_x(self):
        """Clear associated X."""
        self._x = None

class F(object):
    def __init__(self):
        pass
    def F(self):
        pass


