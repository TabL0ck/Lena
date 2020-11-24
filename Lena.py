import os
import sys
sys.path.append('/home/lena/Pomichnik/modules/Lena_small_def')
sys.path.append('/home/lena/Pomichnik/modules/execute_cmd')
import webbrowser
import speechd
import datetime
import simpleaudio
import speech_recognition
import time
import Lena_small_def
import Lena_cmd
opts = {
	"alias": ('кариночка','камышка','мариночка','п****','галиночка','алёна','лена','леночка','алёночка','алиночка','алина','лерочка','ариночка'),
	"cmd":{
		"ctime":('время','времени','час'),
		"rty":('повтори','повторим','повторяй','повторили','повторяю'),
		"repeat":('скажи', 'произнеси', 'скажем','сказать','скажу'),
		"clock":('будильник','поставь'),
		"write":('запиши','каво'),
		"read":('прочти','прочитай','школа')
	},
	"gog": ('скажи','произнеси','скажем','сказать','скажу','будильник','поставь'),
	"times":('на','часов','минут')
}
def search_Micro():
	for index,name in enumerate(speech_recognition.Microphone.list_microphone_names()):
		print('Microphone with name \'{}\' found for Microphone(device_index = {})'.format(name,index))
	choosen_one = int(input('Input index of your main Microphone: '))
	return choosen_one

class LenO4KA:

	def __init__(self):
		self.google = ''
		self.hours = 60
		self.minutes = 60
		self.retry = ''
		self.clock_active = False
		self.pizdesh = False
		self.file_one = ''

	def Lena_golos(self,text):
		Lena.speak(text)
		time.sleep(len(text)*0.1)

	def callback(self,recognizer,audio):
		try:
			voice = recognizer.recognize_google(audio,language="ru-RU").lower()
			print("[log] Распознано: " + voice)
			if self.pizdesh == True:
				self.write_file_one(voice+'\n')
			cmd = Lena_small_def.delete_text_before_command(voice,opts['alias'])
			if cmd == None:
				return
			temp = Lena_small_def.delete_trash(cmd,opts['gog'])
			temp = Lena_small_def.recognize_cmd(cmd,opts['cmd'])
			if temp['cmd'] == 'rty':
				self.execute_cmd(self.get_retry())
			else:
				google = cmd
				google = Lena_small_def.delete_trash(google,opts['gog'])
				cmd =  Lena_small_def.recognize_cmd(cmd,opts['cmd'])
				self.set_google(google)
				self.execute_cmd(cmd['cmd'])
				self.set_retry(cmd['cmd'])
		except speech_recognition.UnknownValueError:
			print("[log] Голос не распознан!")
		except speech_recognition.RequestError as e:
			self.Lena_golos("Неизвестная ошибка, проверьте интернет")
			os.system('shutdown now')

	def execute_cmd(self,cmd):
		if cmd == 'ctime':
			self.Lena_golos('Сейчас ' + Lena_cmd.ctime_hours() + ':' + Lena_cmd.ctime_minutes())
		elif cmd == 'repeat':
			self.Lena_golos(self.get_google())
		elif cmd == 'clock':
			self.set_google(Lena_small_def.delete_trash(self.google,opts['times']))
			self.set_google(self.google.replace(':'," ").strip())
			time = Lena_cmd.clock(self.get_google())
			if time[0] == 60:
				self.Lena_golos('Простите, но я не могу поставить будильник на несуществующее время')
				return
			self.Lena_golos('Ставлю будильник на '+str(time[0])+' часов: '+str(time[1])+' минут')
			self.set_hours(time[0])
			self.set_minutes(time[1])
			self.set_clock_active(True)
			os.system("amixer sset 'Master' 100%")

		elif cmd == 'write':
			self.set_pizdesh(True)
			self.open_with_write_file_one()
			self.Lena_golos('Записываю')
		elif cmd == 'read':
			self.set_pizdesh(False)
			self.close_file_one()
			self.open_with_read_file_one()
			self.Lena_golos(self.read_file_one())
			self.close_file_one()
			os.system('rm /home/lena/Pomichnik/text/pizdesh.txt')
		else:
			print("[log] Команда не распознана")

	def set_google(self,google):
		self.google = google
	def get_google(self):
		return self.google

	def set_hours(self,hours):
		self.hours = hours
	def get_hours(self):
		return self.hours

	def set_minutes(self,minutes):
		self.minutes = minutes
	def get_minutes(self):
		return self.minutes

	def set_retry(self,retry):
		self.retry = retry
	def get_retry(self):
		return self.retry

	def set_clock_active(self,clock_active):
		self.clock_active = clock_active
	def get_clock_active(self):
		return self.clock_active

	def set_pizdesh(self,value):
		self.pizdesh = value
	def get_pizdesh(self):
		return self.pizdesh

	def open_with_read_file_one(self):
		self.file_one = open('/home/lena/Pomichnik/text/pizdesh.txt','r')
	def open_with_write_file_one(self):
		self.file_one = open('/home/lena/Pomichnik/text/pizdesh.txt','w')
	def write_file_one(self,text):
		self.file_one.write(text)
	def read_file_one(self):
		return self.file_one.read()
	def close_file_one(self):
		self.file_one.close()

#запуск
Lena = speechd.SSIPClient('test')
Lena.set_output_module('rhvoice')
Lena.set_language('ru')
Lena.set_rate(10)
Lena.set_volume(100)
Lena.set_synthesis_voice('Anna')
Lena.set_punctuation(speechd.PunctuationMode.SOME)
index = search_Micro()
r = speech_recognition.Recognizer()
m = speech_recognition.Microphone(device_index = index)

with m as source:
	r.adjust_for_ambient_noise(source)

os.system('clear')
Assistent = LenO4KA()
Assistent.Lena_golos('Привет, хозяин, слушаю вас')

while True:
	print('Vvedyte komandu')
	with m as source:
		audio = r.listen(source, phrase_time_limit = 8)
	Assistent.callback(r,audio)
	if Assistent.get_clock_active():
		Assistent.set_clock_active(Lena_cmd.alarm(Assistent.hours, Assistent.minutes))
