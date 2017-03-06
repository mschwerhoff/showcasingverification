Tags: swap, VeriFast, Permissions
Title: Swap in VeriFast
Date: 2017-03-05

A VeriFast encoding of a method that swaps the values of two fields `x.f` and `y.f`.

    :::text
    #include "stdlib.h"

    struct Cell {
      int f;
    };

    void swap(struct Cell* x, struct Cell* y)
      //@ requires x->f |-> ?v &*& y->f |-> ?w;
      //@ ensures  x->f |-> w &*& y->f |-> v;
    {
      int tmp = x->f;
      x->f = y->f;
      y->f = tmp;
    }

Note that the precondition disallows aliasing between `x` and `y`.
