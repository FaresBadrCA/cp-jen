# 📚 About 

Jen is a configurable test case generator for competitive programming.
The format of the test cases is specified in a TOML configuration file. 

# 🔌 Installation

Python version >=3.11 is required to install the python library. Install with:

`pip install cp-jen`

This will create a `jen` script in your python `bin` folder.
To call this script from anyware, ensure the python `bin` folder is in your PATH.

# 💼 Usage

Calling `jen` with a configuration file creates a test case and saves it in the current directory.

`jen config.toml`

To stress test your program, run `jen` with two additional arguments:

`jen config.toml ./tst ./ref`

Jen will continuously generate test cases and pipe them to the test and reference program's standard input.
The outputs from both programs are compared until a test case that generates different outputs is found.

# ⚙️  Configuration

The configuration is a TOML file. Examples of input configurations for past problems are in the examples folder.

## Example Configuration
As an example, we look at test cases for Atcoder contest [ABC346, problem D](https://atcoder.jp/contests/abc346/tasks/abc346_d).

```toml
in = """
N
S
{C}"""

[N]
type = 'int'
min = 2
max = 20

[S]
type = 'str'
allowed = ['0','1']
min = 'N'
max = 'N'

[C]
type = 'int'
min = 1
max = 1000000000

[1]
delimiter = ' '
count = 'N' 
```

Each test case will have an integer N, followed by a string of zeros and ones of size N, and finally N integers between 1 and 1,000,000,000 separated by spaces.

## jen.toml Specifications 

A variable called "in" is required. It is a string defining the input variables.

*in* rules:
- Any latin script letter is considered a variable (case sensitive).
- braces {} define a group. Groups are repeating sections of input.
- The first group is called '1'. The second group is '2', ... etc.
- group [1.1] is the first group within group 1.
- Any other character is kept as-is when generating inputs.

Each variable has a type. The type of a variable can be inferred from its name
or set explicitly in the variable configurations.
Each type has allowed properties and default values for those properties, listed below.

*Types*
- **int**:
    - default names: (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,u,v,w)
    - min: 0
    - max: 1000

- **string**:
    - default names: (s,t)
    - min: 0
    - max: 1000

- **float**:
    - default names: (x,y,z)
    - min: 0.0
    - max: 1000.0

- **group**:
    - count: 'n'
    - delimiter: " "

