class CNC:
    """ Python class for CNC Machine
    """

    def __init__(self, port):
        """
        Args:
            port (string): the serial port of CNC, e.g, "COM3"
        """
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.is_open = self.ser.isOpen()
        if self.is_open:
            print('pydexarm: %s open' % self.ser.name)
        else:
            print('failed to open serial port')

    def _send_cmd(self, data, wait=True):
        """
        Send command to the arm.

        Args:
            data (string): the command
            wait (bool): wait for response from the arm (ok) or not.
                If True, this function will block until the arm response "ok"
                If False, this function will not block here. But the command could be ignored if buffer of the arm is full.
        """
        self.ser.write(data.encode())
        if not wait:
            self.ser.reset_input_buffer()
            return
        while True:
            try:
                serial_str = self.ser.readline().decode("utf-8")
                if len(serial_str) > 0:
                    if serial_str.find("ok") > -1:
                        print("read ok")
                        break
                    else:
                        print("read:", serial_str)
            except:
                print('no val')

# cnc = CNC(port="/dev/ttyACM0")

with open('CNC_G_Code/GeneralVerticalv1.txt') as f:
    lines = f.readlines()

commands = []

for item in lines:
    commands.append(item.strip())

# for cmd in commands:
#     cnc._send_cmd(cmd)
