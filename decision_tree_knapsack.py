'''
///////////////////////////
11/11/18 // oserttas-math
///////////////////////////
Content :
Brute force optimaztion for knapsack problem
Source:
Introduction to Computation and Programming Using Python
by John Guttag
'''

class Letter(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.weight = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.weight
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.weight) + '>'

def buildMenu(names, values, weights):
    menu = []
    for i in range(len(values)):
        menu.append(Letter(names[i], values[i],
                          weights[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of Items to numbers"""
    itemsCopy = sorted(items, key = keyFunction,
                       reverse = True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)

def testGreedys(letters, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'weights')
    testGreedy(letters, maxUnits, Letter.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'weights')
    testGreedy(letters, maxUnits,
               lambda x: 1/Letter.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'weights')
    testGreedy(letters, maxUnits, Letter.density)

def maxVal(toConsider, avail):
    """Assumes toConsider a list of items, avail a weight
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the items of that solution"""
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #Explore right branch only
        result = maxVal(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        #Explore left branch
        # Where you will have the element 'a'
        withVal, withToTake = maxVal(toConsider[1:],
                                     avail - nextItem.getCost())
        withVal += nextItem.getValue()
        #Explore right branch
        # Where you will not have the element 'a'
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result

def testMaxVal(letters, maxUnits, printItems = True):
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = maxVal(letters, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print('   ', item)

names = ['a', 'b', 'c', 'd']
values = [6, 7, 8, 9]
weights = [3, 3, 2, 5]
letters = buildMenu(names, values, weights)

testGreedys(letters, 5)
print('')
print('Best Result from Tree')
print('')
testMaxVal(letters, 5)
