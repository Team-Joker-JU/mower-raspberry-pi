from controller import Controller
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='usb_port', help="This should be the USB port")
    parser.add_argument(dest='baud_rate', help="This should be the baudrate")
    args = parser.parse_args()
    usb_port = args.usb_port
    baud_rate = args.baud_rate

    c = Controller(usb_port, baud_rate)
    c.start()
    
if __name__ == '__main__':
    main()
