import streamlit as st
import pandas as pd

from collections import namedtuple
import altair as alt
import math

import operator
import matplotlib as plt
import matplotlib.pyplot as plt

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
    
    
    
    




#----------------------------------------------------------


        # FUNCIONES PARA LAS GRÁFICAS


#--------------------------------------------------------






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
    if len(listadeportes) == 0:
        st.text('Error, deporte no válido')
    else:
        d2 = PaisDeporte(listadeportes,listapaises,3)

        d5 = cantidadMedallas(d2)

        d6 = eliminar0ySoloNMejor(d5,a)

        series = pd.Series(d6,copy=True,dtype='float64')

        fig = plt.figure ()

        plt.pie(series.values,labels=series.index, normalize=True)
        plt.axis('equal')
        plt.title(f'Mostrando un total de hasta {a} países con más medallas en {cat}')

        st.pyplot(fig)
    
        st.text('Teniendo en cuenta las modalidades de')
        for deporte in listadeportes:
            st.text(deporte)
    
    
   


agree = st.checkbox('¿Quieres seleccionar los deportes por código? Ej: escribir M para todas las modalidades de Masculino', value=False)                    
                    
listaopciones = ['A4','Baloncesto','Balonmano','Ciclo','Doma','Espada','Florete','Futbol','Gim','Hockey','K4','N','Rugby','Sable','Salto','Volei','Wax','Waterpolo']

if not agree:
    opcion = st.selectbox('Selecciona uno de los siguientes deportes:',options=listaopciones,index = 2)
else:
    opcion = st.text_input('Escribe un deporte codificado:')




n = st.select_slider('Selecciona la cantidad de países a mostrar', options=range(1,9),value = 4)

graficoMedallasNMejores (opcion,listapaises,n)


