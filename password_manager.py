from getpass import getpass


class PasswordManager:
    uppercaseStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercaseStr = "abcdefghijklmnopqrstuvwxyz"
    numberStr = "0123456789"
    symbolStr = "~!@#$%^&*"
    ratioDict = {"U": 0.2, "L": 0.3, "S": 0.1}

    def __init__(self) -> None:
        self.__userName = input(
            "Hello, I'm your password manager UePG. What should I call you?\n"
        )
        print(f"Nice to meet you, {self.__userName}!")
        self.__privateKey = getpass(
            "Please input your private key to active me, and you MUST remember it.\n"
        )
        print("Well done! Enjoy your password manager~")

    def __require_c(self) -> bool:
        # U, L, S requirements
        while True:
            s = input(
                "Do you need <uppercase> <lowercase> <symbol>? (Enter three y/n)\n"
            )
            notYN = [i for i in s if i not in "YyNn "]
            if not notYN:
                ynList = [i for i in s if i in "YyNn"]
                if len(ynList) == 3:
                    U, L, S = [True if i in "Yy" else False for i in ynList]
                    break
                else:
                    print("# Invalid input, please enter THREE y or n")
            else:
                print("# Invalid input, please enter and ONLY enter y or n")
        return U, L, S

    def __require_n(self) -> int:
        # D requirement
        while True:
            res = None
            nList = input(
                "Length between? (enter two numbers not smaller than 6,\n"
                "and separate them with one space)\n"
            ).strip()
            nList = [i for i in nList.split(" ") if i != ""]
            # check if all numbers
            allNum = True
            for i in nList:
                for k in i:
                    if k not in "0123456789":
                        print("# Invalid input, please enter numbers only")
                        allNum = False
                        break
                else:
                    continue
                break
            if not allNum:
                continue
            # check if only two numbers
            if len(nList) != 2:
                print("# Invalid input, please enter TWO numbers")
                continue
            nList = [int(i) for i in nList]
            n1, n2 = min(nList), max(nList)
            # check if larger than 6
            if n1 < 6:
                print("# Invalid input, please enter two number NOT smaller than 6")
                continue
            if n1 == n2:
                res = n1
            else:
                place = 0
                for c in self.__privateKey:
                    place += ord(c)
                place %= n2 - n1 + 1
                res = n1 + place
            break
        return res

    def __encrypt(self, index: str, U: bool, L: bool, S: bool, D: int) -> None:
        p1 = "UT" + self.__privateKey[0] if U else "UF" + self.__privateKey[-1]
        p2 = "LT" + self.__userName[0] if L else "LF" + self.__userName[-1]
        p3 = "ST" + self.__privateKey[-1] if S else "SF" + self.__privateKey[0]
        p4 = str(D)
        ordN, ordK = 0, 0
        for i in self.__userName:
            ordN += ord(i)
        for i in self.__privateKey:
            ordK += ord(i)
        ordSum = ordN + ordK
        for i in index + p1 + p2 + p3 + p4:
            ordSum += ord(i)
        x, y = str(round((ordSum + 1 / 7) ** (1 / 3), D)).split(".")
        while len(y) < D:
            y += str((ordN - ordK - int(y[-1])) % 9)
        x, y = int(x), list(y)
        # arrange characters each position
        nDict = {"U": U, "L": L, "S": S}
        for k, v in self.ratioDict.items():
            if nDict[k]:
                nDict[k] = int(v * D) if int(v * D) else 1
            else:
                nDict[k] = 0
        usedPos = set()
        # change number into uppercase
        while nDict["U"]:
            pos = (x + ordN + sum(usedPos)) % D
            while pos in usedPos:
                pos = (pos + 1) % D
            char = self.uppercaseStr[(x + ordK + sum(usedPos)) % 26]
            y[pos] = char
            usedPos.add(pos)
            nDict["U"] -= 1
        # change number into lowercase
        while nDict["L"]:
            pos = (x + ordN + sum(usedPos)) % D
            while pos in usedPos:
                pos = (pos + 1) % D
            char = self.lowercaseStr[(x + ordK + sum(usedPos)) % 26]
            y[pos] = char
            usedPos.add(pos)
            nDict["L"] -= 1
        # change number into symbol
        while nDict["S"]:
            pos = (x + ordN + sum(usedPos)) % D
            while pos in usedPos:
                pos = (pos + 1) % D
            char = self.symbolStr[(x + ordK + sum(usedPos)) % len(self.symbolStr)]
            y[pos] = char
            usedPos.add(pos)
            nDict["S"] -= 1
        password = "".join(y)
        print(f"Your password for {index}: {password}")

    def get_password(self) -> None:
        print("-" * 8)
        print("Please enter the information according to my prompts.")
        need = True
        while need:
            index = input("What's your password index?\n")
            U, L, S = self.__require_c()
            if not (U or L or S):
                print("# Invalid input, cannot generate a password without characters")
                continue
            D = self.__require_n()
            self.__encrypt(index, U, L, S, D)
            while True:
                need = input("Need another password? (y/n)\n")
                if need in "Yy":
                    need = True
                    break
                elif need in "Nn":
                    need = False
                    break
                else:
                    print("# Invalid input, please enter y or n")
        print("-" * 8)
        input("Wake me up anytime, bye~ (Enter to exit)\n")


if __name__ == "__main__":
    PasswordManager().get_password()
