Jen is a configurable test case generator for competitive programming.
The format of the test cases is specified in a TOML configuration file.
Supplied with a test and a reference program, Jen will generate test cases and supply them to the test and ref programs
through standard input and compare the outputs of the two programs. If a difference in outputs is found, the test case is saved to a file.

install with `pip install cp-jen`
then run `jen <config.toml> <test_program> <reference_program>`

The specifications for the configuration file are detailed below.

- A variable called "in" is required. It is a string defining the input variables.

"in" rules:
- Any latin script letter is considered a variable. (case sensitive)
- braces {} define a group. Groups are repeating sections of input.
- The first group is called '1'. The second group is '2', ... etc.
- group [1.1] is the first group within group 1.
- Any other character is kept as-is when generating inputs.

Each variable has a type. The type of a variable can be inferred from its name
or set explicitly in the variable configurations.
Each type has allowed properties and default values for those properties, listed below.

*Types*
int:
    - default names: (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,u,v,w)
    - min: 0
    - max: 1000

string:
    - default names: (s,t)
    - min: 0
    - max: 1000

float:
    - default names: (x,y,z)
    - min: 0.0
    - max: 1000.0

group:
    - count: 'n'
    - delimiter: " "

