import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

def pokergame(probability_win,buy_in):
    randomnumber = random.random()
    if randomnumber < probability_win:
        return (buy_in,True)
    else:
        return (-buy_in,False)


def khalilmodel(start_buy_in,probability_win,max_buy_in = 'inf'):
    money_state = 0
    buy_in = start_buy_in
    while (buy_in <= max_buy_in):
        (value,win) = pokergame(probability_win,buy_in)
        money_state += value
        ###print money_state
        if win:
            return money_state
        else:
            buy_in = buy_in*2
    return money_state

def khalilnewmodel(start_buy_in,probability_win,max_buy_in):
    money_state = 0
    buy_in = start_buy_in
    while (buy_in <= max_buy_in):
        (value,win) = pokergame(probability_win,buy_in)
        money_state += value
        ###print money_state
        if win:
            return money_state
        else:
            buy_in = -money_state
    return money_state

def raoulmodel(start_buy_in,probability_win,max_buy_in = 'inf'):
    return pokergame(probability_win,start_buy_in)[0]

def tester(model,start_buy_in, number_of_tests,probability_win, max_buy_in = 'inf'):
    accumulated_wealth = 0
    b = 0
    for i in range(number_of_tests):
        a = accumulated_wealth
        accumulated_wealth += model(start_buy_in,probability_win,max_buy_in)
        if a > accumulated_wealth:
            b+=1
    return accumulated_wealth/float(number_of_tests)

def testertester(numtester,model,start_buy_in, number_of_tests,probability_win, max_buy_in):
    a = 0
    for i in range(numtester):
        a += tester(model,start_buy_in, number_of_tests,probability_win, max_buy_in)[2]
    return float(a)/numtester

def plot(minimum,maximum,step,model1,model2,model3,start_buy_in, number_of_tests,probability_win):
    oldtestlist = []
    newtestlist = []
    raoultestlist = []
    for i in range(minimum,maximum+step,step):
        a = tester(model1,start_buy_in, number_of_tests,probability_win,i)
        b = tester(model2,start_buy_in, number_of_tests,probability_win,i)
        c = tester(model3,start_buy_in, number_of_tests,probability_win,i)
        oldtestlist.append(a)
        newtestlist.append(b)
        raoultestlist.append(c)
        print (i,a,b,c)
    plt.plot([i for i in range(minimum,maximum+step,step)], oldtestlist, 'ro')
    plt.plot([i for i in range(minimum,maximum+step,step)], newtestlist, 'bs')
    plt.plot([i for i in range(minimum,maximum+step,step)], raoultestlist, 'g^')
    vasss = (min(oldtestlist)-10)
    plt.axis([0, maximum+step, vasss, abs(vasss)])
    plt.title('Max Buy In vs Expected Loss with a %d percent probability of winning' %(probability_win*100))
    plt.xlabel('Max Buy In')
    plt.ylabel('Expected Loss')
    lmodel1 = mpatches.Patch(color='red', label='betting double till win')
    lmodel2 = mpatches.Patch(color='blue', label='covering loss')
    lmodel3 = mpatches.Patch(color='green', label='playing the minimum $25')
    plt.legend(handles=[lmodel1,lmodel2,lmodel3])
    plt.show()
    
    
