import RPi.GPIO as GPIO
import time

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', ' ': ' '}

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Dot and dash input
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Word separator input
GPIO.setup(26, GPIO.OUT)  # Optional: for visual output

def main():
    message = ""
    not_pressed = time.time()
    try:
        while True:
            if GPIO.input(21) == GPIO.LOW:  # Button for Morse code pressed
                start_time = time.time()
                
                while GPIO.input(21) == GPIO.LOW:
                    time.sleep(0.01)  # debounce
                
                press_duration = time.time() - start_time

                if press_duration < 0.15:  # Short press for dot
                    message += '.'
                    print(message)
                    not_pressed = time.time()
                else: # Long press for dash
                    message += '-'
                    print(message)
                    not_pressed = time.time()
            not_pressedtime = time.time() - not_pressed
            
            if not_pressedtime > .75:
                if message and message[-1] != ' ':
                    message +
                
                
                
            if GPIO.input(20) == GPIO.LOW:  # Word separator button pressed
                decoded_word = ""
                decoded_word = decrypt(message)
                print(decoded_word)
                message = ""                  
                while GPIO.input(20) == GPIO.LOW:
                    time.sleep(0.1)  # debounce

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

def decrypt(message):
    message += ' '  # Add space to handle last Morse code
    decipher = ''
    citext = ''
    
    for letter in message:
        if letter != ' ':
            citext += letter
        else:
            if citext:  # Process the collected Morse code
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
            else:
                decipher += ' '  # Add space for word separation

    return decipher

if __name__ == '__main__':
    main()
