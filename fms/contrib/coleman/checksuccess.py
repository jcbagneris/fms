#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Checks the Success of Agent Behaviors
"""

__author__ = "Sami Nazif / Patrick Coleman"
__license__ = "BSD"

import sys
import dumbstartfms

def main():
    """
    Runs a head to head competition of agent behavior types.
    """
    expnum = 0
    agents = []
    overall = dict()


#    agents = ['AvgBuySellTrader','AvgBuySellTraderD','DefectorTrader',
#              'DeflationaryTrader', 'InflationaryTrader','Mem1Trader', 
#              'Mem3Trader','Mem5Trader', 'Mem5TraderD',
#              'Mem10Trader',
#              'ProbeAdjustBSTrader','ProbeAdjustTrader', 'ProbeSameTrader',
#              'RandomFixedTrader', 'RandomFixedTraderHalves','SmartMem3Trader',
#              'SmartMem5Trader', 'SmartMem5TraderD', 'SmartMem10Trader',
#	      'ZeroIntelligenceBoundedTrader', 'ZeroIntelligenceTrader',
#              'ZeroIntelligenceTraderNL', 'ZigFastTrader','ZigTrader']
#    overall = {'AvgBuySellTrader':0,'AvgBuySellTraderD':0,'DefectorTrader':0,
#              'DeflationaryTrader':0, 'InflationaryTrader':0,'Mem1Trader':0,
#              'Mem3Trader':0,'Mem5Trader':0, 'Mem5TraderD':0, 
#              'Mem10Trader':0,
#              'ProbeAdjustBSTrader':0,'ProbeAdjustTrader':0, 'ProbeSameTrader':0,
#              'RandomFixedTrader':0, 'RandomFixedTraderHalves':0,'SmartMem3Trader':0,
#              'SmartMem5Trader':0, 'SmartMem5TraderD':0, 'SmartMem10Trader':0, 
#              'ZeroIntelligenceBoundedTrader':0, 'ZeroIntelligenceTrader':0,
#              'ZeroIntelligenceTraderNL':0, 'ZigFastTrader':0,'ZigTrader':0}


    #overall = {'AvgBuySellTrader':0,'DefectorTrader':0,'Mem1Trader':0,
    #          'Mem3Trader':0,'Mem5Trader':0, 'Mem10Trader':0,
    #          'ProbeAdjustBSTrader':0, 'ProbeSameTrader':0,
    #          'RandomFixedTrader':0, 'RandomFixedTraderHalves':0,
    #          'ZeroIntelligenceBoundedTrader':0,'ZeroIntelligenceTrader':0}
    #agents = ['AvgBuySellTrader','Mem5Trader', 'Mem10Trader',
    #          'RandomFixedTraderHalves',]

    agentfile = open('agentfile.txt','r')
    
    #This looks through the config file to pull out the agents that
    #will participate in the head to head
    for line in agentfile:
	if line.startswith('#'):
	    continue
	else:
	    agents.append(line.rstrip())
	    overall[line.rstrip()] = 0


    #Loops through the agents, running them against each other, excluding
    #identical types. The script generates experiment YAML files which are
    #then run using a specific version of startfms.py (dumbstart),
    #the original fms runtime.

    for agenti in agents:
        for agentj in agents:
            if agenti == agentj:
                continue
            currentagent = agenti
            nextagent = agentj
            #print agenti
	    #print agentj 
            expname = 'exp' + str(expnum)
            args = ['run', expname + '.yml']
            yamltowrite = open(expname + '.yml', 'w')
            linestowrite = []
            linestowrite.append('--- # Experiment ' + str(expnum))     
            linestowrite.append('outputfilename: ' + expname + '.csv')
            linestowrite.append('orderslogfilename: ' + expname + '.log')
            yamltoread = open('template.yml', 'r')
            for line in yamltoread:
                linestowrite.append(line)
            yamltoread.close()
            #This is the important agent specification part
            linestowrite.append('agents:')
            linestowrite.append('    - classname: ' + currentagent)
            linestowrite.append('      number: 100')
            linestowrite.append('      money: 100000')
            linestowrite.append('      stocks: 1000')
            linestowrite.append('      args: [1000, 1000]')
            linestowrite.append('    - classname: ' + nextagent)
            linestowrite.append('      number: 100')
            linestowrite.append('      money: 100000')
            linestowrite.append('      stocks: 1000')
            linestowrite.append('      args: [1000, 1000]')
            
            for line in linestowrite:
                yamltowrite.write(line.rstrip() + '\n') 
            
            yamltowrite.close()
            dumbstartfms.main(args)
            wealthresult = wealth_tester(expname)
            
	    
	    for guy in wealthresult.keys():
                overall[guy] += wealthresult[guy]
            expnum += 1 #increment the exp number counter
    
    fultimateout = open('ultimateoutput.txt', 'a')
    dudes = [key for key, dummy in sorted(overall.items(), key = lambda arg: arg[1], reverse = True)]
    fultimateout.write('==========================================================================' + '\n')
    for dude in dudes:
        fultimateout.write('Agent ' + dude + ' scored ' + str(overall[dude]) + ' overall.' + '\n')
    return 0


def wealth_tester(expname):
    '''
    Checks the TotalWealth of each Behavior Type in the wealth file.
    '''
    try:
        wealthfile = open(expname + 'wealth.csv', 'r')
    except IOError:
        print "Check the wealth file."
   
    try:
       transactionfile = open(expname + '.csv')    
    except IOError:
        print "Error in passing the csv file"
    
    fout = open('ultimateoutput.txt', 'a')
    
    #find the average stockprice
    #indices for readability
    #time = 0
    #transactionnum = 1
    #price = 2
    #volume = 3
    #totalprice = 0
    #numtrans = 0
    #skipfirstlines = 0
    #for line in transactionfile:
    #    if skipfirstlines == 0 or skipfirstlines == 1:
    #        skipfirstlines += 1
    #        continue
    #    splitline = line.split(';')
    #    totalprice = totalprice + (int(float(splitline[price])) * int(splitline[volume]))
    #    numtrans = numtrans + int(splitline[volume])
    #    avgtrans = totalprice / numtrans    
    avgtrans = 500 #This replaces the actual average finder
    
    totalwealth = dict()
    #indices for readability
    time = 0
    id = 1 
    behavior = 2
    wealth = 3
    stock = 4
    
    for line in wealthfile:
        splitline = line.split(';')
        agent = splitline[behavior]
        #print agent
        if agent in totalwealth.keys():
            #add wealth
            totalwealth[agent] = totalwealth[agent] + int(splitline[wealth])
            #add stock x avg transaction price
            totalwealth[agent] = totalwealth[agent] + (int(splitline[stock]) * avgtrans)
        else:
            totalwealth[agent] = 0
            #add wealth
            totalwealth[agent] = totalwealth[agent] + int(splitline[wealth])
            #add stock x avg transaction price
            totalwealth[agent] = totalwealth[agent] + (int(splitline[stock]) * avgtrans)
        
    #Order them top to bottom
    agents = [key for key, dummy in sorted(totalwealth.items(), key = lambda arg: arg[1], reverse = True)]
        #print agents
    #for agent in agents:
    #    print totalwealth[agent]        
    #print totalwealth
    #print type(totalwealth.keys())
    print totalwealth
    fout.write(expname + '\n') 
    fout.write('Agent1: ' + agents[0] + " has a total wealth of " + str(totalwealth[agents[0]]) + '\n')
    fout.write('Agent2: ' + agents[1] + " has a total wealth of " + str(totalwealth[agents[1]]) + '\n')
    
    wealthfile.close()
    fout.close()
    return totalwealth
    



if __name__ == "__main__":
    sys.exit(main())


