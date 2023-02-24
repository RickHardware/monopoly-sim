import numpy as np
import pandas as pd
import random as rd
import Player as plr
import MonoUtils as MU
import matplotlib.pyplot as plt


class Game:
    def __init__(self,TurnLimit):
        self.TurnLimit =TurnLimit
        self.ownedprops = []
        self.ownersofprops = []
        self.board = pd.read_csv("Monoboard.csv")
        

    def PlayAGame(self, player1, player2, player3):
        Turn = 1
        playerlist = [player1, player2, player3]
        plotassist = np.arange(1,self.TurnLimit +1)
        payToString = ""
        payFromstring = ""
        bankruptcheck = 0


        while(Turn<=(self.TurnLimit) and bankruptcheck == 0):             
            for player in playerlist:
                newturninfo = player.TakeYourTurn(self.board, self.ownedprops, self.ownersofprops)

                Board = newturninfo[0]
                #print(len(newturninfo), "length")
                #print(newturninfo[1], "look at this")
                self.ownedprops = newturninfo[1]
                self.ownersofprops = newturninfo[2]
                rent = newturninfo[3]
                rentTo = newturninfo[4]
                rentFrom = newturninfo[5]
                #Pay all the rent
                for player in playerlist:
                    if player.name == rentTo:
                        player.Cash += rent
                        payFromstring = player.name + " receives " + str(rent) + " from "
                    if player.name ==rentFrom:
                        player.Cash -=rent
                        payToString = player.name 
                print(payFromstring + " " + payToString)
                print("END TURN")
            #bankrupt check:
            numbankrupt = 0
            for player in playerlist:
                if player.bankrupt >0:
                    numbankrupt +=1
            if numbankrupt == len(playerlist)-1:
                print("Only one remains:")
                for player in playerlist:
                    if player.bankrupt ==0:
                        winner = player
                        print("By Default, Winner = " + winner.name + " with "+ str(int(winner.Cash)) )
                        print("portfolio = ")
                        for i in range(0, len(winner.Properties)):
                            print(Board["Name"][winner.Properties[i]])
                        print(self.ownedprops)
                        print(self.ownersofprops)
                        return()

            elif numbankrupt == len(playerlist):
                print("All players are bankrupt, game ends on turn " + str(Turn))
                bankruptcheck = 1
            else:
                Turn+=1
            print("Turn Number = " + str(Turn))



        if player1.Cash == player2.Cash and player1.Cash ==player3.Cash:
            print("DRAW")
        else:
            if player1.Cash > player2.Cash:
                if player1.Cash>player3.Cash:
                    winner = player1
                else:
                    winner = player3
            else: 
                winner = player2                   
            print("Winner = " + winner.name + " with "+ str(int(winner.Cash)) )
            print("portfolio = ")
            for i in range(0, len(winner.Properties)):
                print(Board["Name"][winner.Properties[i]])
        #    print(winner.Properties)
            toplot = player1.cashtracker
            #print(toplot)
            plt.plot(plotassist,toplot, label = player1.name)
            toplot = player2.cashtracker
           # print(toplot)
            plt.plot(plotassist,toplot, label = player2.name)
            toplot = player3.cashtracker
        #    print(toplot)
            plt.plot(plotassist,toplot, label = player3.name)
            plt.legend(loc="upper left")
