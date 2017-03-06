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
