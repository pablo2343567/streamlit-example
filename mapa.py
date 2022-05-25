

import streamlit as st
import pandas as pd

import math

import operator
import matplotlib as plt
import matplotlib.pyplot as plt

import numpy as np


import pygal
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



def Mapa (listadeportes,listapaises,nPrimeros,top=False,titulo='Medallas'):

    d2 = PaisDeporte(listadeportes,listapaises,nPrimeros)
    
    d5 = cantidadMedallas(d2)
    
    
    
    def diccionarioCodigos():
        asd = df99['cod'].tolist()
        
        diccodigo = {}
    
        for codigo in asd:
            i = asd.index(codigo)
            pais = listapaises[i]
            diccodigo[pais] = codigo
        
        return diccodigo
    
    
    
    
    def dicValoresParaPlotear (dic):
        
        res = {}
        for pais,medallas in dic.items():
            if pais in diccodigo:
                codigo = diccodigo[pais]
                res[codigo] = medallas
                
        resord = dict(sorted(res.items(), key=operator.itemgetter(1) , reverse = True))       
        
        return resord
                
    
    
    
        
    diccodigo = diccionarioCodigos()
    
    dicValoresPlotear = dicValoresParaPlotear(d5)
    
    
    if top:
        custom_style = Style(colors = ('#FFFF00','#867F88','#E45C13'))
    else:
        custom_style = Style(colors = ('#FF0000','#867F88','#E45C13'))
    
    
    pygal.maps.world.World()
      
    
    worldmap.title = 'Cantidad de Medallas por pais'
      
    
    
     
    
    mejores = {}
    
    
    if top:
        i = 0
        for k,v in dicValoresPlotear.items():
            if i == 3:
                worldmap.add('Top 3',mejores)
                mejores = {}
            if i == 10:
                worldmap.add('Top 10',mejores)
                break
            
            if v != 0:
                mejores[k] = v
            i += 1
        
    
        worldmap.add('Resto', dicValoresPlotear)
    
    else:
        
        worldmap.add('Medallas',dicValoresPlotear)
      
    
    
    
    
    
    worldmap.render_in_browser()

    
   

Mapa (listadeportes,listapaises,3,True,'Cantidad de Medallas por pais')
                 
                    
    
opcion = st.selectbox('Selecciona una modalidad',listadeportes)




st.text ('El valor de 3 corresponde al primer puesto, 2 para el segundo y 3 para el tercero')
