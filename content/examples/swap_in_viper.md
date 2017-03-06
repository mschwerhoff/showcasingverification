Tags: swap, Viper, Permissions
Title: Swap in Viper
Date: 2017-03-05

Two Viper encodings of a method that swaps the values of two fields `x.f` and `y.f`.

    :::text
    field f: Int

    method swap1(x: Ref, y: Ref)
      requires acc(x.f) && (x != y ==> acc(y.f))
      ensures  acc(x.f) && (x != y ==> acc(y.f))
      ensures  x.f == old(y.f)
      ensures  y.f == old(x.f)
    {
      var tmp: Int := x.f
      x.f := y.f
      y.f := tmp
    }

    method swap2(x: Ref, y: Ref)
      requires forall r: Ref :: r in Set(x, y) ==> acc(r.f)
      ensures  forall r: Ref :: r in Set(x, y) ==> acc(r.f)
      ensures  x.f == old(y.f)
      ensures  y.f == old(x.f)
    {
      var tmp: Int := x.f
      x.f := y.f
      y.f := tmp
    }

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula
eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient
montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque
eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo,
fringilla vel, aliquet nec, vulputate eget, arcu.
