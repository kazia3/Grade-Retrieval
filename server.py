import csv
import socket
import argparse 
import sys
from cryptography.fernet import Fernet
# from signal import signal, SIGPIPE, SIG_DFL  

# signal(SIGPIPE,SIG_DFL)

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

        print('Data read from csv file:')
        print(self.grades)
        print()

    def listen(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(Server.address)
            self.socket.listen(Server.backlog)

            print('Listening for connections on port ', Server.port)
            print()

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
                command = recvbytes.decode(Server.encoding)

                if len(recvbytes) == 0:
                    print("Closing connection.")
                    connection.close()
                    break
                
                ##############enter how server work here#############
                stud = command[:7]
                func = int(command[-1])
                userfound = 0

                for i in self.grades:
                    if i[1] == stud:
                        print()
                        print('User found.')
                        userfound = 1

                        encryption_key = i[2]
                        
                        if func == 0:
                            print('Received GG command from client.')
                            data = [i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]]
                            send_msg = ','.join(str(e) for e in data)
                            
                        elif func == 1:
                            print('Received GL1A command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][3])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                        elif func == 2:
                            print('Received GL2A command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][4])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                        elif func == 3:
                            print('Received GL3A command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][5])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                        elif func == 4:
                            print('Received GL4A command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][6])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                        elif func == 5:
                            print('Received GMA command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][7])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                        elif func == 6:
                            print('Received GEA command from client.')
                            sum = 0
                            for e in range(1,len(self.grades)):
                                sum += int(self.grades[e][8]) + int(self.grades[e][9]) + int(self.grades[e][10]) + int(self.grades[e][11])
                            average = sum/len(self.grades)
                            send_msg = str(average)

                if userfound == 1:
                    encryption_key_bytes = encryption_key.encode('utf-8')

                    # Encrypt the message for transmission at the server.
                    fernet = Fernet(encryption_key_bytes)
                    encrypted_message_bytes = fernet.encrypt(send_msg.encode(self.encoding))
                    print()
                    print("encrypted_message_bytes = ", encrypted_message_bytes)
                    print()

                    print(send_msg, type(send_msg))

                    connection.sendall(send_msg.encode(self.encoding)) 
                
                else:
                    print()
                    print('User not found.')
                    print("Closing connection.")
                    connection.close()

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
            self.socket.connect((Client.SERVER_HOSTNAME, Server.port))
            print("Connected to \"{}\" on port {}".format(Client.SERVER_HOSTNAME, Server.port))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered, i.e., ignore blank lines.
        while True:
            self.input_text = input("Input your student number followed by a command (e.g. 400130086GLA): ")
            if self.input_text != "":
                print("Command entered: ", self.input_text)
                break

    def command_process(self):
        if self.input_text[7:] == "GG":
            self.input_text = self.input_text.replace('GG', '0')
            print('Getting grades: ')
        elif self.input_text[7:] == "GMA":
            self.input_text = self.input_text.replace('GMA', '5')
            print('Getting midterm average: ')
        elif self.input_text[7:] == "GL1A":
            self.input_text = self.input_text.replace('GL1A', '1')
            print('Getting lab 1 average: ')
        elif self.input_text[7:] == "GL2A":
            self.input_text = self.input_text.replace('GL2A', '2')
            print('Getting lab 2 average: ')
        elif self.input_text[7:] == "GL3A":
            self.input_text = self.input_text.replace('GL3A', '3')
            print('Getting lab 3 average: ')
        elif self.input_text[7:] == "GL4A":
            self.input_text = self.input_text.replace('GL4A', '4')
            print('Getting lab 4 average: ')
        elif self.input_text[7:] == "GEA":
            self.input_text = self.input_text.replace('GEA', '6')
            print('Getting exam average: ')
        else:
            print('Invalid command.')
            self.get_console_input()
    
    def send_console_input_forever(self):
        while True:
            try:
                self.get_console_input()
                self.command_process()
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
            self.socket.sendall(self.input_text.encode(Server.encoding))
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

            print("Received: ", recvd_bytes.decode(Server.encoding))

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