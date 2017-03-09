Tags: LinkedList, LinkedList-Prepend, Viper, Permissions
Title: LinkedList-Prepend in Viper
Date: 2017-03-09

A Viper encoding of a method that prepends a value to a linked list of integers.

    :::text
    field val: Int
    field next: Ref

    predicate LinkedList(x: Ref) {
      acc(x.val) && acc(x.next) &&
      (x.next != null ==> LinkedList(x.next))
    }

    function head(x: Ref): Int
      requires LinkedList(x)
    { unfolding LinkedList(x) in x.val }
    
    method prepend(x: Ref, v: Int) returns (y: Ref)
      requires LinkedList(x)
      ensures LinkedList(y) && head(y) == v
    {
      y := new(val, next)
      y.val := v
      y.next := x
      fold LinkedList(y)
    }

Note: `y := new(val, next)` models object initialisation by first havocing `y`
and then inhaling permissions to `y.val` and `y.next`.
