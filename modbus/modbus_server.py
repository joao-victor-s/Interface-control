from pyModbusTCP.server import ModbusServer
import logging
import time

logging.basicConfig()
logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)

if __name__ == '__main__':
    server = ModbusServer(host='0.0.0.0', port=5020, no_block=True)
    server.start()  
    print("Modbus Server is running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:    
        print("\nShutting Down...")
        server.stop()
