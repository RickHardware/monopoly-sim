import numpy as np
import pandas as pd
import random as rd
import MonoUtils as MU
#import matplotlib.pyplot as plt

class Player:
    def __init__(self, name):
        self.name = name
        self.Cash = 2500
        self.Properties = []
        self.Position = 0
        self.TimesPassedGo = 0
        self.cashtracker = []
        self.rolltracker = []
        self.bankrupt = 0
        self.owedonnextturn = 0

    def SameColourCounter(self,Property, Board):
        rightcolour  = Board[['Colour']].loc[Board['Name'] == Property]
        rightnum = 0
        for ii in range(0, len(self.Properties)):
            if Board[['Colour']].loc[Board['Name'] == Property] ==rightcolour:
                rightnum+=1
        amountneededforset = int(Board[['Number']].loc[Board['Name'] == Property]) -rightnum
        return(amountneededforset)      

    def TradeAnalyser(self, PropertyForSale, Board):
        #factors in trade:  affordable? Same props? 
        #0.5 numeber to full set 0.4 affordable, 0.1 random
        propprice = Board[['Price']].loc[Board['Name'] == PropertyForSale]
        ColourCoefficient =  1/(self.SameColourCounter(PropertyForSale)) 
        RandomCoefficient = rd.randint(0,10)/100
        if self.Cash < propprice:
            AffordabilityCoefficient = -100
        else:
            AffordabilityCoefficient = (1/(propprice/self.Cash))*0.4
        FavourabilityCoeff = RandomCoefficient + ColourCoefficient + AffordabilityCoefficient
        return(FavourabilityCoeff) 
            
        
    def PayRent(self,rent, Paywho, WhoPays):
        self.Cash -= rent
        if Paywho == WhoPays:
            print("Can't pay yourself!")
            return([0,"nobody", "nobody"])
        else:
            return([rent, Paywho, WhoPays])
    
    def BuyProperty(self, PropertyLandedOnDframe):      
        print(self.name + " has bought " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] +" for " + str(PropertyLandedOnDframe.iloc[[0],[4]].values[0]))
        self.ownedprops.append(int(self.Position))
        self.ownersofprops.append(self.name)
        self.Properties.append(self.Position)


    
    def TakeYourTurn(self, Board, ownedprops, ownersofprops):
        #must instantiate sometimes unused variables:
        rentowed = 0
        towhom = "blank"
        fromwhom = "blank"
        self.Board = Board
        self.ownedprops = ownedprops
        self.ownersofprops = ownersofprops


        #For debug say who has how much moneu
        print("Start Turn " + self.name + " has " + str(self.Cash))
##      
        if int(self.Cash) <= 0:
            print("Bankrupt")
            self.bankrupt += 1       
        if self.bankrupt >0:
            self.Cash = 0
            print(self.name + " is bankrupt and cannot roll")
            self.cashtracker.append(0)
            returnlist = [Board, self.ownedprops, self.ownersofprops, rentowed, towhom, fromwhom]
            return(returnlist)
        
        #roll and move
        rolled = MU.dice_roller()
        self.Position += rolled
        self.rolltracker.append(rolled)
        #position logic

        #Pass go Check:
        if self.Position>=40:
            self.Cash+=200
            self.Position-=40
        #Track Cash        
        self.cashtracker.append(int(self.Cash))
        #print(self.name,self.Position,"position")
        PropertyLandedonFilter = (Board["Position"]==self.Position)
        PropertyLandedOnDframe = Board.where(PropertyLandedonFilter)
        PropertyLandedOnDframe = PropertyLandedOnDframe.dropna()

        if len(PropertyLandedOnDframe)>=1:
            print(self.ownedprops)
            print(self.ownedprops.count(int(self.Position)))         
            if self.ownedprops.count(self.Position) > 0 :
                print(self.name + " cannot buy " +PropertyLandedOnDframe.iloc[[0],[0]].values[0]  + " is already owned")
                if self.ownersofprops[self.ownedprops.index(self.Position)] == self.name:
                    print("by"+self.name)
                else:
                    print(self.name +" Pays " + self.ownersofprops[self.ownedprops.index(self.Position)]+' '+str(Board["Rent"][self.Position]))
                    rentlist = self.PayRent(Board["Rent"][self.Position], self.ownersofprops[self.ownedprops.index(self.Position)], self.name)
                    rentowed = rentlist[0]
                    towhom = rentlist[1]
                    fromwhom = rentlist[2]
                returnlist = [Board, self.ownedprops, self.ownersofprops, rentowed, towhom, fromwhom]
                return(returnlist)
            elif  (4,38).count(self.Position) > 0:
                print(self.name + " has paid " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] +" of " + str(PropertyLandedOnDframe.iloc[[0],[4]].values[0]))
            elif  (10,20,30).count(self.Position) >0:
                print(self.name + " is just resting at " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] )                 
            else:                
                self.BuyProperty(PropertyLandedOnDframe)
            owed = (PropertyLandedOnDframe.iloc[[0],[4]]).values[0]
            self.Cash -= owed
            returnlist = [self.Board, self.ownedprops, self.ownersofprops, rentowed, towhom, fromwhom]
            #print("returnlist")
            #print(len(returnlist))
            #print(self.ownedprops)
            return(returnlist)