import sys
import random

expressCount = 5  # 算式数目
expressList = []  # 算式列表
nRange = 10  # 操作数范围
count = 4  # 操作数的多少
ise = True


class Exam:
    expression = ""
    Canswer = ""
    answer = 0

    '''
    recursiveGeneral用于生成表达式
    '''

    def __init__(self, nRange, count):
        self.nRange = nRange
        self.count = count
        result = self.recursiveGeneral(self.count)
        self.expressList = result['expressList']
        self.expression = result['expression']
        self.answer = result['answer']
        self.Canswer = str(self.getFraction(result['answer']))

    '''
    将分子分母转换为分数，并计算真分数
    '''
    def getFraction(self, number):
        son = number[0]
        mom = number[1]
        if mom == 1:
            return son
        elif (son > mom):
            quotient = int(son / mom)
            son = son - (quotient * mom)
            return str(quotient) + "'" + str(son) + "/" + str(mom)
        else:
            return str(son) + "/" + str(mom)

    '''
    随机获取分子和分母，如果可以化成整数，则重新生成。
    getSimple用于化简分数
    '''
    def getRandomFraction(self):
        number_range = self.nRange
        while True:
            figure1 = self.getRandom(number_range)
            figure2 = self.getRandom(number_range)
            if (figure1 % figure2) == 0 or figure2 == 0:
                continue
            else:
                break
        return self.getSimple(figure1, figure2)

    '''
    分配分数和整数表达式数量，避免全为一类
    getRandomFraction获取最简随机分数
    getFraction计算真分数
    '''
    def getRandomNum(self):  # 获得随机运算数字
        number_range = self.nRange
        result = {}
        if self.getRandom(100) > 50:
            figure = self.getRandom(number_range - 1)
            result['figure'] = figure
            result['figure_char'] = str(figure)
            result['figure_array'] = [figure, 1]
        else:
            figure = self.getRandomFraction()
            result['figure'] = figure[0] / figure[1]
            result['figure_char'] = self.getFraction(figure)
            result['figure_array'] = [figure[0], figure[1]]
        return result

    '''
    返回运算符
    '''
    def getCoperator(self, operator):
        operatorArray = ['+', '-', '×', '÷']
        return operatorArray[operator - 1]

    '''
    获取随机数
    '''
    def getRandom(self, range):
        return random.randint(1, range)

    '''
    计算表达式结果
    '''
    def getRes(self, figure1, figure2, operate):
        # eval(operation)
        if operate == 1:
            numerator = figure1[0] * figure2[1] + figure2[0] * figure1[1]
            denominator = figure1[1] * figure2[1]
        elif operate == 2:
            numerator = figure1[0] * figure2[1] - figure2[0] * figure1[1]
            denominator = figure1[1] * figure2[1]
            if numerator < 0:
                return [numerator, denominator]
        elif operate == 3:
            numerator = figure1[0] * figure2[0]
            denominator = figure1[1] * figure2[1]
        elif operate == 4:
            numerator = figure1[0] * figure2[1]
            denominator = figure1[1] * figure2[0]
        result = self.getSimple(numerator, denominator)
        return result

    '''
    化简分数
    '''
    def getSimple(self, numerator, denominator):
        flage = self.getGreatestCommonDivisor(numerator, denominator)
        numerator = int(numerator / flage)
        denominator = int(denominator / flage)
        return [numerator, denominator]

    '''
    得到最大公约数
    '''
    def getGreatestCommonDivisor(self, numerator, denominator):
        numerator, denominator = denominator, numerator % denominator
        if denominator == 0:
            return numerator
        else:
            return self.getGreatestCommonDivisor(numerator, denominator)

    '''
    递归二叉树生成表达式
    '''
    def recursiveGeneral(self, count):
        if count == 1:
            figure = self.getRandomNum()
            return {
                'expressList': figure['figure'],
                'expression': figure['figure_char'],
                'answer': figure['figure_array']
            }
        else:
            leftcount = self.getRandom(count - 1)
            rightcount = count - leftcount

            left = self.recursiveGeneral(leftcount)
            right = self.recursiveGeneral(rightcount)

            operate = self.getRandom(4)

            if operate == 4 and right['answer'][0] == 0:
                t = left
                left = right
                right = t
            answer = self.getRes(left['answer'], right['answer'], operate)
            if answer[0] < 0:
                t = left
                left = right
                right = t
                answer = self.getRes(left['answer'], right['answer'], operate)

            leftvalue = left['answer'][0] / left['answer'][1]
            rightvalue = right['answer'][0] / right['answer'][1]
            expressList = [left['expressList'], operate, right['expressList']]
            if type(left['expressList']) != list and type(right['expressList']) != list:  # 两个子树都为值
                if (operate == 1 or operate == 3) and leftvalue < rightvalue:
                    expressList = [right['expressList'], operate, left['expressList']]
            elif type(left['expressList']) == list and type(right['expressList']) == list:  # 两个子树都为树
                if operate == 1 or operate == 3:
                    if leftvalue == rightvalue and left['expressList'][1] < right['expressList'][
                        1]:  # 树的值相等时，运算符优先级高的在左边
                        expressList = [right['expressList'], operate, left['expressList']]
                    elif leftvalue < rightvalue:
                        expressList = [right['expressList'], operate, left['expressList']]
                if operate in [3, 4]:
                    if left['expressList'][1] in [1, 2]:
                        left['expression'] = '(' + left['expression'] + ')'
                    if right['expressList'][1] in [1, 2]:
                        right['expression'] = '(' + right['expression'] + ')'
            else:  # 一边的子树为树
                if operate == 1 or operate == 3:
                    if type(right['expressList']) == list:
                        expressList = [right['expressList'], operate, left['expressList']]
                if operate in [3, 4]:
                    if type(left['expressList']) == list and left['expressList'][1] in [1, 2]:
                        left['expression'] = '(' + left['expression'] + ')'
                    if type(right['expressList']) == list and right['expressList'][1] in [1, 2]:
                        right['expression'] = '(' + right['expression'] + ')'
            expression = left['expression'] + ' ' + self.getCoperator(operate) + ' ' + right['expression']
            return {
                'expressList': expressList,
                'expression': expression,
                'answer': answer
            }

