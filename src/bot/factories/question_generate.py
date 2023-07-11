import os
import sys

module_path = os.path.abspath(os.getcwd() + "../../../../")
if module_path not in sys.path:
    sys.path.append(module_path)


if __name__ == "__main__":
    from src.bot.factories.question_factories import read_arg

    read_arg()
