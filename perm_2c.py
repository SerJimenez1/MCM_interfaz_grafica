import math
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

class MCM:

    #Atributos de la clase
    __valor_max    = None  #Valor máximo del rango #Rango (MCM Rango)
    __valor_min    = None  #Valor mínimo del rango #Rango (MCM Rango)
    __n1           = None  #Primer número (MCM Simple)
    __n2           = None  #Segundo número (MCM Simple)
    __rango        = None  #Rango (MCM Rango)
    __lista_primos = None  #Lista de números primos
    __mcm          = None  #Resultado MCM
    __fact_primos  = []    #Factores primos
    __ejecutado    = False #Estado de ejecución

    def __es_primo(self,num):  #Método que determinara si un número es primo

        for i in range(2,num):
            if num%i == 0:
                return False
        return True

    def __rango_primos(self, simple = False): #Método para crear un rango de números primos

        lista_primos = []

        if simple == True: #Para MCM simple (2 números)
            for i in range(2, max([self.__n1,self.__n2])+1):
                if self.__es_primo(i):
                    lista_primos.append(i)
            return lista_primos
        
        else:

            for i in range(2,self.__rango[-1]+1):
            #Si el num es primo, se almacena en la lista
                if self.__es_primo(i):
                    lista_primos.append(i)
            return lista_primos
    
    def crear_rango(self,vmin,vmax): #Método para crear el rango para el MCM
        
        if vmax < vmin:
            print("No se pudo crear el rango, el valor máximo debe ser mayor al mínimo")
            return None
        elif type(vmax) != int or type(vmin) != int or vmin <= 0:
            print("No se pudo crear el rango, los valores mínimo y máximo deben ser números naturales mayores a 0")
            return None
        
        self.__valor_max    = vmax
        self.__valor_min    = vmin
        self.__rango        = list(range(self.__valor_min,self.__valor_max + 1)) 
        self.__lista_primos = self.__rango_primos(simple = False)
    
    def calcular(self): #Método para calcular el MCM de un rango de números
        
        self.__fact_primos = []
        if self.__rango == None:
            print("No hay un rango definido para calcular el MCM")
        
        else:
            indice = 0
            r = self.__rango
            self.__mcm = 0
            while {1}  != set(r):
        
                #División de todos los números del rango

                r2 = list(map(lambda x: x/self.__lista_primos[indice] if x%self.__lista_primos[indice] == 0 else x, r)) 

                #Si la nueva lista es igual a la original, se pasa al siguiente primo de la lista

                if r2 == r:
                    indice += 1 
                    continue

                 #Si la nueva lista y la original no son iguales, se agrega el num primo a la lista de factores primos

                self.__fact_primos.append(self.__lista_primos[indice])

                r = r2

            self.__mcm = math.prod(self.__fact_primos)
            self.__ejecutado = True
    
    def calcular_simple(self, n1, n2): #Método para calcular el MCM de dos números

        self.__fact_primos = []
        indice = 0
        self.__n1 = n1
        self.__n2 = n2
        self.__lista_primos = self.__rango_primos(simple = True)
        r = [self.__n1,self.__n2]

        while {1}  != set(r):
    
            #División de ambos números

            r2 = list(map(lambda x: x/self.__lista_primos[indice] if x%self.__lista_primos[indice] == 0 else x, r)) 

            #Si la nueva lista es igual a la original, se pasa al siguiente primo de la lista

            if r2 == r:
                indice += 1 
                continue

                #Si la nueva lista y la original no son iguales, se agrega el num primo a la lista de factores primos

            self.__fact_primos.append(self.__lista_primos[indice])

            r = r2

        self.__mcm = math.prod(self.__fact_primos)
        self.__ejecutado = True

        
    def resultado(self): #Método que regresa el resultado del MCM convertido en string

        if self.__ejecutado == False:
            print("Debe calcular el MCM primero.")

        else:
            return str(self.__mcm)
        

    def info(self, *args): #Imprimir la información que se desea sobre el resultado.
        
        if self.__ejecutado == False:
            print("Debe calcular el MCM primero.")

        else:
            info_rango = f"Rango = {self.__rango}"
            info_mcm = f"Mínimo Común Múltiplo = {self.__mcm}"
            info_vmax = f"Valor máximo del rango = {self.__valor_max}"
            info_vmin = f"Valor mínimo del rango = {self.__valor_min}"
            lista_print = []

            if "vmax" in args:
                lista_print.append(info_vmax)
            if "vmin" in args:
                lista_print.append(info_vmin)
            if "rango" in args:
                lista_print.append(info_rango)
            if "mcm" in args:
                lista_print.append(info_mcm)
            
            for i in lista_print:
                print(i)
        

