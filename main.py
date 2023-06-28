# this is stellaris auto empire design import export
# last edit 28.05.2023
import Empire
import os
import json
import random


windows_illegal_symbols = ['<', '>', '*', '?', '/', r'\\', r'{', '}', '&', '#', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']

# def cleanEmpireDesigntxt(empireDesigntxt:str):
#     listOflines = empireDesigntxt.replace('\t', '').split('\n')
#     listOflinesFromSecond = listOflines[1::]
#     firstLine = listOflines[0].replace('=', ':')
#     map(lambda line : '"' + line.replace('=', '":'), listOflinesFromSecond)
#     return firstLine + ''.join(listOflinesFromSecond)
#     # add after afgument json needs ',' add ',' after true/false/"/}/null if next line isnt }
#     # add parce ingame enums like 'yes' to strings

def separateEmpires(s:str):
    empires = []
    counter = 0
    current_empire = [0, 0]
    lookint_for = 'start'
    skip_one = True
    for iter in range(0, len(s)):
        if s[iter] == '{':
            counter += 1
        if s[iter] == '}':
            counter -= 1
        if counter == 0 and s[iter] == '"':
            if lookint_for == 'start':
                current_empire[0] = iter
                lookint_for = 'end'
                continue
            if lookint_for == 'end':
                if skip_one:
                    skip_one = False
                    continue
                current_empire[1] = iter
                empires.append((current_empire[0], current_empire[1]))
                current_empire[0] = current_empire[1]
                lookint_for = 'end'
                skip_one = True
                continue
    empires.append((current_empire[0], len(s)))
    list_of_empires = []
    for empire in empires:
        list_of_empires.append(s[empire[0]:empire[1]])
    return list_of_empires

def readEmpireDesignsTxt():
    f = open('EmpireDesigns.txt', 'r')
    lines = f.read()
    empires = [Empire.Empire(_) for _ in separateEmpires(lines)]
    # print(empires[0])

    for e in empires:#remove windows illegel names from file names
        for s in windows_illegal_symbols:
            e.changeName(e.name.replace(s, ''))

    for e in empires:
        f = open('empires\\' + e.name, 'w')
        f.write(e.fulltxt)
        f.close()

def createNamseLists():
    fleshFile = open('names//flesh.txt', 'r')
    fleshList = fleshFile.read().split('\n')
    fleshFile.close()
    hiveFile = open('names//hive.txt', 'r')
    hiveList = hiveFile.read().split('\n')
    hiveFile.close()
    machineFile = open('names//machine.txt', 'r')
    machineList = machineFile.read().split('\n')
    machineFile.close()
    anyFile = open('names//any.txt', 'r')
    anyList = anyFile.read().split('\n')
    anyFile.close()
    return {'flesh': fleshList, 'machine':machineList, 'hive':hiveList, 'any':anyList}

def randomiseNames(possibleNames:list, anyNames:list, type:str):
    currentEmpires = os.listdir('empires/' + type)
    takenAnyNames = []
    numberOfEmpires = len(currentEmpires)
    targetNames = random.sample(possibleNames + anyNames, numberOfEmpires)
    empires = []

    for currentEmpireName in currentEmpires:
        if currentEmpireName in targetNames:
            targetNames.remove(currentEmpireName)
            print('{} shall stay'.format(currentEmpireName))
            continue
        # print('trying to parse: ' + currentEmpireName)
        f = open('empires/' + type + '/' + currentEmpireName, 'r')
        e = Empire.Empire(f.read())
        empires.append(e)
        f.close()
        os.remove('empires/' + type + '/' + currentEmpireName)

    counter = 0
    oldName = ''
    for empire in empires:
        oldName = empire.name
        empire.changeName(targetNames[counter])
        if targetNames[counter] in anyNames:
            takenAnyNames.append(targetNames[counter])
        counter += 1
        print('{} -> {}'.format(oldName, empire.name))
        f = open('empires/' + type + '/' + empire.name, 'w')
        f.write(empire.fulltxt)
        f.close()
    return takenAnyNames

def createuser_empire_designs_v34txt():
    machineEmpires = os.listdir('empires/AI')
    hiveEmpires = os.listdir('empires/hive')
    fleshEmpires = os.listdir('empires/flesh')
    result = ''
    for e in machineEmpires:
        f = open('empires/AI/' + e)
        result += f.read()
    for e in hiveEmpires:
        f = open('empires/hive/' + e)
        result += f.read()
    for e in fleshEmpires:
        f = open('empires/flesh/' + e)
        result += f.read()
    return result
def main():
    # readEmpireDesignsTxt()

    dirNames = createNamseLists()
    anyNamesTaken = randomiseNames(dirNames['machine'], dirNames['any'], 'AI')
    dirNames['any'] = [name for name in dirNames['any'] if name not in anyNamesTaken]
    anyNamesTaken = randomiseNames(dirNames['flesh'], dirNames['any'], 'flesh')
    dirNames['any'] = [name for name in dirNames['any'] if name not in anyNamesTaken]
    anyNamesTaken = randomiseNames(dirNames['hive'], dirNames['any'], 'hive')
    dirNames['any'] = [name for name in dirNames['any'] if name not in anyNamesTaken]

    f = open('user_empire_designs_v3.4.txt', 'w')
    f.write(createuser_empire_designs_v34txt())
    f.close()

if __name__ == '__main__':
    main()


