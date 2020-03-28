# version: 1.0.0
""" Custom pylint checker
"""

import re
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class DocstringBlanklinesChecker(BaseChecker):
    """ Docstring checker
    """
    __implements__ = IAstroidChecker

    name = 'docstring-blank-line'
    # priority = -1
    msgs = {'C9000': ('Blank line expected before parameter block in %s docstring.',
                      'non-docstring-blank-line',
                      'A parameter block in a docstring should be preceded by a blank line.')}
    # options = ()

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self.__parameter_block_regex = re.compile(r'^\s*:(?:raise|raises|param|type|return|rtype|yields)')

    def __is_valid_docstring(self, docstring):
        """ Check if the given docstring is "valid"

        :param docstring: The docstring
        :type docstring: String
        :return: True if the docstring is valid, False otherwise
        :rtype: Boolean
        """
        last_line_was_blank = False
        for line in docstring.split('\n'):
            sline = line.strip()
            if not sline:
                last_line_was_blank = True
            else:
                if self.__parameter_block_regex.match(sline):
                    return last_line_was_blank
                last_line_was_blank = False
        return True

    def __check_docstring(self, node, context):
        """ Check the docstring in the given context

        :param node: The nodes whos docstring should be checked
        :type node: AST node
        :param context: The context of the docstring
        :type context: String
        """
        docstring = node.doc
        if docstring and not self.__is_valid_docstring(docstring):
            self.add_message('non-docstring-blank-line', node=node, args=(context,))

    def visit_functiondef(self, node):
        """ Called for each function definition
        """
        self.__check_docstring(node, 'function')

    def visit_classdef(self, node):
        """ Called for each class definition
        """
        self.__check_docstring(node, 'class')


def register(linter):
    """ Register all custom checkers
    """
    linter.register_checker(DocstringBlanklinesChecker(linter))
