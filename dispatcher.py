"""
"""
import argparse
import sys
#import os
#import importlib

from command import Command

class DuplicateKeyError(Exception):
    """
    """

    def __init__(self, message, key):
        """
        """
        super(DuplicateKeyError, self).__init__(message)
        self.key = key


def merge_command_lists(default, extensions):
    """
    @deprecated: hodor
    """
    for command in extensions:
        if not command in default:
            default.append(command)
        else:
            raise DuplicateKeyError('Duplicate Key detected', command.command)
    return default


def merge_commands(dicts, duplicate_error=True):
    """merge any number of dictionaries. strip away duplicate keys. optionally
    raise error on duplicates

    :param list dicts: a list of all dictionaries to merge
    :param bool duplicate_error: if True raise error on duplicate keys
    :raises DuplicateKeyError: if duplicate_error is true and duplicate key exists
    :returns dict: merge result
    """
    result = {}
    if duplicate_error:
        for d in dicts:
            for k, v in d.items():
                if not k in result:
                    result[k] = import_command(v)
                else:
                    raise DuplicateKeyError('Command duplicate detected!', k)
    else:
        result = {k: import_command(v) for d in dicts for k, v in d.items()}

    return result

def build_command_dict(default, extensions):
    """
    """
    command_dict = {}

    # filter duplicate commands from default command list
    for command in default:
        try:
            command_dict[command.command] = command
        except KeyError:
            raise DuplicateKeyError('Duplicate Key detected', command.command)

    # add additional commands and check for duplicates
    for command in extensions:
        if not command in default:
            try:
                command_dict[command.command] = command
            except KeyError:
                raise DuplicateKeyError('Duplicate Key detected', command.command)
        else:
            raise DuplicateKeyError('Duplicate Key detected', command.command)

    return command_dict


class ArgumentParser(object):
    """
    """

    def __init__(self, dispatcher):
        """
        """
        self._subparser = argparse.ArgumentParser()

        positional_args = ''
        for cmd_key, cmd_obj in dispatcher._commands.items():
            positional_args = positional_args + '    {}    {}\n'.format(
                                cmd_obj.command, cmd_obj.description)

        self._usage = (
            '{} ({})\n'
            '\n'
            'usage: {} [-h] <command> [<args>] \n'
            '\n'
            'positional arguments:\n'
            '{}'
            '\n'
            'optional arguments:\n'
            '   -h, --help      show this help message and exit'
            '').format(dispatcher._name, dispatcher._version, dispatcher._cmd, positional_args)

        setattr(self._subparser, 'format_help', lambda: print(self._usage))



    def print_help(self):
        print(self._usage)

    def add_argument(self, *args, **kwargs):
        """
        """
        return self._subparser.add_argument(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        """
        """
        return self._subparser.parse_args(*args, **kwargs)


class CommandDispatcher(object):
    """
    """
    _default_commands = []
    _name = 'Subcommander'
    _cmd = 'subcmd'
    _version = '1.0'

    def __init__(self, extensions=None):
        """
        """
        # merge default commands and custom app commands
        if extensions is not None:
            try:
                self._commands = build_command_dict(self.__class__._default_commands, extensions)
            except DuplicateKeyError as err:
                print('Command Error!'
                    'Command duplication detected! Could not initialize custom commands.'
                    'Command \'{}\' already exists!'.format(err.key))
                exit(1)
        else:
            self._commands = build_command_dict(self.__class__._default_commands, [])

        # build usage text
        # usage = '{} <command> [<args>]\n'.format(self.__class__._base_command)
        # for cmd_key, cmd_obj in self._commands.items():
        #     usage = usage + '    {}    {}\n'.format(cmd_obj.command, cmd_obj.description)

        # dispatch commands
        parser = ArgumentParser(self)
        parser.add_argument('command', help='the command to run')

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        arguments = parser.parse_args(sys.argv[1:2])
        if not arguments.command in self._commands:
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # # use dispatch pattern to invoke method with same name
        # getattr(self, args.command)()
