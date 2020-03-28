# version: 1.0.0
""" Helper script which runs pylint over the given source code. It also allows to configure special /
different options for specific folders.
"""

import os
import sys
import fnmatch
import subprocess
from collections import OrderedDict

# the pylint binary
PYLINT = 'pylint'
PYLINT_CUSTOM_PLUGINS_PATH = './pylint_modules'
PYLINT_CUSTOM_PLUGINS = ['custom_pylint_check', 'pylint.extensions.docparams']

# linter options per file or directory, None as value means to skip the matching objects
file_specific_options = OrderedDict()
file_specific_options['./build/*'] = None
file_specific_options['./docs/*'] = None
file_specific_options['./test/*'] = None
file_specific_options['./venv/*'] = None

# default
file_specific_options['*'] = ['--msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"',
                              '--max-line-length=120',
                              '--disable=C0103,C1001,W0703,W0511,W0603,W0403,R0201,R0903,R0902,R0913,W0223,R0914', ]

# disabled codes / warnings / remarks so far (we have to discuss what we want)
# C0103: Invalid name.
# C1001: Old-style class defined.
# W0703: Catching too general exception.
# W0511: FIXMEs and TODOs in the code.
# W0603: Using the global statement.
# R0201: Method could be a function.
# W0403: Relative import.
# R0903: Too few public methods.
# R0902: Too many instance attributes
# R0913: Too many arguments
# W0223: Method 'SomeMethod' is abstract in class 'SomeClass' but is not overridden
# R0914: Too many locals


# see also http://pylint-messages.wikidot.com/all-codes for a list of all codes and warnings
# (unfortunately it seems that this list is not complete)


# preprocess the options
_file_options = OrderedDict()
for k, v in list(file_specific_options.items()):
    fixed_key = os.path.sep.join(k.split('/'))
    _file_options[fixed_key] = v


def get_options_for_path(filepath):
    """ extract the options for the given filepath from the options dictionary
    """
    for matchpath, options in list(_file_options.items()):
        if fnmatch.fnmatch(filepath, matchpath):
            return options
    return None


def main():
    """ main function which fetches all files and then run the pylint against it,
    with the specific options for the given path
    """
    error_code = 0
    # walk over all files and run pylint against them
    for root, _, files in os.walk('.'):
        for filename in files:
            if not filename.endswith('.py'):
                # we are only interested in python files
                continue
            filepath = os.path.join(root, filename)
            ploptions = get_options_for_path(filepath)
            if ploptions is None:
                # skip
                continue
            # print '* running pylint against "%s" with options %s' % (filepath, ploptions)
            callargs = [PYLINT, '--load-plugins=%s' % ','.join(PYLINT_CUSTOM_PLUGINS)]
            callargs.extend(ploptions)
            callargs.append(filepath)
            # now run pylint against the file
            try:
                with open(os.devnull, 'w') as devnull:
                    env = dict(os.environ, PYTHONPATH=PYLINT_CUSTOM_PLUGINS_PATH)
                    subprocess.check_output(callargs, stderr=devnull,
                                            env=env)  # pylint: disable=unexpected-keyword-arg
            except subprocess.CalledProcessError as e:
                error_code = 1
                print(e.output.decode('ascii', 'ignore'))  # pylint: disable=superfluous-parens
            sys.stdout.write('.')
            sys.stdout.flush()
    return error_code


if __name__ == '__main__':
    sys.exit(main())
