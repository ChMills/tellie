### sends a continuous pulse
from core import serial_command
import sys

def safe_exit(sc,e):
    print "Exit safely"
    print e
    sc.stop()

if __name__=="__main__":
    width = sys.argv[1]
    channel = sys.argv[2]
    number = sys.argv[3]
    width = int(width)
    channel = int(channel)
    number = int(number)
    print "Opening serial link..."
    sc = serial_command.SerialCommand("/dev/tty.usbserial-FTGA2OCZ")
    print "Done!"
    sc.stop()
    sc.select_channel(channel)
    sc.set_pulse_height(16383)
    sc.set_pulse_width(width)
    sc.set_pulse_number(number)
    for i in range(10):
        try:
            print sc.trigger_single()
            #while True:
            #    pass
        except Exception,e:
            safe_exit(sc,e)
        except KeyboardInterrupt:
            safe_exit(sc,"keyboard interrupt")
        
        
