import streamlit as st
import pandas as pd

from collections import namedtuple
import altair as alt
import math

import operator
import matplotlib as plt
import numpy as np
import pygal
import xlrd
from pygal.style import Style


df = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d99.csv',delimiter=';')

df99 = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/d.csv',delimiter=';')

dft = pd.read_csv('https://raw.githubusercontent.com/pablo2343567/streamlit-example/master/t.csv',delimiter=';')



listadeportes = list (dft['Paises'])
listapaises = list (df['Paises'])
 
listaaños = ['R-' , '17' , '18' , '19' , 'T-']




def ListaSoloGanadores():
    """
    Devuelve una lista de diccionarios con clave el deporte y valor el ganador
    """
    res = {}
    for deporte in listadeportes:

        for i in range (len(listapaises)): 
            pos = int ( df99[deporte][i] )
            if pos == 1:
                res[deporte] = listapaises[i]
                
    return res


listaGanadores = ListaSoloGanadores()





def filtro (cadena):
    """
    Dada una cadena de texto, selecciona los deportes que la contienen
    """
    l = []
    for deporte in listadeportes:
        if cadena in deporte:
            l.append(deporte)
    
    return l


def nGanadores(deportes,paises,n=20):
    """
    Devuelve un número n de ganadores por cada deporte. Devuelve un diccionario
    con clave el deporte y con valor un diccionario con clave el país y valor
    la posición de dicho país. 
    """
    res = {}
    for deporte in deportes:
        dicpos = {}
        
        for i in range (len(paises)): 
            pos = int ( df99[deporte][i] )
            if pos != 99 and pos != 0 and pos <= n:
                dicpos[paises[i]] = pos

        valores_ord = dict(sorted(dicpos.items(), key=operator.itemgetter(1)))
        
        res[deporte] = valores_ord
                
    return res
            



def nGanadoresInversa(deportes,paises,n=12):
        """
        Como el diccionario de nGanadores pero da más peso a los primeros 
        """
        a = list (range(1,n+1))
        
        res = {}
        for deporte in deportes:
            dicpos = {}
            
            for i in range (len(paises)): 
                pos = int ( df99[deporte][i] )
                if pos != 99 and pos != 0 and pos <= n:
                    dicpos[paises[i]] = a[-pos]
    
            valores_ord = dict(sorted(dicpos.items(), key=operator.itemgetter(1)))
            
            res[deporte] = valores_ord
                    
        return res






def PaisDeporte (deportes,paises,n=20):
    """
    Diccionario con clave los países y valores un diccionario con el deporte
    y la posición en la que ha quedado. La n indica hasta qué posición se
    aceptan los deportes (con n=2 se seleccionan la primera y la segunda pos)
    """
    res = {}
    for i in range (len(paises)): 
        pais = paises[i]
        dicpos = {}
        
        for deporte in deportes:
            
            pos = int ( df99[deporte][i] )
            if pos != 99 and pos != 0 and pos<=n:
                dicpos[deporte] = pos
                
        valores_ord = dict(sorted(dicpos.items(), key=operator.itemgetter(1)))
        
        res[pais] = valores_ord

    return res




def cantidadMedallas(dic):
    """
    Dado un diccionario de PaisDeporte, devuelve la cantidad de medallas
    de cada país
    """
    res = {}
    for pais in dic:
        res[pais] = len(dic[pais])
        
    return res




    
def dicEvolucionNuevo(deporte, dic):
        listaDeporte = filtro(deporte)
        d={}
        
        def resetLista():
            long = len(listaDeporte)
            lista = []
            for i in range (long):
                lista.append(0)  
            return lista
        
        
        lista = resetLista()
        
        i = 0
        for comp in listaDeporte:

            
            posiciones=dic[comp]
            for pais, pos in posiciones.items():
                if pais not in d:
                    
                    lista = resetLista()
                    
                    lista[i] = pos
                    d[pais] = lista.copy()
                else:
                    acum = d[pais]
                    acum[i] = pos
                    d[pais] = acum
            i += 1
        return d
    
    
    
    
d1 = nGanadores(listadeportes,listapaises)
d2 = PaisDeporte(listadeportes,listapaises,3)

d4 = nGanadoresInversa (listadeportes,listapaises)

d5 = cantidadMedallas(d2)










#----------------------------------------------------------


        # FUNCIONES PARA LAS GRÁFICAS


#--------------------------------------------------------







