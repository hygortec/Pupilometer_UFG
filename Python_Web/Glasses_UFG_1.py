import serial
import os
import time

class Glasses_UFG:

    ini = time.time()

    #porta = '/dev/ttyUSB0' #Porta Linux
    porta = 'COM6' #Porta Windows
    baud_rate = 9600

    Obj_porta = serial.Serial()

    def connect(self, _Porta, _Baud_rate): 
        global Obj_porta 
        self.Obj_porta = serial.Serial(_Porta, _Baud_rate)

    def disconnect(self):
        global Obj_porta
        if(self.Obj_porta.isOpen() == True):
            self.Obj_porta.close()

    ################################ Led red ##########################################
    def led_red(self, _Eye, _LedStatus, _Intensity): 

        global Obj_porta
        try:
            eye = 6
            if(_Eye == 0):
                eye = 6

            else:
                 eye = 1

            intensity = 0
            ledStatus = 00
            if(_LedStatus == True):
                intensity = _Intensity
                ledStatus = 200

            else:
                intensity = 0
                ledStatus = 00

            valor = bytearray([165, eye, intensity, ledStatus])  
            self.Obj_porta.write(valor)

        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
    
    ################################ Led gren #########################################
    def led_gren(self, _Eye, _LedStatus, _Intensity):
        global Obj_porta
        try:

            eye = 7
            if(_Eye == 0):
                eye = 7

            else:
                 eye = 2

            intensity = 0
            ledStatus = 00
            if(_LedStatus == True):
                intensity = _Intensity
                ledStatus = 200

            else:
                intensity = 0
                ledStatus = 00


            valor = bytearray([165, eye, intensity, ledStatus])
            self.Obj_porta.write(valor)

        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")

    ################################ Led blue #########################################
    def led_blue(self, _Eye, _LedStatus, _Intensity):
        global Obj_porta
        try:

            eye = 8
            if(_Eye == 0):
                eye = 8

            else:
                 eye = 3

            intensity = 0
            ledStatus = 00
            if(_LedStatus == True):
                intensity = _Intensity
                ledStatus = 200

            else:
                intensity = 0
                ledStatus = 00


            valor = bytearray([165, eye, intensity, ledStatus]) 
            self.Obj_porta.write(valor)

        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
    
    ################################ Led white #########################################
    def led_white(self, _Eye, _LedStatus, _Intensity):
        global Obj_porta
        try:
            self.led_red(_Eye, _LedStatus, _Intensity)
            self.led_gren(_Eye, _LedStatus, _Intensity)
            self.led_blue(_Eye, _LedStatus, _Intensity)
        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
    
    ################################ Led circle #######################################
    def led_focus(self, _Eye, _LedStatus):
        global Obj_porta
        try:

            eye = 10
            if(_Eye == 0):
                eye = 10

            else:
                 eye = 5

            intensity = 0
            ledStatus = 00
            if(_LedStatus == True): 
                intensity = 2           
                ledStatus = 200

            else:
                intensity = 00
                ledStatus = 00

            valor = bytearray([165, eye, intensity, ledStatus])
            self.Obj_porta.write(valor)

        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
    
    ################################ Led Infra_red ####################################
    def led_infrared(self, _Eye, _LedStatus):
    
       try:

            eye = 9
            if(_Eye == 0):
                eye = 9

            else:
                 eye = 4

            intensity = 0
            ledStatus = 00
            if(_LedStatus == True): 
                intensity = 0           
                ledStatus = 244

            else:
                intensity = 00
                ledStatus = 00

            valor = bytearray([165, eye, intensity, ledStatus])        
            self.Obj_porta.write(valor)

       except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")

    ################################ Beep ####################################
    def beep(self, _Status):
        global Obj_porta
        try:
            intensity = 0
            status = 00
            if(_Status == True): 
                intensity = 2           
                status = 200

            else:
                intensity = 00
                status = 00

            valor = bytearray([165, 11, intensity, status]) 
            self.Obj_porta.write(valor)

        except serial.SerialException:
           print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
    
    ################################ MAIN #############################################

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def ExecuteProtocol(self, _Eye, OnInfraRed, OnCircle, _Protocolo):

        linhas = _Protocolo.split(";")

        if OnInfraRed:
            if _Eye == 2:
                self.led_infrared(0, OnInfraRed) 
                self.led_infrared(1, OnInfraRed)    
            else:
                self.led_infrared(_Eye, OnInfraRed)       

        if OnCircle:
            if _Eye == 2:
                self.led_focus(0, OnCircle)
                self.led_focus(1, OnCircle)
            else:
                self.led_focus(_Eye, OnCircle)

        self.beep(False)
        
        for linha in linhas:
            cor =  linha[len(linha) - 1 : ]
            Time = float(0)            

            if (cor != "R" and cor != "G" and cor != "B" and cor != "W"):
                Time = float(linha)
            else:
                Time = float(linha[0 : len(linha) - 1])           

            if cor == "B":#------------------------------------Azul--------------------------------
                # Ligar o LED do lado esquerdo e direito
                if _Eye == 2:
                    self.led_blue(0, True, 200)
                    self.led_blue(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo e direito
                    self.led_blue(0, False, 0)
                    self.led_blue(1, False, 0)
                    self.beep(False)
                elif _Eye == 1:  
                    # Ligar o LED do lado direito           
                    self.led_blue(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado direito                
                    self.led_blue(1, False, 0)
                    self.beep(False)
                elif _Eye == 0:  
                    # Ligar o LED do lado esquerdo           
                    self.led_blue(0, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo                
                    self.led_blue(0, False, 0)
                    self.beep(False)
            elif cor ==  "G": #------------------------------------Verde--------------------------------------
                # Ligar o LED do lado esquerdo e direito
                if _Eye == 2:
                    self.led_gren(0, True, 200)
                    self.led_gren(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo e direito
                    self.led_gren(0, False, 0)
                    self.led_gren(1, False, 0)
                    self.beep(False)
                elif _Eye == 1:  
                    # Ligar o LED do lado direito           
                    self.led_gren(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado direito                
                    self.led_gren(1, False, 0)
                    self.beep(False)
                elif _Eye == 0:  
                    # Ligar o LED do lado esquerdo           
                    self.led_gren(0, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo                
                    self.led_gren(0, False, 0)
                    self.beep(False)
            elif cor ==  "R":#------------------------------------Vermelho--------------------------------------
                # Ligar o LED do lado esquerdo e direito
                if _Eye == 2:
                    self.led_red(0, True, 200)
                    self.led_red(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo e direito
                    self.led_red(0, False, 0)
                    self.led_red(1, False, 0)
                    self.beep(False)
                elif _Eye == 1:  
                    # Ligar o LED do lado direito           
                    led_red(1, True, 200)
                    beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado direito                
                    self.led_red(1, False, 0)
                    self.beep(False)
                elif _Eye == 0:  
                    # Ligar o LED do lado esquerdo           
                    self.led_red(0, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo                
                    self.led_red(0, False, 0)
                    self.beep(False)
            elif cor ==  "W":#------------------------------------Vermelho--------------------------------------
                 # Ligar o LED do lado esquerdo e direito
                if _Eye == 2:
                    self.led_white(0, True, 200)
                    self.led_white(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo e direito
                    self.led_white(0, False, 0)
                    self.led_white(1, False, 0)
                    self.beep(False)
                elif _Eye == 1:  
                    # Ligar o LED do lado direito           
                    self.led_white(1, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado direito                
                    self.led_white(1, False, 0)
                    self.beep(False)
                elif _Eye == 0:  
                    # Ligar o LED do lado esquerdo           
                    self.led_white(0, True, 200)
                    self.beep(False)
                    time.sleep(Time)  # Tempo 
                    # Desligar o LED do lado esquerdo                
                    self.led_white(0, False, 0)
                    self.beep(False)
            else:
                time.sleep(Time)  # Tempo 

        self.led_infrared(0, False) 
        self.led_infrared(1, False) 
        self.led_focus(0, False)
        self.led_focus(1, False)
        return


if __name__=='__main__':

    c = Glasses_UFG()

    
    c.connect("COM6", 9600)
    c.beep(True)
    time.sleep(0.1)
    c.beep(False)
    time.sleep(0.1)
    c.beep(True)
    time.sleep(0.1)
    c.beep(False)
    #ExecuteProtocol(2, True, True, "90;1W;300")
    c.disconnect()
    