'''
交给exam类生成表达式
'''
def _birthExpress(expression_count, number_range, count):
    List = []
    for i in range(expression_count):
        expression = Exam(number_range, count)
        while _checkRepeat(expression, List):
            expression = Exam(number_range, count)
        List.append({
            'expressList': expression.__dict__['expressList'],
            'expression': expression.__dict__['expression'],
            'answer': expression.__dict__['answer'],
            'Canswer': expression.__dict__['Canswer']
        })
    return List

def _checkRepeat(expression, List):
    expressionarray = expression.__dict__['expressList']
    for i in List:
        if expressionarray == i['expressList']:
            return True
    return False

def _checkUserAns(fileName):
    with open(fileName, "r", encoding="gbk") as file:
        lines = file.readlines()
        list = []
        for line in lines:
            list.append(line.replace("\n", ""))
    return list


def _cmpAns(list):
    correct = []
    wrong = []
    grade = []
    with open('Answer.txt', "r", encoding="gbk") as f:
        lines = f.readlines()
        listA = []
        for line in lines:
            listA.append(line.replace("\n", ""))
    for num in range(expressCount):
        if listA[num] != list[num]:
            wrong.append(num)
        else:
            correct.append(num)
    grade.append(correct)
    grade.append(wrong)
    return grade

'''
保存生成的表达式
'''
def _writeBirth(expressionlist):
    with open("Exercises.txt", "w") as fE:
        with open("Answer.txt", "w") as fA:
            for i in range(len(expressionlist)):
                fE.write(str((i + 1)) + '. ' + expressionlist[i]['expression'] + ' =\n')
                fA.write(str((i + 1)) + '. ' + expressionlist[i]['Canswer'] + '\n')

'''
处理参数
'''
def toolBar(argv):
    global expressCount, nRange, ise
    if argv[1] == '-n':
        expressCount = int(argv[2])
    elif argv[1] == '-r':
        nRange = int(argv[2])
    elif argv[1] == '-e':
        ise = False
        ans = _checkUserAns(argv[2])
        res = _cmpAns(ans)
        with open('Grade.txt', "w") as fG:
            print('[+] Correct:' + str(len(res[0])) + str(res[0]) + '\n' + '[-] Wrong:' + str(len(res[1])) + str(
                res[1]))
            fG.write('[+] Correct:' + str(len(res[0])) + str(res[0]) + '\n' + '[-] Wrong:' + str(len(res[1])) + str(
                res[1]))


if __name__ == '__main__':
    toolBar(sys.argv)
    expressList = _birthExpress(expressCount, nRange, count)
    if ise == True:
        _writeBirth(expressList)
