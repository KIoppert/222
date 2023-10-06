def longDivision(dividend, divider):
    rest, i = 0, 0
    ans = ''
    digits = str(dividend)
    isFraction = False
    if dividend < divider:
        ans = '0'
    while i < len(digits):
        d = int(digits[i])
        d += rest * 10
        whole = d // divider
        if whole or len(ans) > 1 or isFraction:
            rest = d % divider
            ans += str(whole)
        else:
            rest = d
        if (i == len(digits) - 1) and not isFraction:
            if d > 0:
                ans += ''
            ans += '.'
            digits += '00000'
            isFraction = True
        i += 1
    return ans
def printNumber(answer, A, B):
    answer = checkOverflow(answer, A, B)
    res = ""
    if answer < 0:
        answer *= -1
        res += '-'
    answer = answer * 1000
    answer = answer // 2 ** B
    res += f'{answer // 1000}.{"0" * (3 - len(str(answer % 1000)))}{answer % 1000}'
    print(res)

def checkOverflow(number, A, B):
    if number < -(2 ** (A + B)) // 2:
        number += 2 ** (A + B)
    if number >= 2 ** (A + B) // 2:
        number -= 2 ** (A + B)
    return number


class FixedPointFormat:
    binNumber = ""
    A = 0
    B = 0
    mapForTranslation = {"0": "0000",
                         "1": "0001",
                         "2": "0010",
                         "3": "0011",
                         "4": "0100",
                         "5": "0101",
                         "6": "0110",
                         "7": "0111",
                         "8": "1000",
                         "9": "1001",
                         "a": "1010",
                         "b": "1011",
                         "c": "1100",
                         "d": "1101",
                         "e": "1110",
                         "f": "1111",
                         }

    def __init__(self, A_B, number):
        for i in number[2::]:
            self.binNumber += self.mapForTranslation[i.lower()]
        self.A, self.B = map(int, A_B.split('.'))
        if self.A + self.B < len(self.binNumber):
            self.binNumber = self.binNumber[len(self.binNumber) - self.A - self.B:]
        self.binNumber = "0" * (self.A + self.B - len(self.binNumber)) + self.binNumber
        self.decNumber = int(self.binNumber, 2) - (0 if self.binNumber[0] != '1' else 2 ** (self.A + self.B))


    def print(self):
        result = "-" * (self.decNumber < 0) + longDivision(abs(self.decNumber), 2 ** self.B)[:-2:]
        print(result)

    def add(self, secondNumber):
        answer = self.decNumber + secondNumber.decNumber
        printNumber(answer, self.A, self.B)

    def sub(self, secondNumber):
        answer = self.decNumber - secondNumber.decNumber
        printNumber(answer, self.A, self.B)

    def mul(self, secondNumber):
        answer = self.decNumber * secondNumber.decNumber
        result = abs(answer) // 2 ** self.B
        result = result % (2 ** (self.A + self.B))
        printNumber(result * (-1 if answer < 0 else 1), self.A, self.B)

    def div(self, secondNumber):
        if secondNumber.decNumber != 0:
            answer = ((abs(self.decNumber) * 2 ** 32) // abs(secondNumber.decNumber))
            answer //= 2 ** (32 - self.B)
            answer = answer % 2 ** (self.A + self.B)
            printNumber(answer * (-1 if (self.decNumber * secondNumber.decNumber) < 0 else 1), self.A, self.B)
        else:
            print("error")
