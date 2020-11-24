import datetime
import simpleaudio

opts = {
	"minutes":('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60'),
	"hours":('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24')

}

def ctime_hours():
	now = datetime.datetime.now()
	return str(now.hour)
def ctime_minutes():
	now = datetime.datetime.now()
	return str(now.minute)


def clock(text):
	hours = ''
	minutes = ''
	count = 0
	for x in text:
		if count == 0 and x != ' ':
			hours = hours + x
		elif count == 1 and x != ' ':
			minutes = minutes + x
		elif x == ' ':
			count += 1
		else:
			break
	for x in range(0,10):
		if hours == str(x):
			hours = '0' + hours
			break

	for x in opts["hours"]:
		if hours == x:
			for y in opts["minutes"]:
				if minutes == y:
					return [int(hours), int(minutes)]
	return [60,60]


def alarm(hours, minutes):
	now = datetime.datetime.now()
	if hours == int(now.hour) and minutes == int(now.minute):
		for x in range(25):
			alarm_play = simpleaudio.WaveObject.from_wave_file('/home/lena/Pomichnik/sound/Clock.wav').play()
			alarm_play.wait_done()
		return False
	else:
		return True
