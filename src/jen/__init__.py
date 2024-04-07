"""
Jen: A Test Case Generator

Reads a TOML file with test case configurations, generates tests
and pipes them to a test program and reference program.

@author: Fares Badr
@date: 2024-04-07
"""

import tomllib
import random
import subprocess


class InputVariable():
    def __init__(self, varname):
        self.name = varname
        self.value = None
        self.props = {}

    def render(self) -> str:
        self.set_value()
        return str(self.value)

    def reset_value(self):
        self.value = None

    def set_value(self):
        """ Randomizes value according to rules given by the variable properties """
        if 'type' not in self.props:
            raise Exception("Variable type not specified.")
        if self.props['type'] == 'int':
            self.value = random.randint(
                self.get_property('min'), self.get_property('max'))
        elif self.props['type'] == 'float':
            self.value = random.uniform(
                self.get_property('min'), self.get_property('max'))
        elif self.props['type'] == 'str':
            k = random.randint(self.get_property(
                'min'), self.get_property('max'))
            self.value = "".join(random.choices(self.props['allowed'], k=k))
        else:
            raise Exception("Unimplemented type.")

    def get_property(self, prop):
        """ Read a property, taking into account default values and resolving variables into values """
        prop_val = self.props[prop]
        if (type(prop_val) == str):
            return StressTester.var_dict[prop_val].value
        else:
            return prop_val


class InputGroup():
    def __init__(self, props, ind=0):
        self.out_list = []  # Used to create an output string
        self.props = props
        self.grp_num = 1  # Counter used to name child groups
        self.start_ind = ind
        self.end_ind = len(StressTester.config['in'])
        self.parse(ind)

    def parse(self, ind):
        """ parse the input string from a starting index """
        while ind < self.end_ind:
            char = StressTester.config['in'][ind]
            if char.isalpha():
                self.add_variable(char)
            elif char == '{':
                ind = self.add_group(ind)
            elif char == '}':
                self.end_ind = ind
                return  # Group is done
            else:
                self.out_list.append(char)
            ind = ind + 1

    def add_variable(self, var):
        """ 
        If variable does not exist, create it. 
        Set variable's properties from the configuration file.
        Then add it to the output list. 
        """
        if (var not in StressTester.var_dict):
            StressTester.var_dict[var] = InputVariable(var)
        input_variable = StressTester.var_dict[var]
        if (var in StressTester.config):
            input_variable.props.update(StressTester.config[var])
        self.out_list.append(input_variable)

    def add_group(self, ind):
        """
        Reads the input string starting from a given index
        until we reach a '}' character, assuming no nested groups. 

        return the index of the '}' character closing that group.
        """
        grp_props = self.props[str(self.grp_num)]
        child_grp = InputGroup(grp_props, ind + 1)
        self.out_list.append(child_grp)
        self.grp_num = self.grp_num + 1
        return child_grp.end_ind

    def reset_value(self):
        for out_item in self.out_list:
            if type(out_item) == str:
                continue
            out_item.reset_value()

    def get_count(self):
        """ Return (int) the number of times the group should repeat. """
        count = self.props.get('count', 1)
        if type(count) == str:
            return int(StressTester.var_dict[count].value)
        else:
            return int(count)

        return int(count.value)

    def render(self):
        """ Return a string with newly set values for the group """
        # update values for all variables
        delimiter = self.props.get('delimiter', ' ')
        count = self.get_count()
        render_list = []  # list of strings
        for _ in range(count):
            self.reset_value()
            for out_item in self.out_list:
                if type(out_item) == str:
                    render_list.append(out_item)
                else:
                    render_list.append(out_item.render())
        return delimiter.join(render_list)


class StressTester(InputGroup):
    config = {}
    var_dict = {}

    def __init__(self, config_file):
        with open(config_file, 'rb') as f:
            StressTester.config = tomllib.load(f)
            if ('in' not in self.config):
                raise Exception("in variable missing from configuration.")
        # No delimiter for the main group
        StressTester.config['delimiter'] = ''
        super().__init__(props=StressTester.config)

    def run(self, test_fn, ref_fn, out_fn=None):
        test_cnt = 1
        while True:
            test_str = self.render()
            try:
                test_ps = subprocess.run(
                    test_fn, input=test_str, stdout=subprocess.PIPE, shell=True, text=True, check=True)
                ref_ps = subprocess.run(
                    ref_fn, input=test_str, stdout=subprocess.PIPE, shell=True, text=True, check=True)
            except Exception:
                break  # Do not continue if calling the programs fails
            print(test_cnt, end='\r')
            test_cnt = test_cnt + 1
            if (ref_ps.stdout != test_ps.stdout):
                print(f"Found difference: test #{test_cnt}")
                break

        if (out_fn is None):
            out_fn = 'test_' + str(test_cnt)
        with open(out_fn, 'w') as f:
            f.write(test_str)

    def single_run(self, out_fn=None):
        test_str = self.render()
        if (out_fn is None):
            out_fn = 'test'
        with open(out_fn, 'w') as f:
            f.write(test_str)
