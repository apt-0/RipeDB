# In utils/helper.py

def show_general_help():
    help_text = """
    RipeDB - A tool for performing queries and analysis on RipeDB

    Usage:
        ripedb [command] [options]

    Commands:
        query   Executes a query on RipeDB.
        help    Shows this help message or details about a specific command.

    For more information on a specific command, use:
        ripedb help [command]
    """
    print(help_text)
