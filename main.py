from FixedPointFormat import FixedPointFormat
from PrecisionFormat import PrecisionFormat
import sys


def use(*args):
    if len(args) == 3:
        if args[0] in ['h', 'f']:
            numA = PrecisionFormat(args[0], args[2])
            numA.print()
        else:
            numA = FixedPointFormat(args[0], args[2])
            numA.print()
    elif len(args) == 5:
        if args[0] in ['h', 'f']:
            numA = PrecisionFormat(args[0], args[2])
            numB = PrecisionFormat(args[0], args[4])
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
                if args[0] not in ['h', 'f']:
                    print('Operation not supported')
                    sys.exit(0)
                numA.div(numB)
            case _:
                print("Unsupported operation")
    else:
        print("Invalid number of arguments")


if __name__ == '__main__':
    form = sys.argv[1]
    if form in ['h', 'f'] or len(form) >= 3:
        use(*sys.argv[1::])
    else:
        print("Unsupported number form")
        sys.exit(0)
