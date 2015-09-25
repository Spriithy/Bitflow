# Bitflow
The bitflow programming language


## Coding in Bitflow

### Getting started

First, when coding in Bitflow you should always keep in mind you are not using any serious programming language. This is a language mostly designed within 4 hours as a challenge.

If you still want to play with it, go ahead !

You will need a Python3 installation in order to interprete your Bitflow code. After getting all that working, you can start coding !

### New Program

Every Bitflow program must be contained in a `.bitflow` file. If not, the interpreter will abort the process.
Once you have your file setup, type the base program.

```txt
(a,b):{
  ... code here ...
};
```

Again, this is the base code without what the Bitflow interpreter can work. Between the two curly brackets, you can type your code !

### How it works

Basically, Bitflow lets you manipulate an array of 10 integers indexed from 0 to 9 (obviously). And that's all ! You can't manipulate specific type variables or anything ! Only integers ! But that said, you can still work with ASCII characters by printing them out. But we'll speak about that later on.

First things first, to be able to work with a given index of the array, you must specify it this way :

```txt
@<index>: ...
```

Where `<index>` is in range 0, 9 inclusive. When you have this, you can now jump to the next part !

### Knowing the useful things

The Bitflow programming language is a charcter-based language. This means, this language doesn't work with natural words. This said, I know let you discover the list of the 11 useful characters :

* `+`  lets you increment the current index by one
* `-`  lets you decrement the current index by one
* `*`  lets you  multiply the current index by two
* `/`  lets you   divide  the current index by two
* `^`  lets you set the current index under power two

* `!`  lets you set the current index value to 0
* `&`  lets you set the current index value to 64
* `$`  lets you set the current index value to 96

* `.`  lets you print the current value as is (Integer)
* `,`  lets you print the current value as an ASCII-character
* `_`  prints a whitespace
* `;`  is equivalent to `\n`

Now let's have a look a working example !

### Adding comments

If you ever want to write comments in your program, just add some at the **end of a line** (or single one).

```txt
@0:
  +++.   # This is a comment and this instructions should print ‘3’
```

#### Example

This example will simply compute and display some numbers on the screen

```txt
(a,b):{
  @0:
    +*^.;             # Should print ‘4’ on a single line
  @1:
    -*/.;             # This logicaly prints ‘-1’
};
```

A basic `Hello World !` program should be (most intuitive version)

```txt
(a,b):{
  @0:                     // We're working with index 0
    &                     // Let's set the value to be 64 (ascii caps letters)
      ++++++++,           // And go to ‘H’
    $                     // Let's go to non caps letters !
      +++++,,             // Go to ‘e’ and print it out !
      +++++++,,
      +++,
    _       // This prints a whitespace
    $
      ---------,
    $
      +++++++++++++++,
      +++,
      ------,
    $
      ++++,
    &/+,   // And this prints an exclamating point
};
```

### Let's go deeper !

Now that you know the basics of Bitflow, let me introduce you to loops ! The loops implemented in Bitflow are extremenly easy to understand ! They are forking like common `for` loops, without specifying neither variable as counter nor incrementation rule.

A Bitflow loop should look like this :

```txt
{<limit>:<code>}
```

Where :

* `<limit>` is the number of iteration of the loop. You can specify it like a normal calculus, i.e. using `+` or `-` or whatever !
* `<code>` is the code you want to apply to the current index

Let's see an example :

```txt
@0:            // Let's work in index 0
  ! {&:+.;}    // Yay ...
```

Let's see... This code will loop 64 times and will display each value on a single line !

### And even deeper !

Now you know how to implement a loop, let's see how to implement nested loops ! Bitflow doesn't natively support nested loops and this is why you can use the **deep-loop**. A deep-loop is a loop **inside** another loop. It is delimited by `[]` rather than `{}`. You can only use this loop inside another loop. Let's see how it works using the example of the multiplication.

```txt
@0:              // again, index 0...
  {&: [&:+] }.;  // hehe !
```

This simple code computes `& * &` that is to say `64 * 64 = 4096`. Of course, you can use several different nested loops side by side ! For example, `{$: [&: +] [$: -] }` is correct and working code that outputs `-3072`.

### Reffering to other indexes values

Of course you can refer to existing index values ! You can do it extremely easily by typing the index of the array index you want to set !

```txt
@0:&^
@1:0.;
```

This code will output the value of index `0`.

### Using command line arguments

Have you ever wondered what did `a` and `b` stand for ? Well, they represent the different values you can pass to the program when compiling it. If not specified, those values are considered null (0). You can use them by typing either `a` or `b` in your code. Those values can be used as loop iteration limit.

You are now ready for Bitflow !





# License

```txt
The MIT License (MIT)

Copyright (c) 2015 | Theophile Dano, Spriithy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
