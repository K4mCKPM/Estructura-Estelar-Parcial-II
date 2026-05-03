# -*- coding: utf-8 -*-
"""
Created on Sat May  2 23:40:54 2026

@author: KamCKPM
"""
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")
sns.set_context("poster")

### Valores:
Masa_Solar = 1.989e30   #                               (kg)
m_H = 1.674e-27         #Masa de un átomo de hidrógeno  (kg)
k_B = 1.38e-23          #Constante de Boltzmann         (J K^-1) 
a = 7.56e-16            #Constante de Radiación         (J m^-3 K^-4)
G = 6.674e-11           #Constante de Newton-Cavendish  (m^3 s^-2 kg^-1)

B = np.pi * a * G**3 * Masa_Solar**2 * m_H**4 / (18 * k_B**4)

### Parámetros
Valores_x = np.linspace(1e-6, 9, 1000)
Valores_mu = [0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]

### Solución cotas superiores
def masa_en_funcion_de_x(x, mu):
    return np.sqrt(x / (B * mu**4 * (1-x)**4))

### Curvas
for mu in Valores_mu:
    M_M_sol = masa_en_funcion_de_x(Valores_x, mu)       #Masa estrella / Masa solar
    plt.plot(M_M_sol, Valores_x, label= rf"$\mu_c$ = {mu:.2f}")

m_sol = masa_en_funcion_de_x(Valores_x, 0.62)           #Para mu = 0.62 del sol ionizado
plt.plot(m_sol, Valores_x, linestyle='-.', color="crimson", label = r"$\mu_{c \odot}$= 0.62")

### Ajustes gráfico
plt.xlabel(r'$M_{\star}/M_{\odot}$')
plt.ylabel(r'Cota superior $x = 1-\beta_{\star}$')
plt.title('Fracción de Presión de Radiación en el Centro')
plt.xlim(-2, 80) 
plt.ylim(-0.05, 0.85) 
plt.axhline(y=0.5, color="blue", linestyle="--", lw=3   , label=r"$1 - \beta^\ast$= 0.5")
plt.fill_between([-2, 200], 0.5, 0.85, color='red', alpha=0.1)
plt.legend()
plt.show()