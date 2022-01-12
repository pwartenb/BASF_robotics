import re

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

    def move_to(self, x=None, y=None, z=None, e=None, feedrate=2000, mode="G1", wait=True):
        """
        Move to a cartesian position. This will add a linear move to the queue to be performed after all previous moves are completed.

        Args:
            mode (string, G0 or G1): G1 by default. use G0 for fast mode
            x, y, z (int): The position, in millimeters by default. Units may be set to inches by G20. Note that the center of y axis is 300mm.
            feedrate (int): set the feedrate for all subsequent moves
        """
        cmd = mode + "F" + str(feedrate)
        if x is not None:
            cmd = cmd + "X"+str(round(x))
        if y is not None:
            cmd = cmd + "Y" + str(round(y))
        if z is not None:
            cmd = cmd + "Z" + str(round(z))
        if e is not None:
            cmd = cmd + "E" + str(round(e))
        cmd = cmd + "\r\n"
        self._send_cmd(cmd, wait=wait)

    def get_current_position(self):
        """
        Get the current position
        
        Returns:
            position x,y,z, extrusion e
        """
        self.ser.reset_input_buffer()
        self.ser.write('M114\r'.encode())
        x, y, z, e = None, None, None, None
        while True:
            serial_str = self.ser.readline().decode("utf-8")
            print(serial_str)
            if len(serial_str) > 0:
                if serial_str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", serial_str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    e = float(temp[3])
                    return x, y, z, e
            if len(serial_str) > 0:
                    if serial_str.find("ok") > -1:
                        return x, y, z

cnc = CNC(port="/dev/ttyACM0")

if __name__ == "__main__":
    with open('CNC_G_Code/test.txt') as f:
        lines = f.readlines()

    commands = []

    for item in lines:
        commands.append(item.strip())

    for cmd in commands:
        cnc._send_cmd(cmd)

    while True:
        pos = cnc.get_current_position()
        print(pos)
        x_pos = int(pos[0])
        y_pos = int(pos[1])
        z_pos = int(pos[2])
        delta_z = float(input("Change Z by how much?"))
        if delta_z == 0:
            cnc._send_cmd("M30")
            cnc._send_cmd("%")
            break
        cnc.move_to(x_pos, y_pos, z_pos + delta_z)

