import numpy as np
import pandas as pd
import random as rd
#import matplotlib.pyplot as plt
import Player as plr
import Game as gme
import MonoUtils as MU

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

P1 = plr.Player("Tom")
P2 = plr.Player("Dick")
P3 = plr.Player("Harry")

Game1 = gme.Game(100)
Game1.PlayAGame(P1,P2,P3)













