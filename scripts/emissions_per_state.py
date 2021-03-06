import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## read data
path = "git/CarbonFootprintAGU/data/"
df = pd.read_csv(path+"locations.csv")
nlocs = len(df)

## PER STATE

states = []              # list of countries / states in USA
n_per_state = []          # number of attendees per country
emissions = []              # total emissions per country

for i in range(nlocs):
    n = df["N"][i]
    dist = df["dist"][i]
    country = df["country"][i]
    state = df["state"][i]
    
    if country == "United States":
    
        if dist < 400:       # BUS / TRAIN / CAR at 60gCO2e / km / person
            e = dist*2*n*0.06      # kgCO2e
        elif dist < 1500:    # SHORT HAUL FLIGHT at 200gCO2e / km / person
            e = dist*2*n*0.2
        elif dist < 8000:    # LONG HAUL FLIGHT at 250gCO2e / km / person
            e = dist*2*n*0.25
        else:                # SUPER LONG HAUL at 300gCO2e / km / person
            e = dist*2*n*0.3
        
        if state not in states:
            states.append(state)
            n_per_state.append(n)
            emissions.append(e)
        else:
            n_per_state[-1] += n
            emissions[-1] += e
    

## sort them
sortarg = np.argsort(np.array(emissions))
states_sorted = np.array(states)[sortarg][::-1]
e_sorted = np.array(emissions)[sortarg][::-1]/1000  # tCO2e
n_sorted = np.array(n_per_state)[sortarg][::-1]
pce_sorted = e_sorted / n_sorted

## save to csv
csvout = open(path+"emissions_per_state.csv","w")
csvout.write("state,N,emissions [tCO2e],emissions_per_capita [tCO2e]\n")
for i,state in enumerate(states_sorted):
    csvout.write(",".join([state,str(n_sorted[i]),str(e_sorted[i]),str(pce_sorted[i])]))
    csvout.write("\n")
    
csvout.close()

    