from math import exp,sqrt,log
import numpy as np
from scipy.stats import norm
from tabulate import tabulate


                                                        #MODELO BINOMIAL
print('                                    MODELO BINOMIAL')

#TIPO DE OPCION: EUROPEO=1, AMERICANO=2
tipo=1
#Precio al día de hoy
S0=200
#TASA LIBRE DE RIESGO (en decimal)
r=.12
#TIEMPO TOTAL DE LA OPCION EN MESES
T=5
#NÚMERO DE PERIODOS
n=7
#PRECIO DE EJERCICIO
k=203
#PORCENTAJE DE SUBIDA O VOLATILIDAD:
var=0 #Decimales de SUBIDA, si se tiene volatilidad poner 0
var1=0 #Decimales de BAJADA, si se tiene volatilidad poner 0
sigma=0.43 #Si se tiene u, poner 0. Si se tiene volatilidad poner en decimales

def binomial(tipo,S0,r,T,n,k,var,var1,sigma):
    deltat=((T/n)/12)
    if var!=0: #si se tiene u
        u=1+var
        d=1-var1
    else: #si se tiene volatilidad
        u=exp(sigma*sqrt(deltat))
        d=exp(-(sigma*sqrt(deltat)))
    
    precios=np.zeros((n+1,n+1)) #diagrama vacio para poner posibles precios
    p=(exp(r*deltat)-d)/(u-d) #probabilidad (p)
    print('\nu:',u,'\nd:',d,'\np:',p)
    
    #Para imprimir precios de acciones en cada tiempo:
    #[columna, fila], comienza en 0 
    for i in range(n+1):
        for j in range(i,n+1):
            precios[i][j]=S0*(u**(j-i))*(d**i)
    print('Posibles precios del mercado: \n',tabulate(precios))
    
    #PRIMERO CALCULAR LA OPCIÓN CALL:
    print('\nCALL:')
    arbolc=np.zeros((n+1,n+1)) #diagrama vacio para poner posibles precios
    for i in range(n+1):
        arbolc[i,n]=max((precios[i,n]-k),0)      
    #Calcular precios de la opcion en cada momento:
    for i in range(n+1):
        for j in range(n-i):
            arbolc[j,n-i-1]=exp((-r)*deltat)*((arbolc[j,n-i]*p)+(arbolc[j+1,n-i]*(1-p)))
    if tipo==1: #Europeo
        print('Precios en cada momento para opción Call: \n',tabulate(arbolc))
        print('El precio de la opción Call Europero es',arbolc[0,0])
    else: #Si la opcion es americana:
        for i in range(n+1):
            for j in range(n-i):
                arbolc[j,n-i-1]=exp((-r)*deltat)*((arbolc[j,n-i]*p)+(arbolc[j+1,n-i]*(1-p)))
                if arbolc[j,n-i-1]<=max((precios[j,n-i-1]-k),0): #Comparar el precio actual con ganancias
                    arbolc[j,n-i-1]=max((precios[j,n-i-1]-k),0) #si es así se cambia
        print('Precios en cada momento para opción Call: \n',tabulate(arbolc))
        print('El precio de la opción Call Americano es',arbolc[0,0])


    #AHORA OPCIÓN PUT:
    print('\nPUT:')
    arbolp=np.zeros((n+1,n+1)) #diagrama vacio para poner posibles precios
    for i in range(n+1):
        arbolp[i,n]=max((k-precios[i,n]),0)      
    #Calcular precios de la opcion en cada momento:
    for i in range(n+1):
        for j in range(n-i):
            arbolp[j,n-i-1]=exp(-r*deltat)*((arbolp[j,n-i]*p)+(arbolp[j+1,n-i]*(1-p)))
    
    if tipo==1: #Europeo
        print('Precios en cada momento para opción Put: \n',tabulate(arbolp))
        print('El precio de la opción Put Europero es: ',arbolp[0,0])
    else: #Si la opcion es americana:
        for i in range(n+1):
            for j in range(n-i):
                arbolp[j,n-i-1]=exp(-r*deltat)*((arbolp[j,n-i]*p)+(arbolp[j+1,n-i]*(1-p)))
                if arbolp[j,n-i-1]<=max((k-precios[j,n-i-1]),0): #Comparar el precio actual con ganancias
                    arbolp[j,n-i-1]=max((k-precios[j,n-i-1]),0) #si es así se cambia
        print('Precios en cada momento para opción Put: \n',tabulate(arbolp))
        print('El precio de la opción Put Americano es',arbolp[0,0])

    #¿SATISFACE PARIDAD?:
    if tipo==1:
        print('\nPARIDAD:')
        a=arbolc[0,0]+k*exp((-r)*(T/12))
        b=arbolp[0,0]+S0
        print(a,'=',b)
        if (a-b)<1*exp(-9) or a-b==0:
            print('Cumple con ecuación de paridad')
        else:
            print('NO cumple con ecuación de paridad')
binomial(tipo,S0,r,T,n,k,var,var1,sigma)



                                            #MODELO BLACK & SCHOLES
print('\n\n                                    MODELO BLACK & SCHOLES')
#Precio inicial
s0=200
#Precio de ejercicio
k=203
#Tiempo de la opcion en meses
T=5
#Volatilidad
sigma=.43
#tasa liBre de riesgo
r=.12

def ByS(S0,T,sigma,k,r):
    t=T/12
    d1=(log(s0/k)+(r+(sigma**2/2))*t)/(sigma*sqrt(t))
    d2=d1-sigma*sqrt(t)
    print('CALL')
    c=s0*norm.cdf(d1)-k*exp(-r*t)*norm.cdf(d2)
    print(c)
    print('\nPUT')
    p=k*exp(-r*t)*norm.cdf(-d2)-s0*norm.cdf(-d1)
    print(p)

    print('\nPARIDAD:')
    a=c+k*exp(-r*t)
    b=p+s0
    print(a,'=',b)
    if (a-b)<1*exp(-9) or a-b==0:
        print('Cumple con ecuación de paridad')
    else:
        print('NO cumple con ecuación de paridad')
ByS(S0,T,sigma,k,r)







