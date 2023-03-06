import csv
import socket
import argparse 
import sys

class Server:
    hostname = "0.0.0.0"
    port = 50000
    address = (hostname, port)
    recvsize = 1024
    encoding = 'utf-8'
    backlog = 10
    grades = []

    def __init__(self):
        self.readcsv()
        print(self.rawdata)
        self.listen()
        self.process()

    def readcsv(self):

        file = open('./course_grades_2023.csv')
        reader = csv.reader(file)

        for i in reader:
            self.grades.append(i)

        # self.rawdata = [clean_line for clean_line in
        #         [line.strip() for line in file.readlines()]
        #         if clean_line != '']

        file.close()

        # try:
        #     self.parseddata = [
        #         (int(e[0].strip()), e[1].strip(), e[2].strip()) for e in
        #         [e.split(',') for e in self.rawdata]]
        # except Exception:
        #     print("Error: Invalid people name input file.")
        #     exit()

        

    def listen(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(Server.address)
            self.socket.listen(Server.backlog)

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())
        
        except Exception as msg:
            print(msg)

        except KeyboardInterrupt:
            print()
        
        finally:
            self.socket.close()
            sys.exit(1)
        
    def connection_handler(self,client):
        connection, address_port = client
        print('Connection received from {}.'.format(address_port))

        while True:
            try:
                recvbytes = connection.recv(Server.recvsize)

                if len(recvbytes) == 0:
                    print("Closing connection.")
                    connection.close()
                    break
                
                ##############enter how server work here#############

            except KeyboardInterrupt:
                print()
                print("Closing connection.")
                connection.close()
                break
    

########################################################################
# Echo Client class
########################################################################

class Client:

    SERVER_HOSTNAME = socket.gethostname()


    # RECV_BUFFER_SIZE = 5 # Used for recv.    
    RECV_BUFFER_SIZE = 1024 # Used for recv.

    def __init__(self):
        self.get_socket()
        self.connect_to_server()
        self.send_console_input_forever()

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow us to bind to the same port right away.            
            # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the client socket to a particular address/port.
            # self.socket.bind((Client.HOSTNAME, 40000))
                
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
            print("Connected to \"{}\" on port {}".format(Client.SERVER_HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered, i.e., ignore blank lines.
        while True:
            self.input_text = input("Input: ")
            if self.input_text != "":
                break
    
    def send_console_input_forever(self):
        while True:
            try:
                self.get_console_input()
                self.connection_send()
                self.connection_receive()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Closing server connection ...")
                # If we get and error or keyboard interrupt, make sure
                # that we close the socket.
                self.socket.close()
                sys.exit(1)
                
    def connection_send(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(self.input_text.encode(Server.MSG_ENCODING))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection ... ")
                self.socket.close()
                sys.exit(1)

            print("Received: ", recvd_bytes.decode(Server.MSG_ENCODING))

        except Exception as msg:
            print(msg)
            sys.exit(1)

########################################################################
# Process command line arguments if this module is run directly.
########################################################################

# When the python interpreter runs this module directly (rather than
# importing it into another file) it sets the __name__ variable to a
# value of "__main__". If this file is imported from another module,
# then __name__ will be set to that module's name.

if __name__ == '__main__':
    roles = {'client': Client,'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles, 
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()

########################################################################