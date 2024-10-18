import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(26, GPIO.OUT)

try:
	while True:
		if GPIO.input(21) == GPIO.LOW:
			GPIO.output(26, GPIO.LOW)

		else:
			GPIO.output(26, GPIO.HIGH)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

