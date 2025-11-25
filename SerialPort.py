"""
Jatin Gandhi., 
Serial Port accesss abstraction with "Expect" implementation.
Expect() will send a command and "expect" a response to have required string., 
"""
from serial.tools import list_ports
import time
import serial


DEFAULT_COMPORT = "COM30"
# At a time we can "Write" max., 1024 bytes., 
MAX_BYTE_LIMIT  = 1024;

class SerialPort:
    def __init__(self, comPort : str = DEFAULT_COMPORT, timeout : int = 5, retries : int = 3, baudrate: int = 9600, sendInitMsg:bool = False, InitMsg: str = "Host Ready"):
        self.TIMEOUT_VALUE = timeout;
        self.NUM_TETRIES   = retries;
        self.baud_rate     = baudrate;
        self.serial_port   = None;
        self.IsConnected   = False;
        self.ComPort       = comPort;
        # NumWrites and NumReads are added for diagnostic purpose only.,
        self.NumWrites     = 0;
        self.NumReads      = 0;
        try:
            self.serial_port = serial.Serial(self.ComPort, timeout=self.TIMEOUT_VALUE,\
            baudrate = self.baud_rate,\
            xonxoff  = False,\
            rtscts   = False,\
            dsrdtr   = False,\
            parity   = serial.PARITY_NONE,\
            stopbits = serial.STOPBITS_ONE,\
            bytesize = serial.EIGHTBITS);

            # Flush as soon as we are able to connect it., 
            self.serial_port.flush();

            # Serial port is set.., 
            self.IsConnected = True;

            # If required, send ready string to check if controller is ready.., 
            if (True == sendInitMsg):
                self.serial_port.write(InitMsg.encode('utf-8'));

        except Exception as e:
            print(f"Could not connect to serial port => {self.ComPort}");
            print("Exception : ", e);

        
    def __del__(self):
        # Clean up., Resetting values.,
        if(None != self.serial_port and self.serial_port.isOpen()):
            self.serial_port.close();
        
        self.serial_port   = None;
        self.IsConnected   = False;
        self.NumWrites     = 0;
        self.NumReads      = 0;

        self.ComPort       = DEFAULT_COMPORT;

    def getList(self) -> list:
        l = list (list_ports.comports());
        com_list = [port.device for port in l]
        # Debug
        print("Detected COM Ports : ", end="");
        for p in com_list:
            print(f"{p},", end="");

        print("\n")
        return list(list_ports.comports());
    

        
    def Write(self, data:str = None, sendcrlf:bool = False, flushonwrite:bool = False):
        """
        IN: data: data string to be sent to serial port., It can be data or command.,
        IN: sendcrlf: Flag to decide if we need to send CR + LF characters (Enter) after command
        IN: flushonwrite: Flag to decide if we should flush the buffer after writing to serial., 
        OUT: Nothing
        """
        if (None == self.serial_port or False == self.IsConnected):
            return;
            
        if (None != data and len(data) > 0):
            self.serial_port.write(data.encode('utf-8')); # data written to 

            # Send carriage return and line feed if caller requested., 
            if (True == sendcrlf):
                self.serial_port.write("\r\n".encode("utf-8")); 

            if (True == flushonwrite):
                self.serial_port.flush();
        
            # Update Write() count for diag., 
            self.NumWrites += 1; 

            time.sleep(0.5);

        return;


    def Read(self) -> str:
        """
        This function returns the data read from serial port.
        """
        if(None == self.serial_port):
            print("Please select the COM port from the list")
            return;

        line = "";

        start_time = time.time();
        while True:
            if (time.time() - start_time) >= self.TIMEOUT_VALUE:
                #print(f"DEBUG: No data for {self.TIMEOUT_VALUE} seconds");
                line = "TIMEOUT";
                # No more data arrived within timeout, exit loop
                break;

            line = self.serial_port.readline()  # Reads until newline or timeout

            # Stop retrying if data is read from serial port.,
            if line:
                break;
            else:
                line = "";
                continue;

        line = line.rstrip();

        # Update Read() count for diag., 
        self.NumReads += 1;

        return str(line);


    def Flush(self):
        """
        This function flush the input buffer.,
        """
        if(None == self.serial_port):
            return;
        
        # Keep reading buffer until we get nothing., 
        # for given timeout set in constructor.,.,
        while True:
            line = self.serial_port.readline()  # Reads until newline or timeout
            if line:
                # Debug: print("Received:", line.decode().rstrip())
                pass;
            else:
                # No more data arrived within timeout, exit loop
                break


    def Expect(self, command="",response="") -> bool:
        """
        IN: command: Command to execute.,
        IN: response: Response expected for the command.,
        OUT: True if response is "in" response data, else returns False
        """
        if(len(command) <= 0 or len(response) <= 0):
            print(f"Expect: Invalid arguments command: {command} response:{response}")
            return;

        # Debug
        # print(f"Sending command: {[ord(x) for x in command]} and waiting for response: {response}");

        self.Write(data=command, sendcrlf=True, flushonwrite=True);

        retry_count = 1;

        status = False;

        while True:
            # Check for timeout., 
            if (retry_count > self.NUM_TETRIES):
                # print(f"DEBUG: No valid response came in {self.NUM_TETRIES} retries");
                break;

            val = self.Read();
            retry_count += 1;

            # if we got expected response.,
            # inform the caller that we e
            if (None != val and None != response and response in val):
                status = True;
                break;

        return status;


# Test code if SerialPort module is executed standalone., 
if __name__ == "__main__":
    ser = SerialPort("COM3",sendInitMsg=True,InitMsg="Hello World");

    if None == ser:
        print("Failed to open COM3 port\n");
        exit(1);

    print (f"List of Serial Ports {ser.getList()}");

    print(f"Writing text 'root' to serial port : {ser.ComPort}");
    ser.Write("root",True, True);

    print("Received from serial port: ");
    print(f"Data : {ser.Read()}");

    print(f"Sending command {hex(ord('\r'))}, {hex(ord('\n'))} and expecting \"login: \"");
    found = ser.Expect("\r\n", "login: ");
    if (True == found):
        print(f"Sent command {hex(ord('\r'))}, {hex(ord('\n'))} and got 'login: ' response");
    else:
        print(f"Sent command {hex(ord('\r'))}, {hex(ord('\n'))} and got no response");
