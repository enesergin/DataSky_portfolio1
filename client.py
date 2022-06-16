import argparse
import socket
import threading
import time
import random

bot_clients = ['alice', 'bob', 'dora', 'chuck']

# parser that checks if the user has written the needed arguments,
# which in this case is the port number and name of the client
parser = argparse.ArgumentParser(
    description='You can connect to a chat room. If you would like a bot client to join the chat,'
                ' write one of the bot names (Alice, Bob, Dora or Chuck)\nExample of how: client.py 1234 Enes')
parser.add_argument('port', type=int, help='Argument 1: Port number you wanna connect to. Write it in numbers only!')
parser.add_argument('name', type=str, help='Argument 2: The client name you would like to connect with.'
                                           ' Write a bot name if you would like to connect a bot')
args = parser.parse_args()
port = args.port
name = args.name

# creating a client socket and then connecting to the user given port
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect(('localhost', port))

# list of positive and negative actions
positiveAction = ['eat', 'walk', 'laugh', 'kiss', 'paint', 'cook']
negativeAction = ['cry', 'fight', 'bully', 'shout', 'steal', 'murder']


# BOT 1 - alice: wants to do the positive actions, and not the negative actions
def alice(action):
    if action in positiveAction:
        positiveAnswers = [
            '{}: I´d like {}.'
            .format(name, action + 'ing'),
            '{}: I think {} sounds great!'
            .format(name, action + 'ing'),
            '{}: {}! I absolutely love {}!'
            .format(name, action + 'ing', action + 'ing')]
        output = random.choice(positiveAnswers)

    elif action in negativeAction:
        negativeAnswers = [
            '{}: I wanna avoid {}'
            .format(name, action + 'ing'),
            '{}: {}? Don´t you have anything else to do?'
            .format(name, action + 'ing'),
            '{}: I think we should do something else other than {}'
            .format(name, action + 'ing')]
        output = random.choice(negativeAnswers)

    else:
        noActionAnswers = [
            '{}: What are you saying? Come on man...'.format(name),
            '{}: Nope, not happening.'.format(name),
            '{}: I´m not interested.'.format(name)]
        output = random.choice(noActionAnswers)
    return output + '\n'


# BOT 2 - bob: says no to every action and sometimes suggest something else (bob is confused)
def bob(action):
    if action in negativeAction or action in positiveAction:
        answers = [
            '{}: I´m not really interested in {}. Can we do some {} instead?'
            .format(name, action + 'ing', random.choice(negativeAction) + 'ing'),
            '{}: You want to {}? Doesnt {} sound better instead?'
            .format(name, action, random.choice(positiveAction) + 'ing'),
            '{}: No way I´m {}, Let´s just do something else...'
            .format(name, action + 'ing')]
        output = random.choice(answers)

    else:
        noActionAnswers = [
            '{}: What? Definitely no.'.format(name),
            '{}: Yeah, not doing that.'.format(name),
            '{}: Aren´t you supposed to say something useful?'.format(name)]
        output = random.choice(noActionAnswers)
    return output + '\n'


# BOT 3 - dora: thinks the positive actions are boring, and wants to do the negative actions (dora is evil)
def dora(action):
    if action in positiveAction:
        positiveAnswers = [
            '{}: {} is boring. I´m not interested in that.'
            .format(name, action + 'ing'),
            '{}: I don´t wanna {}. Not really for me.'
            .format(name, action),
            '{}: Really? {}? You can come up with something more exciting than {}...'
            .format(name, action + 'ing', action + 'ing')]
        output = random.choice(positiveAnswers)

    elif action in negativeAction:
        negativeAnswers = [
            '{}: You wanna {}? I´m okay with that but maybe we should keep it private.'
            .format(name, action),
            '{}: {}? If you aren´t going to tell anyone I´m down. Sounds great to me...'
            .format(name, action + 'ing'),
            '{}: Yes definitely, let´s go {}!'
            .format(name, action + 'ing')]
        output = random.choice(negativeAnswers)

    else:
        noActionAnswers = [
            '{}: Come on man, suggest something to do!'.format(name),
            '{}: I don´t even know what I´m doing here.'.format(name)]
        output = random.choice(noActionAnswers)
    return output + '\n'


# BOT 4 - chuck: wants to do the positive actions, and not the negative actions
def chuck(action):
    if action in positiveAction:
        positiveAnswers = [
            '{}: {}, sounds great to be honest!.'
            .format(name, action + 'ing'),
            '{}: Such a good idea! Let´s go {}'
            .format(name, action + 'ing'),
            '{}: YES! I want to {} too!'
            .format(name, action)]
        output = random.choice(positiveAnswers)

    elif action in negativeAction:
        negativeAnswers = [
            '{}: No chance I´m {}.'
            .format(name, action + 'ing'),
            '{}: What? {} sucks. I´m definitely not doing that!'
            .format(name, action + 'ing'),
            '{}: I think we should do something else other than {}'
            .format(name, action + 'ing')]
        output = random.choice(negativeAnswers)

    else:
        noActionAnswers = [
            '{}: I´m not doing that.'.format(name),
            '{}: That´s just boring. Suggest something else...'.format(name),
            '{}: I´m not too sure to be honest.'.format(name)]
        output = random.choice(noActionAnswers)
    return output + '\n'


# this is the host sending messages, gets broadcasted to all the connected clients
def host_sending_message():
    while True:
        msg = f'{name}: {input()}'  # formats the message
        split = msg.split(": ")
        if split[1] == "":
            print('Can´t be empty!')
            continue
        else:
            time.sleep(0.5)
            print('')
            print_send(msg)


def print_send(msg):
    print(msg)
    socketClient.send(msg.encode('utf-8'))


# this is used for handling of clients i.e. connecting not connected clients to the server,
# and also making sure that clients receive messages from other clients
def client_handling():
    while True:
        msg = socketClient.recv(1024).decode('utf-8')

        if msg.lower() == 'not_connected':  # 'not_connected' is sent from server if the client is not connected,
            # goes into this if-statement if the client isn't connected
            socketClient.send(name.encode('utf-8'))  # sends the clients name back to the server

        else:
            if ":" in msg:  # goes in here if its a sent message,
                # and not a notification telling if a client has connected/disconnected
                split = msg.split(": ")

                if split[0].lower() not in bot_clients:  # receiving messages from host,
                    # will trigger bot functions later in this if-statement

                    message = ""
                    allActions = positiveAction + negativeAction
                    for i in allActions:  # loop that checks if the host-client message includes any of the actions
                        if i in msg.lower():  # an action has been found in the host-client message
                            message = i
                            break

                    output = ''
                    for i in bot_clients:  # loop that goes through the bot names,
                        # and runs their assigned function using builtin function eval
                        if i == name.lower():
                            output = eval(i + '(message)')
                            break

                    print(msg)  # message that is received from the host
                    print_send(output)  # message that is printed to the current client window, and to the other clients

                else:  # receiving messages from bots, won't trigger bot function
                    time.sleep(1)
                    print(msg)

            else:  # notifies that a client has connected/disconnected the chat to the other clients
                print(msg)


handling_thread = threading.Thread(target=client_handling)
handling_thread.start()

if name not in bot_clients:
    sending_thread = threading.Thread(target=host_sending_message)
    sending_thread.start()
