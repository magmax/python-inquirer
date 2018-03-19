# -*- coding: utf-8 -*-
import os
import sys
import glob
import math
import subprocess

from ._text import Text
from inquirer import errors

from readchar import key


def get_completion(comp_prefix, reduce_to_common_prefix=True):
    """
    Gets a filepath completion based on the current input and the results
    returned by the glob module.

    If only one possible option exists, returns that option. If multiple options exists,
    returns the longest common prefix among the options, unless reduce_to_common_prefix
    is set to False, in which case it returns all options as a list of strings.

    :param comp_prefix: str Current input
    :param reduce_to_common_prefix: bool, Whether to reduce multiple options to the longest
                                          common prefix
    :return: bool, (str or list) Whether a completion was found, and the completion or list
                                 of completions
    """
    options = glob.glob(comp_prefix.replace(r'\ ', ' ') + '*')
    if len(options) == 1:
        completion = options[0]
        if os.path.isdir(completion):
            completion += os.path.sep
        return completion != comp_prefix, completion
    elif len(options) > 1:
        if not reduce_to_common_prefix:
            return None, options
        completion = os.path.commonprefix(options)
        return completion != comp_prefix, completion
    return False, comp_prefix


def show_completion_hint(current, terminal_width, is_unix=True):
    """
    Shows all possible completions given the current input.

    On Unix, options will be piped to the more program so that if there are many possible
    values the user can scroll through them. On Windows, the whole list is dumped no matter
    the size because it's too complicated to make piped output work.

    :param current: str Current input
    :param terminal_width: int Width of the terminal, used for layout calculation
    :param is_unix: bool Whether this is a Unix terminal
    """
    # Get possible completion options, make sure there was more than one available option
    _, options = get_completion(current, reduce_to_common_prefix=False)
    if not isinstance(options, list):
        return

    # Sort options alphabetically, add trailing slashes to directories
    sorted_options = sorted([
        os.path.basename(option) + (os.path.sep if os.path.isdir(option) else '')
        for option in options
    ], key=lambda op: op.lower())

    # Layout completion options
    longest_option = max(*[len(op) for op in sorted_options]) + 2  # 2 is for padding
    n_option_cols = int(terminal_width / float(longest_option))
    n_option_rows = int(math.ceil(len(sorted_options) / float(n_option_cols)))
    option_rows = [''] * n_option_rows
    for i, option in enumerate(sorted_options):
        row_i = i % n_option_rows
        option_rows[row_i] += option + (' ' * (longest_option - len(option)))

    print()  # To move prompt down
    if is_unix:
        options_matrix = '\n'.join(option_rows)
        _echo = subprocess.Popen(['echo', '{}'.format(options_matrix)], stdout=subprocess.PIPE)
        subprocess.call(['more'], stdin=_echo.stdout)
        _echo.wait()
    else:
        # On Windows just print it out no matter how big the list is
        for row in option_rows:
            print(row)


class Path(Text):
    def __init__(self, *args, **kwargs):
        super(Path, self).__init__(*args, **kwargs)
        self.show_options = False

    def process_input(self, pressed):
        if pressed == '\t':
            self.current = os.path.expanduser(self.current)
            _completed = False
            if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
                # Window style paths
                if self.show_options:
                    # Show options if this is the second consecutive TAB without a completion
                    show_completion_hint(self.current, self.terminal.width, is_unix=False)
                # TODO Support for Windows
            else:
                # Unix style paths
                if self.show_options:
                    # Show options if this is the second consecutive TAB without a completion
                    show_completion_hint(self.current, self.terminal.width)
                elif self.question.midtoken_completion and self.cursor_offset > 0:
                    # User completed path somewhere in the middle of the input
                    _completed, completion = get_completion(self.current[:-self.cursor_offset])
                    self.current = ''.join((
                        completion,
                        self.current[-self.cursor_offset:]
                    ))
                elif self.cursor_offset == 0:
                    # Normal end-of-line completion
                    _completed, self.current = get_completion(self.current)

            self.show_options = not _completed
        elif pressed in {key.CR, key.LF, key.ENTER}:
            raise errors.EndOfInput(self.current.strip().replace(' ', r'\ '))
        else:
            # Only any key press except TAB, reset showing options
            self.show_options = False
            super(Path, self).process_input(pressed)
