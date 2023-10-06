from FixedPointFormat import FixedPointFormat
from FloatingFormat import FloatingFormat
import sys


def start(*args):
    if len(args) == 3:
        if args[2][:2:] == "0x":
            if args[0] in ['h', 'f']:
                numA = FloatingFormat(args[0], args[2])
                numA.print()
            else:
                numA = FixedPointFormat(args[0], args[2])
                numA.print()
        else:
            print("nan")
    elif len(args) == 5:
        if args[2][:2:] == "0x" and args[4][:2:] == "0x":
            if args[0] in ['h', 'f']:
                numA = FloatingFormat(args[0], args[2])
                numB = FloatingFormat(args[0], args[4])
            else:
                numA = FixedPointFormat(args[0], args[2])
                numB = FixedPointFormat(args[0], args[4])
            operation = args[3]
            match operation:
                case "+":
                    numA.add(numB)
                case "-":
                    numA.sub(numB)
                case "*":
                    numA.mul(numB)
                case "/":
                    numA.div(numB)
                case _:
                    print("Unsupported operation")
        else:
            print("nan")
    else:
        print("Invalid number of arguments")


if __name__ == '__main__':
    form = sys.argv[1]
    if form in ['h', 'f'] or len(form) >= 3:
        start(*sys.argv[1::])
    else:
        print("Unsupported number form")
