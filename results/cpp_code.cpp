#include <string>
#include <vector>

class A;
class B;
class C;
class X;
class F;

using std::string;
using std::vector;

class A : public F {
public:
    A(std::string name, std::string id)
        : F(), name(name), id(id)
    {
        // constructor body
    }
    void A(std::string a1, std::string a2) {}

private:
    std::string name;
    std::string id;
};

class B {
public:
    B() {}
    void B() {}
    void B(std::string b1, std::string b2) {}
    void set_f(F* obj) { f = obj; }
    F* get_f() const { return f; }

private:
    F* f = nullptr;
};

class C {
public:
    C() {}
    void C() {}
    void set_a(A* obj) { a = obj; }
    A* get_a() const { return a; }

private:
    A* a = nullptr;
};

class X {
public:
    X() {}
    void X() {}
    void set_x(X* obj) { x = obj; }
    X* get_x() const { return x; }

private:
    X* x = nullptr;
};

class F {
public:
    F() {}
    void F() {}
};


