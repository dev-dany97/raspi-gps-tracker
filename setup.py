# version: 1.0.0
# _*_ coding: utf-8 _*_
""" Setup module for package creation
"""

from setuptools import setup


PIP_REQUIREMENTS_FILE = 'requirements.txt'

MODULE_TYPE = 'script'


def get_requirements(requirements_file):
    """ Get the "non meta" requirements from the requirements file. That way we only have to track them in one location
        (the requirements.txt file), instead of there and in this file. The file is expected to have to following form:
        Two blocks of depencies, each start with a '# <comment>' line:

        # version: 1.0.2
        # dependencies of this package (they are also used in setup.py)
        pyserial>=3.4
        int_tfc_base_lib>=0.2.0
        # this file also contains pip "meta" requirements (packages which are needed
        to build and test this package, not used in setup.py)
        pep8
        pylint
        coverage
        sphinx
        wheel
    """
    LS = '\n'
    with open(requirements_file, 'rt') as rf:
        all_lines = rf.read()
    non_meta_deps = []
    in_dependency_block = False
    skip_comments = 2  # quantity of comments at the start of the file
    for line in all_lines.split(LS):
        sline = line.strip()
        if not sline:
            continue
        if sline.startswith('#'):
            skip_comments -= 1
            if in_dependency_block:  # pylint: disable=bad-option-value, no-else-break
                # marker for the second block, meta dependencies, block -> done
                break
            elif skip_comments == 0:
                # first block -> every non-empty line after this one is a dependency
                in_dependency_block = True
        elif in_dependency_block:
            # store the line
            non_meta_deps.append(sline)
    return non_meta_deps


setup(
    name='dany_raspi_gps_tracker',
    version='1.0.0',
    classifiers=['Development Status :: 3 - Alpha'],
    # classifiers=['Development Status :: 4 - Beta'],
    # classifiers=['Development Status :: 5 - Production/Stable'],
    author='daniel.mohles',
    author_email='daniel_mohles@outlook.de',
    description='GPS tracker for Raspberry Pi with SIM868 GSM/GPRS/GNSS HAT and Ubidots upload',
    long_description=open('README.md').read(),
    install_requires=get_requirements(PIP_REQUIREMENTS_FILE),
    scripts=['src/dany_raspi_gps_tracker']
)