class Pantalla:

    titulos          = ["BIENVENIDO A LA CALCULADORA DE MCM",                       
                        "MENÚ PRINCIPAL",
                        "MCM DE DOS NÚMEROS",
                        "MCM DE UN RANGO DE NÚMEROS"]
    texto_simple     = ["Ingrese el primer número:", "Ingrese el segundo número:"]
    texto_rango      = ["Ingrese el primer límite:", "Ingrese el segundo límite:"]
    texto_menu       = ["Calcular MCM de dos números", "Calcular MCM de un rango de números", "Salir"]
    texto_error      = "Por favor ingrese un número valido."
    texto_retornar   = "Presione cualquier tecla para regresar al menú principal"

    def __init__(self, stdscr):
        self.stdscr = stdscr
    
    def pantalla_menu(self, fila_seleccionada): #Método para imprimir el menú
        
        #Inicializar paleta de colores
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        altura, ancho = self.stdscr.getmaxyx()

        rectangle(self.stdscr, 3, 3, altura-3, ancho-3) #curses.textpad.rectangle(win, uly, ulx, lry, lrx)

        #Print del título principal
        self.stdscr.addstr(0, ancho//2-len(self.titulos[0])//2, self.titulos[0])
        self.stdscr.addstr(2, ancho//2-len(self.titulos[1])//2, self.titulos[1])

        #Print de las opciones
        for indice, i in enumerate(self.texto_menu):
            x = ancho//2 - len(i)//2
            y = altura//2 - len(self.texto_menu)//2 + indice

            if indice == fila_seleccionada:
              
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, i)
                self.stdscr.attroff(curses.color_pair(1))

            else:
                self.stdscr.addstr(y, x, i)

        self.stdscr.refresh()
    
    def pantalla_mcm(self, mcm, simple = False): #Método para imprimir las pantallas para el cálculo del mcm
        self.stdscr.clear()
        altura, ancho = self.stdscr.getmaxyx()

        #Elección de los títulos
        if simple == True:
            titulo = self.titulos[2]
        else:
            titulo = self.titulos[3]

        self.stdscr.addstr(0, ancho//2-len(titulo)//2, titulo)
        self.stdscr.refresh()

        #Creando ventana
        window = curses.newwin(altura-5, ancho-5, 3, 3) #newwin(int nlines, int ncols, int begin_y, int begin_x)
        window.border()
        _, ancho_W = window.getmaxyx()

        i = 0

        while i < 2:

            #Elección texto input
            if simple == True:
                t = self.texto_simple[i]

            else:
                t = self.texto_rango[i]

            long_cuadro = 4

            posh_texto = ancho_W//2-len(t)//2- long_cuadro      #Posicion horizontal del texto
            posv_texto = 5
            posh1_rect = ancho_W//2+len(t)//2- long_cuadro + 1  #1ra posición horizontal del rectángulo
            posh2_rect = posh1_rect + long_cuadro               #2da posición horizontal del rectángulo

            #Creando ventana para la textbox
            win_text = curses.newwin(1, posh2_rect - posh1_rect, 8, posh1_rect+4) #newwin(int nlines, int ncols, int begin_y, int begin_x)
            box = Textbox(win_text)

            #Creando rectángulo para la textbox
            rectangle(window, posv_texto - 1, posh1_rect, posv_texto + 1, posh2_rect + 1 ) #curses.textpad.rectangle(win, uly, ulx, lry, lrx)
            
            window.addstr(posv_texto, posh_texto, t)
            window.refresh()

            #Input del usuario
            box.edit()

            try:
                texto = int(box.gather())
                
            except ValueError:
                window.addstr(posv_texto + 5, posh_texto, self.texto_error)
                window.refresh()
                win_text.clear()
                continue
            
            if texto <= 0:
                window.addstr(posv_texto + 5, posh_texto, self.texto_error)
                window.refresh()
                win_text.clear()
                continue

            if i == 0:
                num_1 = int(texto)
            else:
                num_2 = int(texto)
            
            i += 1
            
            window.clear()
            window.border()
        
        #Cálculo MCM
        if simple == True:
            mcm.calcular_simple(num_1,num_2)
            resultado = f"El MCM de {num_1} y de {num_2} es: "+ mcm.resultado()

        else:
            mcm.crear_rango(min([num_1,num_2]),max([num_1,num_2]))
            mcm.calcular()
            resultado = f"El MCM desde {min([num_1,num_2])} hasta {max([num_1,num_2])} es: "+ mcm.resultado()

        #Print del resultado en pantalla
        window.addstr(10, ancho_W//2-len(resultado)//2, resultado)
        window.addstr(20, ancho_W//2-len(self.texto_retornar)//2, self.texto_retornar)
        window.refresh()

        window.getch()
    
    def len_menu(self): #Método para retornar la longitud del menú

        return len(self.texto_menu)

#Función principal

def main(stdscr):
    mcm = MCM()
    scr = Pantalla(stdscr)
    curses.curs_set(False)
    
    fila_actual = 0

    scr.pantalla_menu(fila_actual)

    while True:
        key = stdscr.getch()
        stdscr.clear()        

        #Verificando cambio o elección de opción en el menú
        if key == curses.KEY_UP and fila_actual > 0:
            fila_actual -= 1

        elif key == curses.KEY_DOWN and fila_actual < scr.len_menu()-1:
            fila_actual += 1

        elif key == curses.KEY_ENTER or key in [10,13]:

            #Salir
            if fila_actual == scr.len_menu() - 1:
                break

            #MCM DE DOS NÚMEROS
            elif fila_actual == 0:
                scr.pantalla_mcm(mcm, simple=True)

            #MCM DE UN RANGO DE NÚMEROS
            elif fila_actual == 1:
                scr.pantalla_mcm(mcm)

        scr.pantalla_menu(fila_actual)

curses.wrapper(main)