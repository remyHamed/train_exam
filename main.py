# -*- coding: utf-8 -*-
"""
Created on Mon Apr 2024

@author: Remy Hamed
Traitements sur fichiers (1h30)
	- accès au cours, à l'ordinateur et à internet
	- les objets Queue de python sont interdits


Mon application va me permettre de simuler un système asynchrone complexe:
	- 2 clients "C1" et "C2" (modélise des clients exterieurs) qui envoient des messages
	- ce que je souhaite tester "T": mon traitement des messages


Chaque client aura un fichiers tests client_i.txt qui contient des commandes du type:
	WAIT n
		'n' est un entier en secondes
		==> le client dort pendant n secondes

	SEND "message"
		le message est forcément entre quotes
		==> envoie un message au système de traitement "T" contenant un timestamp, l'id du client et le texte


Le système de traitement "T" récupère les messages et les logguent dans un fichier CSV avec le format suivant:
	timestamp de traitement; timestamp d'envoi, id client;text



Vous me fournirez les documents suivants dans un zip:
	- un fichier python contenant votre code source aéré et documenté
	- le fichier de log que vous avez obtenu
"""
from asyncio import threads
from time import sleep
from threading import Thread, Lock
import time

class Queue:
    def __init__(self):
        self.__queue = []
        self.__lock = Lock()

    def push( self, data ):
        with self.__lock:
            self.__queue.append( data )

    def pop( self ):
        with self.__lock:
            if len(self.__queue) == 0:
                return None
            return self.__queue.pop( 0 )

    def __len__(self):
        with self.__lock:
            return len(self.__queue)

class T:
    def __init__(self, filename):
        self.filename = filename

    def send_message(self, client_id, message):
        timestamp_send = int(time.time())
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([int(time.time()), timestamp_send, client_id, message])


def read_messages_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        messages = []
        for line in lines:
            if line.strip():
                parts = line.strip().split(' ')
                message = " ".join(parts[1:])
                wait_time_str = parts[-1].replace('"', '')
                if parts[0] == 'WAIT':
                    time.sleep(int(wait_time_str))
                messages.append((message, wait_time_str))
        return messages

def client(id: int, queue: Queue, file_path: str):
    messages = read_messages_from_file(file_path)
    for message, wait_time in messages:
        time.sleep(wait_time)
        queue.push(f"Message {id:03d}: {message}")

if __name__ == "__main__":
    q = Queue()

    threads = [
        Thread(target=client, args=(1, q, 'client_1.txt')),
        Thread(target=client, args=(2, q, 'client_2.txt')),
    ]
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]


[ t.start() for t in threads ]
[ t.join() for t in threads ]
print("finished....")
print( len(q) )