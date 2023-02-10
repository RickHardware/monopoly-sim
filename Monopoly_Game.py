import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
#Road Map:
#Good:
#Game plays
#Rent is paid properly
#Bankrupty Works

#Want:
#Houses are buyable
#Chance and community chest works
#Trading works

#Need  an affordability algorithm for buying property? and houses:
    #Maybe will analyse board to see if any rents are big enough tobankrupt

#Need Trade analyser|:
    #propose if score greateer than a certain amount
    #IE enough money and owns other properties in the suit
    
    #accept if greater than a certain amount:
    #needs money. maybe with hold if will give a rival a full set.
#Think Ck2 opinion:
    #as seller:
        # +10 I dont own any others
        # -10 opponent owns some
#Scores drive acceptable price ranges for each.
    #seller will sell for at lest 300 buyer will buy for less than 350: sold at 350


Board= pd.read_csv("Monoboard.csv")
ownedprops = []
ownersofprops = []
#Board.describe()
#print(Board)

def dice_roller():
    result = rd.randrange(1,7)
    #print('You rolled a ' + str(result))
    return(result)

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
    
    def SameColourCounter(self,Property):
        rightcolour  = Board[['Colour']].loc[Board['Name'] == Property]
        rightnum = 0
        for ii in range(0, len(self.Properties)):
            if Board[['Colour']].loc[Board['Name'] == Property] ==rightcolour:
                rightnum+=1
        amountneededforset = int(Board[['Number']].loc[Board['Name'] == Property]) -rightnum
        return(amountneededforset)

    def ColourCounter(self, Props_Owned,colour):
        #ColourCounts 
        #Colours = 
        BrownCount = 0
        LBCount = 0
        PinkCount = 0
        OrangeCount = 0
        RedCount = 0
        YellowCount = 0
        GreenCount = 0
        DBCount = 0
        colours = []
        Fullsets = []
        for ii in range(0, len(Props_Owned)):
            colours.append(Board["Color"][Props_Owned[ii]])
        for ij in range(0, len(Props_Owned)):
            if colours[ij] =="Brown":
                BrownCount +=1
            if colours[ij] =="LightBlue":
                LBCount +=1
            if colours[ij] =="Pink":
                PinkCount +=1
            if colours[ij] =="Orange":
                OrangeCount +=1
            if colours[ij] =="Red":
                RedCount +=1
            if colours[ij] =="Yellow":
                YellowCount +=1
            if colours[ij] =="Green":
                GreenCount +=1
            if colours[ij] =="DarkBlue":
                DBCount +=1
        if BrownCount==2:
            Fullsets.append("Brown")
        
        

    def TradeAnalyser(self,BuyerCash,SellerCash, PropertyForSale,BuyerPortf,SellerPort):
        #factors in trade:  affordable? Same props? 
        ColourCoefficient =  Player.SameColourCounter(PropertyForSale)
        FavourabilityCoeff = ColourCoefficient/3*2
        randomness = randint(0,10)/10*2
        Affordable = 0
        int(Board[['Price']].loc[Board['Name'] == PropertyForSale])
        return(FavourabilityCoeff) 
            
        
    def PayRent(self,rent, Paywho, WhoPays):
        self.Cash -= rent
        if Paywho == WhoPays:
            print("Can't pay yourself!")
            return()
        if Paywho == P1.name:
            P1.owedonnextturn += rent
        if Paywho == P2.name:
            P2.owedonnextturn += rent
        if Paywho == P3.name:
            P3.owedonnextturn += rent
    
    def TakeYourTurn(self):
        self.Cash += self.owedonnextturn
        if self.owedonnextturn >=1:
            print(self.name +" got " + str(self.owedonnextturn) + ' in rent!')
        self.owedonnextturn =0
        if self.bankrupt >0:
            self.Cash = 0
            print(self.name + " is bankrupt and cannot roll")
            self.cashtracker.append(0)
            return(print("Bankrupt"))
        if int(self.Cash) <= 0:
            print("Bankrupt")
            self.bankrupt += 1
        rolled = dice_roller()
        self.Position += rolled
        self.rolltracker.append(rolled)
        if self.Position>=40:
            self.Cash+=200
            self.Position-=40
        newcash = int(self.Cash)
        self.cashtracker.append(newcash)
        #print(self.name,self.Position,"position")
        PropertyLandedonFilter = (Board["Position"]==self.Position)
        PropertyLandedOnDframe = Board.where(PropertyLandedonFilter)
        PropertyLandedOnDframe = PropertyLandedOnDframe.dropna()
        #print(len(PropertyLandedOnDframe),"results")
        propname = str((PropertyLandedOnDframe.iloc[[0],[0]].values[0]))
        if len(PropertyLandedOnDframe)>=1:         
            if self.Position in ownedprops :
                print(self.name + " cannot buy " +PropertyLandedOnDframe.iloc[[0],[0]].values[0]  + " is already owned")
                if ownersofprops[ownedprops.index(self.Position)] == self.name:
                    print("by"+self.name)
                else:
                    print(self.name +" Pays " + ownersofprops[ownedprops.index(self.Position)]+' '+str(Board["Rent"][self.Position]))
                    Player.PayRent(self,Board["Rent"][self.Position], ownersofprops[ownedprops.index(self.Position)], self.name)
                return("property owned")
            elif self.Position in (4,38):
                print(self.name + " has paid " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] +" of " + str(PropertyLandedOnDframe.iloc[[0],[4]].values[0]))
            elif self.Position in(10,20,30):
                print(self.name + " is just resting at " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] )                 
            else:                
                print(self.name + " has bought " + PropertyLandedOnDframe.iloc[[0],[0]].values[0] +" for " + str(PropertyLandedOnDframe.iloc[[0],[4]].values[0]))
                ownedprops.append(self.Position)
                ownersofprops.append(self.name)
                self.Properties.append(self.Position)
            owed = (PropertyLandedOnDframe.iloc[[0],[4]]).values[0]
            self.Cash -= owed
            #print(Player.ColourCounter(self, self.Properties))


        
        # if self.Position 
        # if self.Position ==4:
        #     print("Taxes!")
        #     self.Cash-= 200
        # if self.Position ==38:
        #     print("Little Taxes!")
        #     self.Cash-= 100
        # print(self.Position)



        #print(self.name +' is on tile number ' + str(self.Position) + 'And has ' + str(self.Cash) + 'Dollars')
            
        
