# Integrator
This is a symbolic integrator based on James Slagle's 1961 thesis.
The goal of this project is to solve integrals symbolically
in an accessible manner.
The machine will work to solve the integration problem, and will share its
thoughts and methods with you.

## Demo
You can try the integrator for yourself [here](http://milessteele.com:5000).

## Getting Your Hands Dirty

After playing with the integrator, you might
be inclined to change some of the ways in which it operates.

Running the integrator locally will enable you to mess
with the code and change how it works.
You can experiment with different ways
of presenting how it does the integration,
or try adding your own strategies to make it smarter,
or anything you can think of.

To get more ideas about what to fiddle with, 
you may want to read the _Parts of the Machine_
section below to get a sense for how the pieces
of the integrator fit together and decide
which one to tackle first.

Here are a few instructions to get you started
running the integrator locally.

### Installing Requirements
Before running the integrator, you will need a few things
set up first.

- __git__ will enable you to track changes that you make
  and submit pull requests to add features for everyone to see.
  This is optional, you could just download a
  zip to get started quickly.
- __python__ comes already installed on many computers, you will
  need this to run the integration engine and webserver.
- __flask__ is a web framework for python which serves
  the web interface. You can install it via
  [pip](http://pip.readthedocs.org/en/latest/installing.html)
  using
  [these instructions](http://flask.pocoo.org/)

### Running
After you have downloaded the `integrator` directory
somewhere go ahead and open up a terminal and
`cd` into the directory:

    $ cd /where/did/you/put/the/integrator

Then run :

    $ python web.py

If all goes well, you should now see something like:

     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Great, you've started the integrator web server
on your computer on port 5000.
Visit [http://localhost:5000](http://localhost:5000)
to see the web interface to your local copy of the integrator.

You can now start editing the code, be sure to refresh
the web page to see your changes take effect.

## Parts of the Machine

### Web Front-End
This is the part of the program that you see when you visit
the website.

It is a simple web page which asks the python server
to solve integration problems for you and then displays
the results.

The html is in
`templates/solver.html`
and the javascript that talks to the server is in
`static/js/solver.js`.

### Web Server
The web server receives requests to solve expressions from
the web page and passes them on to the underlying layers
of the program before passing the result back to the web page.

### Parser
The web server sends input from the web interface to the parser
which lives in `parseintg.py`.

Right now, the parser is a horrible tangled mess, so it
would probably be best at this point to think of it as a black
box which converts text like `int x + 1 dx` into a
tree of expressions representing that expression.

That particular example, `int x + 1 dx`,
would be converted into something like:

    Integral(
      Sum(
        Variable("x"), Number(1)
      ),
      Variable("x"))

### Elements
The parser parses the input string into elements
like `Number`, `Sum`, `Product`, and `Integral`.
These types of expressions are implemented in `elements.py`.

Each type of expressions is a kind of `Expression`
which is a class that knows how to simplify itself a bit.

### Solver
The elements forming the expression to be solved
are then passed on to `solver.py` which does
the meat of the integration.

The solver is responsible for coralling expressions
into their simplified form, and then trying integration
strategies to solve the integrals in the expression.

You can run the solver by itself from the command line.
But the output is not very pretty as it is meant for the web.

    $ python solver.py
    Enter a string to be integrated.
    Just press enter to integrate 'int 3 x / 4 dx'
    -> 
    I will attempt to solve \( \int{\frac{3 \cdot x}{4}}\;dx \).
    \( \int{\frac{3 \cdot x}{4}}\;dx \) is an integral.
    Which of my strategies are applicable to this integral?
    The "integral with a constant divisor" rule <div class="strategy-icon"><div class="strategy-code"><pre>class ConstantDivisor(IntegrationStrategy):<br>  description = "integral with a constant divisor"<br><br>  @classmethod<br>  def applicable(self, intg):<br>    exp = intg.simplified().exp<br>    return (exp.is_a(Fraction)<br>      and (is_constant(exp.denr, intg.var)))<br><br>  @classmethod<br>  def apply(self, intg):<br>    exp = intg.simplified().exp<br>    return Product(Fraction(Number(1), exp.denr), Integral(exp.numr, intg.var))<br></pre></div></div> is applicable, I will try it.
    I will attempt to solve \( \frac{1}{4} \cdot \int{3 \cdot x}\;dx \).
    \( \frac{1}{4} \cdot \int{3 \cdot x}\;dx \) is a product. I will solve the two sub-problems and then multiply the results.
    [<sublogger.SubLogger object at 0x7f3ff3543490>, <sublogger.SubLogger object at 0x7f3ff3543510>]
    I will multiply the results of the sub-problems back together to get \( \frac{1}{4} \cdot 3 \cdot (\frac{1}{2} \cdot {x}^{2} + C) \).


### Strategies
All of the strategies that the solver knows how to
try are in `strategies.py`

Here is an example of a strategy.
This strategy takes a sum inside of an integral
and ouputs a new equivalent expression which
is the sum of two integrals.

```python
# int x + x^2 dx = int x dx + int x^2 dx
class DistributeAddition(IntegrationStrategy):
  description = "integral of sums to sum of integrals"

@classmethod
def applicable(self, intg):
  exp = intg.simplified().exp
    return exp.is_a(Sum)

  @classmethod
  def apply(self, intg):
    exp = intg.simplified().exp
    new_expr = Sum(Integral(exp.a, intg.var), Integral(exp.b, intg.var))
    return add_integration_constant(new_expr, intg)
```

Applying these strategies as they become applicable
will solve a surprising number of integrals.
