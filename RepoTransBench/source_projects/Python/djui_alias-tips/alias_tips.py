def suggest_alias(command):
    """Suggest an alias for a given command."""
    if not command or not isinstance(command, str):
        return None
    if command == "list":
        return "ls"
    elif command == "remove":
        return "rm"
    elif command == "copy":
        return "cp"
    elif command == "move":
        return "mv"
    elif command == "make directory":
        return "mkdir"
    else:
        return None

def is_alias_recommended(command):
    """Return True if the command should have an alias, False otherwise."""
    common = ["list", "remove", "copy", "move", "make directory"]
    if command in common:
        return True
    return False