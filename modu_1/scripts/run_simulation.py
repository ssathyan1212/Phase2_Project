import sys
from main import run

if __name__ == "__main__":
    # default mode
    mode = "normal"

    # read mode from command line
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    run(mode)
