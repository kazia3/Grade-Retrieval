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

    def __init__(self):
        self.readcsv()
        print(self.rawdata)
        self.listen()
        self.process()

    def readcsv(self):

        file = open('./course_grades_2023.csv')

        self.rawdata = [clean_line for clean_line in
                [line.strip() for line in file.readlines()]
                if clean_line != '']

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
    

