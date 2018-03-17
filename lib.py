"""
"""

def import_command(command):
    """import a command by its name
    """
    return importlib.import_module('appconf.commands.'+command.lower()+command)
