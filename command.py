"""
"""

class CommandMeta(type):
    """
    """
    @property
    def command(self):
        return self._command

    @property
    def description(self):
        return self._description

    @property
    def hidden(self):
        return self._hide


class Command(metaclass=CommandMeta):
    """
    """
    _command = ''
    _description = ''
    _hide = False
