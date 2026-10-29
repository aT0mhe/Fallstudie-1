# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 15:23:59 2026

@author: tom2h
"""
import pandas as pd
# DME - Fallstudie
# Zweistufige Synthese von DME aus Synthesegas
# Stoffbilanz ohne Recycle 

# 1. Anlagenparameter 

produktion = 100000             #t/a
betriebsstunden = 8000          #h/a

# 2. Stoffdaten

M_DME = 46.07                   #kg/kmol

# 3. Reaktionsparameter

X1 = 0.50                       #CO-Umsatz
S1 = 0.97                       #Methanolselektivität 
Y1 = X1 * S1

X2 = 0.80                       #Methanolumsatz
S2 = 0.999                      #DME-Selektivität
Y2 = X2 * S2

# 3.1. Rückführung 

R_Methanol = 1

R_CO = 0.90

# 4. Bilanzierung 

# Im Folgenden wird die Zweistufige Synthese von DME aus Synthesegas 
# betrachtet. Das Verfahren wird hierbei mit der gewünschten Produktion
# bilanziert. 

# 4.1. Produktion von DME

m_DME = produktion * 1000 / betriebsstunden     #kg/h 

n_DME = m_DME / M_DME                           #kmol/h

# 4.2. Zweiter Schritt: DME-Synthese aus Methanol 

n_Methanol_R2_theoretisch = n_DME * 2           #kmol/h
# Hier wurde die Stöchiometrie von Methanol zum Methanol beachtet

n_Methanol_R2_ein = n_Methanol_R2_theoretisch / Y2            #kmol/h
# Nur 80% des eintretenden Methanols reagieren

n_Methanol_R2_aus = n_Methanol_R2_ein * (1-X2)     #kmol/h
#Methanol, dass den Reaktor unreagiert verlässt 

n_Methanol_R2_Nebenreaktionen = n_Methanol_R2_ein * X2 * (1-S2) #kmol/h
#Stoffmenge des Methanols, welches in Nebenreaktionen umgesetzt wird

n_H20_R2 = n_DME                                   #kmol/h

# 4.2.1 Methanolrecycle

n_Methanol_Recycle = n_Methanol_R2_aus * R_Methanol       #kmol/h

n_Methanol_purge = n_Methanol_R2_aus * (1-R_Methanol)

n_Methanol_R1_aus = n_Methanol_R2_ein - n_Methanol_Recycle

n_H20_purge = n_H20_R2 * (1-R_Methanol)

n_H20_Recycle = n_H20_R2 * R_Methanol

# 4.3. Erster Schritt: Methanolsynthese aus Synthesegas 

n_CO_R1_ein = n_Methanol_R1_aus / Y1           #kmol/h

n_CO_umgesetzt = n_CO_R1_ein * X1

n_CO_R1_aus = n_CO_R1_ein - n_CO_umgesetzt

n_CH4_R1 = n_CO_umgesetzt * (1-S1)

n_CH4_R1_aus = n_CO_umgesetzt * (1-S1) * R_CO

n_H20_R1 = n_CH4_R1

n_H20_Mischer = n_H20_Recycle + n_H20_R1

n_H2_R1_Ein = 2 * n_Methanol_R1_aus + 3 * n_CH4_R1

# 4.3.1 Synthesegasrecycle

n_CO_Recycle = n_CO_R1_aus * R_CO         #kmol/h

n_CO_purge = n_CO_R1_aus * (1-R_CO)

n_CO_R1_frisch = n_CO_R1_ein - n_CO_Recycle

n_CH4_Recycle = n_CH4_R1 * R_CO

n_CH4_purge = n_CH4_R1 * (1-R_CO)

# Ergebnisse 

print("DME-Fallstudie")
print("Zweistufige Synthese von DME aus Synthesegas")


# 5. Stoffstromtabelle

# 5.1. Eintritt Mischer 1 (S1)
S1 = {
      "CO": n_CO_R1_frisch, 
      "H2": n_H2_R1_Ein,
      "Methanol": 0, 
      "CH4": 0, 
      "DME": 0,
      "H2O": 0, 
      }
# 5.2. Eintritt Methanolreaktor (S2)
S2 = {
      "CO": n_CO_R1_ein,
      "H2": n_H2_R1_Ein, 
      "Methanol": 0, 
      "CH4": n_CH4_Recycle,
      "DME": 0,
      "H2O": 0 
      }
#5.3. Austritt Methanolreaktor (S3) 
S3 = {
      "CO": n_CO_R1_aus, 
      "H2": 0, 
      "Methanol": n_Methanol_R1_aus,
      "CH4": n_CH4_R1, 
      "DME": 0, 
      "H2O": n_H20_R1
      }
#5.4. Austritt Flashabscheider 1 (S4)
S4 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_R1_aus, 
      "CH4": 0,
      "DME": 0, 
      "H2O": n_H20_R1
      }
#5.5. Austritt Mischer 2 (S5)
S5 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_R2_ein, 
      "CH4": 0,
      "DME": 0, 
      "H2O": n_H20_Mischer
      }
#5.6. Austritt Kopf Rektifikation 1 (S6)
S6 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_R2_ein, 
      "CH4": 0,
      "DME": 0, 
      "H2O": 0
      }
#5.7. Wasserstrom aus Rektifikation 1 (S7)
S7 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": 0, 
      "CH4": 0,
      "DME": 0, 
      "H2O": n_H20_Mischer
      }
#5.8. Eintritt Reaktor 2 (S8)
S8 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_R2_ein, 
      "CH4": 0,
      "DME": 0, 
      "H2O": 0
      }
#5.9. Recycle zu Mischer 1 (S9)
S9 = {
      "CO": n_CO_Recycle, 
      "H2": 0, 
      "Methanol": 0, 
      "CH4": n_CH4_Recycle,
      "DME": 0, 
      "H2O": 0
      }
#5.10. Purge aus Recycle 1 (S10)
S10 = {
      "CO": n_CO_purge, 
      "H2": 0, 
      "Methanol": 0, 
      "CH4": n_CH4_purge,
      "DME": 0, 
      "H2O": 0
      }
#5.11. Recycle zu Mischer 2 (S11)
S11 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_Recycle, 
      "CH4": 0,
      "DME": 0, 
      "H2O":n_H20_Recycle
      }
#5.12. Purge aus Recycle 2 (S12)
S12 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": n_Methanol_purge, 
      "CH4": 0,
      "DME": 0, 
      "H2O":n_H20_purge
      }
#5.13. Produktstrom (S13)
S13 = {
      "CO": 0, 
      "H2": 0, 
      "Methanol": 0, 
      "CH4": 0,
      "DME": n_DME, 
      "H2O": 0
      }
stoffstroeme = pd.DataFrame({
    "S1 - Eintritt Mischer 1": S1, 
    "S2 - Eintritt Reaktor 1": S2, 
    "S3 - Austritt Reaktor 1": S3,
    "S4 - Eintritt Mischer 2": S4,
    "S5 - Austritt Mischer 2": S5,
    "S6 - Kopfprodukt Rektifikation 1": S6,
    "S7 - Wasserstrom Rektifikation 1": S7,
    "S8 - Eintritt Reaktor 2": S8,
    "S9 - Recycle Synthesegas": S9,
    "S10 - Purge Synthesegas": S10,
    "S11 - Recycle Methanol": S11,
    "S12 - Purge Methanol": S12,
    "S13 - Produktstrom": S13
    })

print("\nStoffstromtabelle [kmol/h]")
print(stoffstroeme.round(2))