def graficaPodioDeporte (deport,listadeportes,listapaises):
    """
    Dado un deporte, dibuja un podio to wapo
    """
         
    def dicPuesto(deportes,paises):
        """
        Como el diccionario de nGanadores pero da más peso a los primeros 
        """
        a = list (range(1,4))
        
        res = {}
        for deporte in deportes:
            dicpos = {}
            
            for i in range (len(paises)): 
                pos = int ( df99[deporte][i] )
                if pos != 99 and pos != 0 and pos <= 3:
                    dicpos[paises[i]] = a[-pos]
    
            valores_ord = dict(sorted(dicpos.items(), key=operator.itemgetter(1)))
            
            res[deporte] = valores_ord
                    
        return res
        
    
    
    dic = dicPuesto(listadeportes,listapaises)
    
    
    a = filtro(deport)
    x = len(a)
    i = 0
    for deporte in dic:
        if deporte in a:
            i += 1
            fig = plt.figure(figsize=(10,8))
            st.pyplot(fig)
            plt.title(deporte)
            result = dic[deporte]
            result = pd.Series(result)
            
            coloritos = [0,0,0]
            valores = [0,0,0]
            indices = ['','','']

            for i in range (len(result.values)):
                
                x = result.values[i]
                z = x   
                if x == max(result.values):
                    coloritos[1] = 'gold'
                    valores[1] = z
                    indices[1] = result.index[i]
                elif x == min(result.values):
                    coloritos[2] = 'sienna'
                    valores[2] = z
                    indices[2] = result.index[i]
                else:
                    coloritos[0] = 'grey'
                    valores[0] = z
                    indices[0] = result.index[i]
            plt.bar(indices, valores , color= coloritos)
            plt.show()








def graficaCorrelacion (cat,listadeportes,listapaises,n=20):
    """
    Dada una cadena de texto (nombre de una columna, por ejemplo población '20-Pob')
    y un número de puestos, por ej 3 para seleccionar la cantidad de medallas de
    oro,plata y bronce.
    Calcula la correlación entre la columna y la cantidad de medallas
    """
    
    d2 = PaisDeporte(listadeportes,listapaises,n)
    d5 = cantidadMedallas(d2)
    
    colpoblacion = df[cat].tolist()
    listamedallas = []
    for k,v in d5.items():
        listamedallas.append(v)
        
    seriespob = pd.Series(colpoblacion)
    seriesmed = pd.Series(listamedallas)
    
    corr = round(seriespob.corr(seriesmed),4)
    
    
    plt.figure(figsize=(10,8))
    plt.scatter(colpoblacion,listamedallas) 
    tit = 'Coeficiente de correlación: ' + str(corr)
    plt.title(tit)
    plt.xlabel (cat)
    plt.ylabel('Número de Medallas')
    
    
    
     
    
    
    


def graficoMedallasNMejores(cat,listapaises,a=10):
    """
    Dada una cadena de texto (por ejemplo, 'Baloncesto'), devuelve una
    gráfica círculo con una cantidad 'a' dada de países con su número de
    medallas ganadas en dicho deporte.
    """
     
        
    def eliminar0ySoloNMejor(dic,a=10):
        """
        Función para ordenar los valores con países con más medallas
        y eliminar países con 0 medallas
        """
        aux = {}
        valoresord = dict(sorted(dic.items(), key=operator.itemgetter(1) , reverse = True))
        i = 0
        for k,v in valoresord.items():
            if i >= a:
                break
            if v > 0:
                aux[k] = v
                i += 1
        
        return aux

    
        
    listadeportes = filtro(cat)
    
    d2 = PaisDeporte(listadeportes,listapaises,3)
    
    d5 = cantidadMedallas(d2)
    
    d6 = eliminar0ySoloNMejor(d5,a)
    
    series = pd.Series(d6,copy=True,dtype='float64')
    
    plt.figure (figsize = (10,8))
    
    plt.pie(series.values,labels=series.index, normalize=True)
    plt.axis('equal')
    plt.title(f'Cantidad de medallas en {cat}, {a} países')
    






def graficaPuestos (deport,listadeportes,listapaises,n=20):
    """
    Dado un deporte, selecciona los países ganadores.
    Dado un número, selecciona la cantidad de puestos (si n=2, se seleccionan
    el primero y el segundo del deporte).
    """

    dic = nGanadores(listadeportes,listapaises,n)
    a = filtro(deport)
    x = len(a)
    i = 0
    plt.figure(figsize=(6+x*3, 4+x*2))
    for deporte in dic:
        if deporte in a:
            i += 1
            plt.subplot(x//2 + 1 , x//2 +1 , i)
            plt.title(deporte)
            result = dic[deporte]
            result = pd.Series(result)
            coloritos = ['grey' if (x < max(result.values)) else 'gold' for x in result.values ]
            plt.bar(result.index, result.values , color= coloritos)







def graficaBarraStackeada (deport,listadeportes,listapaises,n=20):
    """
    Dado un deporte, crea un gráfico de barras apilado con la posición de
    cada año en ese deporte, resultando una mayor altura de la barra una mejor
    posición
    """
    
    listaDeporte = filtro(deport)
    paises = []
    dic = dicEvolucionNuevo(deport, nGanadoresInversa(listadeportes, listapaises,n))
    
    for k,v in dic.items():
        paises.append(k)
        x = len(v)

    acumulasion = None
    
    plt.figure (figsize = (10,8))
    for i in range(x):
        valores = []
        for clave,valor in dic.items():
            
            posicion = valor[i]
            valores.append(posicion)
            
        valores = np.array(valores)
        plt.bar (paises,valores,bottom = acumulasion)
        
        if i == 0:
            acumulasion = valores
        else:
            acumulasion += valores
        
    plt.legend(listaDeporte) 
    plt.suptitle(f'Países que han puntuado en {deport}: {n} mejores puestos')
    plt.show()

    
graficaPodioDeporte('Baloncesto ',listadeportes,listapaises)
