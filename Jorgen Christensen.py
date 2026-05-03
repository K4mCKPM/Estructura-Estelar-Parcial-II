# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:55:31 2026

@author: KamCKPM
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid, cumulative_trapezoid

sns.set_theme(style="darkgrid")
sns.set_context("poster")
ruta = r"K:\Universidad\7mo Semestre\Stellar Structure\Jorgen Christensen.txt"

### Valores:
Radio_sol = 6.96340e8   #                               (m)
Masa_Solar = 1.989e30   #                               (kg)
G = 6.674e-11           #Constante de Newton-Cavendish  (m^3 s^-2 kg^-1)


### Lectura del archivo de datos:    
with open(ruta, "r") as f:
    lineas = f.readlines()
    
datos = [linea.split() for linea in lineas[1:]] 
nombres = ["r/R",   "c (cm/sec)",  "rho (g/cm^3)", "p (dyn/cm^2)", "Gamma_1",   "T (K)"]
df = pd.DataFrame(datos, columns=nombres)
df = df.apply(pd.to_numeric, errors="coerce")


### Se definen las variables de integración
x = df["r/R"]                           #Se guarda la distancia radial adimensional
rho = df["rho (g/cm^3)"]*(100**3)/1000  #Se convierte la densidad a kg/m^3

idx = np.argsort(x) #Se usa para organizar los valores desde el centro a la superficie.
x = x[idx]          
rho = rho[idx]


### Integrales
#- Masa encerrada en un radio
Funcion_masa = x**2 * rho
m_x = cumulative_trapezoid(Funcion_masa, x, initial=0)

Masa_S = m_x[-1] * 4 * np.pi * Radio_sol**3
errorsito = abs(Masa_Solar - abs(Masa_S))*100/Masa_Solar
M_encerrada = m_x * 4 * np.pi * Radio_sol**3

print(f"""El valor calculado de la masa para un R de configuración como el 
radio solar es: {Masa_S:.3E} m, que comparando con el valor real, 
que es: {Masa_Solar:.3E} m, obtenemos un error relativo del {errorsito:.2f} %""")
      
#- Potencial gravitatorio para una masa encerrada
Funcion_pot_grav = m_x * x * rho
Int_Omega = trapezoid(Funcion_pot_grav, x)

Omega = Int_Omega * G * 16 * np.pi**2 * (Radio_sol**5)

print(f"\nEl valor del factor de concentración de masa es {Radio_sol * Omega / (G * M_encerrada[-1]**2):.3f}")


### Gráficas
def Densidad(x=x, rho=rho):
    sns.lineplot(x = x, y = rho, color="darkgreen")
    plt.xlabel("Radio adimensional")
    plt.ylabel(r"Densidad [kg $\cdot$ m$^{-3}$]")
    plt.show()

def dif_masa(x=x, Curva=Funcion_masa):
    sns.lineplot(x = x, y = Curva, label=f"Integral bajo la curva = {m_x[-1]:.4E}", color="crimson")
    plt.xlabel("Radio adimensional")
    plt.ylabel("Continuidad de masa [kg $\cdot$ m$^{-3}$]")
    plt.show()

def Masa(x=x, M_encerrada=M_encerrada):
    sns.lineplot(x = x, y = M_encerrada, color="royalblue")
    plt.xlabel("Radio adimensional")    
    plt.ylabel("Masa encerrada en el radio [kg]")
    plt.show()

### Descomentar las siguientes funciones dependiendo de la gráfica que desee.
#Densidad()                 #Densidad vs Radio 
#dif_masa()                 #Continuidad de masa vs Radio
#Masa()                     #Masa vs Radio
