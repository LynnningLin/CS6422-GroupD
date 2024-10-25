class Colours():
    """
    -Always Place Colours.RESET when finished print statement
    -ANSI Colours Inherits
    """
    RESET = "\033[0m"
    RED = "\u001b[31m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"



# Palette Test
# print(f"{Colours.GREEN}This text is green.{Colours.RESET}")
# print(f"{Colours.BLUE}This text is blue.{Colours.RESET}")
# print(f"{Colours.YELLOW}This text is yellow.{Colours.RESET}")
# print(f"{Colours.CYAN}This text is cyan.{Colours.RESET}")
# print(f"{Colours.MAGENTA}This text is magenta.{Colours.RESET}")