P1 = Player("Tommy")
P2 = Player("Sally") 
P3 = Player("Andre")



    #more points if buyer owns owns other colours
   
    


class Game:
    def __init__(self,TurnLimit):
        self.TurnLimit =TurnLimit
        

    def PlayAGame(self):
        Turn = 1
        plotassist = np.arange(1,self.TurnLimit +1)
        while(Turn<=(self.TurnLimit)):
            P1.TakeYourTurn()
            print("END TURN")
            P2.TakeYourTurn()
            print("END TURN")
            P3.TakeYourTurn()
            print("END TURN")
            Turn+=1
            #time.sleep(0.000001)
            print("Turn Number = " + str(Turn))
            #print(Turn)
        #print(Turn)
        P1.Position =0
        P2.Position = 0
        if P1.Cash == P2.Cash and P1.Cash ==P3.Cash:
            print("DRAW")
        else:
            if P1.Cash > P2.Cash:
                if P1.Cash>P3.Cash:
                    winner = P1
                else:
                    winner = P3
            else: 
                winner = P2                   
            print("Winner = " + winner.name + " with "+ str(int(winner.Cash)) )
            print("portfolio = ")
            for i in range(0, len(winner.Properties)):
                print(Board["Name"][winner.Properties[i]])
        #    print(winner.Properties)
            toplot = P1.cashtracker
            #print(toplot)
            plt.plot(plotassist,toplot, label = P1.name)
            toplot = P2.cashtracker
           # print(toplot)
            plt.plot(plotassist,toplot, label = P2.name)
            toplot = P3.cashtracker
        #    print(toplot)
            plt.plot(plotassist,toplot, label = P3.name)
            plt.legend(loc="upper left")


Game1 = Game(100)
Game1.PlayAGame()
# print(plotassist)
# toplot = P1.cashtracker
# plt.plot(toplot,plotassist, label = P1.name)
# toplot = P2.cashtracker
# plt.plot(toplot,plotassist, label = P2.name)
# toplot = P3.cashtracker
# plt.plot(toplot,plotassist, label = P3.name)
# plt.legend(loc="upper left")


#print(P1.rolltracker)
#toplot = P1.rolltracker
#plt.plot(toplot,plotassist, label = P1.name)
#toplot = P2.rolltracker
#plt.plot(toplot,plotassist, label = P2.name)
#toplot = P3.rolltracker
#plt.plot(toplot,plotassist, label = P3.name)
#plt.legend(loc="upper left")












