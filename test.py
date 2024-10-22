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
                    '(':'-.--.', ')':'-.--.-'}

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Dot and dash input
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Word separator input
GPIO.setup(26, GPIO.OUT)  # Optional: for visual output

def main():
    message = ""
    
    try:
        while True:
            if GPIO.input(21) == GPIO.LOW:  # Button for Morse code pressed
                start_time = time.time()
                
                while GPIO.input(21) == GPIO.LOW:
                    time.sleep(0.01)  # debounce
                
                press_duration = time.time() - start_time
                
                if press_duration < 0.5:  # Short press for dot
                    message += '.'
                    GPIO.output(26, GPIO.LOW)  # Optional: Turn on for dot
                else:  # Long press for dash
                    message += '-'
                    GPIO.output(26, GPIO.HIGH)  # Optional: Turn on for dash
                
                # Wait until button is released
                while GPIO.input(21) == GPIO.HIGH:
                    time.sleep(0.01)  # debounce
            
            if GPIO.input(20) == GPIO.LOW:  # Word separator button pressed
                if message:  # Only decrypt if there is a message
                    decoded_word = decrypt(message)
                    print(decoded_word)  # Print the decoded word
                    message = ""  # Reset the message for the next input
                
                # Wait until button is released
                while GPIO.input(20) == GPIO.HIGH:
                    time.sleep(0.01)  # debounce

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
                # Check if the Morse code exists in the dictionary
                if citext in MORSE_CODE_DICT.values():
                    decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                else:
                    decipher += '?'  # Indicate unknown Morse code
                citext = ''
            else:
                decipher += ' '  # Add space for word separation

    return decipher


if __name__ == '__main__':
    main()
