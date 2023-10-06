from FixedPointFormat import FixedPointFormat


def IsNumberSpecial(self):
    return self.isINF or self.isZero or self.isNAN


class FloatingFormat:
    binNumber = ""
    isNAN = False
    isINF = False
    isNegativeINF = False
    isZero = False
    isDenorm = False

    def __init__(self, form, number):
        if form == 'h':
            self.bitForExp = 5
            self.bitForMant = 10
        elif form == 'f':
            self.bitForExp = 8
            self.bitForMant = 23
        number = "0" * ((self.bitForExp + self.bitForExp + 1) // 4 - len(number[2::])) + number[2::]
        for i in number:
            self.binNumber += FixedPointFormat.mapForTranslation[i.lower()]
        if len(self.binNumber) > self.bitForExp + self.bitForMant:
            self.binNumber = self.binNumber[len(self.binNumber) - self.bitForExp - self.bitForMant-1::]
        self.binNumber = '0' * ((self.bitForExp + self.bitForMant + 1) - len(self.binNumber)) + self.binNumber
        self.isNegative = 1 if self.binNumber[0] == '1' else 0
        self.exponenta = int(self.binNumber[1:self.bitForExp + 1], 2) - (2 ** (self.bitForExp - 1) - 1)
        self.mantisa = int('1' + self.binNumber[self.bitForExp + 1:], 2)
        if self.exponenta == -(2 ** (self.bitForExp - 1) - 1):
            position = self.binNumber[self.bitForExp + 1:]
            self.exponenta -= position.find('1')
            position = position[position.find('1'):]
            position += "0" * (self.bitForMant - len(position) + 1)
            self.mantisa = int(position, 2)
            self.isDenorm = True
        self.getSpecialForm()

    def getSpecialForm(self):
        if self.exponenta == (2 ** self.bitForExp) // 2:
            if int(self.binNumber[self.bitForExp + 1:], 2) != 0:
                self.isNAN = True
            else:
                if self.isNegative:
                    self.isNegativeINF = True
                self.isINF = True
        elif self.mantisa == 0:
            if self.exponenta == -126 or self.exponenta == -14:
                self.isZero = True
                self.exponenta = 0
                self.mantisa = 0

    def mul(self, secondNumber):
        if IsNumberSpecial(self) or IsNumberSpecial(secondNumber):
            self.checkSpecialSituations(secondNumber, "*")
        else:
            isNegative = self.isNegative ^ secondNumber.isNegative
            a, b = self.mantisa, secondNumber.mantisa
            newMantisa = bin(a * b)[2::]
            newExponeta = self.exponenta + secondNumber.exponenta + len(newMantisa) - (self.bitForMant * 2 + 1)
            FloatingFormat.printNumber(newExponeta, newMantisa[1:self.bitForMant + 1:], isNegative, self.bitForMant,
                                       self.bitForExp)

    def div(self, secondNumber):
        if IsNumberSpecial(self) or IsNumberSpecial(secondNumber):
            self.checkSpecialSituations(secondNumber, "/")
        else:
            isNegative = self.isNegative ^ secondNumber.isNegative
            a, b = self.mantisa, secondNumber.mantisa
            newMantisa = bin((a << 32) // b)[2:]
            newExponeta = self.exponenta - secondNumber.exponenta - (32 - len(newMantisa) + 1)
            FloatingFormat.printNumber(newExponeta, newMantisa[1:self.bitForMant + 1:], isNegative, self.bitForMant,
                                       self.bitForExp)

    def add(self, secondNumber):
        if IsNumberSpecial(self) or IsNumberSpecial(secondNumber):
            self.checkSpecialSituations(secondNumber, "+")
        else:
            tempExponenta = min(self.exponenta, secondNumber.exponenta)
            a = self.mantisa << (self.exponenta - tempExponenta)
            b = secondNumber.mantisa << (secondNumber.exponenta - tempExponenta)
            if self.isNegative:
                a *= -1
            if secondNumber.isNegative:
                b *= -1
            newMantisa = bin(a + b)
            if newMantisa[0] == '-':
                newMantisa = newMantisa[3::]
                isNegative = 1
            else:
                newMantisa = newMantisa[2::]
                isNegative = 0
            newExponenta = min(self.exponenta, secondNumber.exponenta) + (len(newMantisa) - (self.bitForMant + 1))
            FloatingFormat.printNumber(newExponenta, newMantisa[1:self.bitForMant + 1:], isNegative, self.bitForMant,
                                       self.bitForExp)

    def sub(self, secondNumber):
        if IsNumberSpecial(self) or IsNumberSpecial(secondNumber):
            self.checkSpecialSituations(secondNumber, "-")
        else:
            tempExponenta = min(self.exponenta, secondNumber.exponenta)
            a = self.mantisa << (self.exponenta - tempExponenta)
            b = secondNumber.mantisa << (secondNumber.exponenta - tempExponenta)
            if self.isNegative:
                a *= -1
            if secondNumber.isNegative:
                b *= -1
            newMantisa = bin(a - b)
            if newMantisa[0] == '-':
                newMantisa = newMantisa[3::]
                isNegative = 1
            else:
                newMantisa = newMantisa[2::]
                isNegative = 0
            newExponenta = min(self.exponenta, secondNumber.exponenta) + (len(newMantisa) - (self.bitForMant + 1))
            FloatingFormat.printNumber(newExponenta, newMantisa[1:self.bitForMant + 1:], isNegative, self.bitForMant,
                                       self.bitForExp)

    def print(self):
        if self.isINF:
            print(f'{"-" if self.isNegative else ""}inf')
        elif self.isNAN:
            print('nan')
        else:
            FloatingFormat.printNumber(self.exponenta, bin(abs(self.mantisa))[3::], self.isNegative, self.bitForMant,
                                       self.bitForExp)

    def checkSpecialSituations(self, secondNumber, operation):
        match operation:
            case "+":
                if self.isZero and secondNumber.isZero:
                    FloatingFormat.printNumber(0, '0', False, self.bitForMant, self.bitForExp)
                if self.isNAN or secondNumber.isNAN:
                    print('nan')
                if self.isINF and secondNumber.isINF:
                    print(self.binNumber)
                    if self.isNegative == secondNumber.isNegative:
                        print(f'{"-" if self.isNegative else ""}inf')
                    else:
                        print("nan")
                elif self.isINF or secondNumber.isINF:
                    if self.isINF:
                        print(f'{"-" if self.isNegative else ""}inf')
                    else:
                        print(f'{"-" if secondNumber.isNegative else ""}inf')
            case "-":
                if self.isZero and secondNumber.isZero:
                    FloatingFormat.printNumber(0, '0', False, self.bitForMant, self.bitForExp)
                if self.isNAN or secondNumber.isNAN:
                    print('nan')
                if self.isINF and secondNumber.isINF:
                    if self.isNegative == secondNumber.isNegative:
                        print("nan")
                    else:
                        print(f'{"-" if self.isNegative else ""}inf')
                elif self.isINF or secondNumber.isINF:
                    if self.isINF:
                        print(f'{"-" if self.isNegative else ""}inf')
                    else:
                        print(f'{"" if secondNumber.isNegative else "-"}inf')
            case "*":
                if self.isNAN or secondNumber.isNAN:
                    print('nan')
                if (self.isZero and secondNumber.isINF) or (self.isINF and secondNumber.isZero):
                    print('nan')
                if self.isINF and secondNumber.isINF:
                    print(f'{"-" if self.isNegative ^ secondNumber.isNegative else ""}inf')
                if self.isINF or secondNumber.isINF:
                    if self.isINF:
                        print(f'{"-" if self.isNegative else ""}inf')
                    else:
                        print(f'{"-" if secondNumber.isNegative else ""}inf')
                if self.isZero or secondNumber.isZero:
                    FloatingFormat.printNumber(0, '0', False, self.bitForMant, self.bitForExp)
            case "/":
                if self.isZero and secondNumber.isZero:
                    print('nan')
                if self.isINF and secondNumber.isZero:
                    print(f'{"-" if self.isNegative ^ secondNumber.isNegative else ""}inf')
                if self.isZero and secondNumber.isINF:
                    print(f'{"-" if self.isNegative ^ secondNumber.isNegative else ""}0')
                if self.isNAN or secondNumber.isNAN:
                    print('nan')
                if secondNumber.isZero:
                    print(f'{"-" if secondNumber.isNegative else ""}inf')
                if self.isINF and secondNumber.isINF:
                    print('nan')

    @staticmethod
    def printNumber(exponenta, mantisa, isNegative, bitForMant, bitForExp):
        if exponenta == 0 and mantisa == "0" or mantisa == "" or ((exponenta <= -2 ** bitForExp // 2 + 1) and not(0)):
            ans = f'0x0.'
            mantisa = "0"
            exponenta = 0
        else:
            ans = f'{"-" if isNegative else ""}0x1.'
        if len(mantisa) > bitForMant:
            mantisa = mantisa[:bitForMant]
        if bitForMant == 10:
            mantisa += '0' * ((12 - len(mantisa) % 12) % 12)
        else:
            mantisa += '0' * ((24 - len(mantisa) % 24) % 24)
        index = 0
        if exponenta >= 2 ** bitForExp // 2:
            print(f'{"-" if isNegative else ""}inf')
            return None
        while index < len(mantisa):
            piece = mantisa[index:index + 4]
            for k, v in FixedPointFormat.mapForTranslation.items():
                if piece == v:
                    ans += k
                    index += 4
                    break
        ans += f'p{"+" if exponenta >= 0 else ""}{exponenta}'
        print(ans)
