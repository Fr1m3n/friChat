from flask import Flask, render_template, request, session, redirect
from time import sleep
from json import dumps, loads

app = Flask(__name__)
app.secret_key = 'ashdl12k34ljllkan'

message_queue = {}

def sendMessage(sender, text):
    for user in message_queue.values():
        user.append({
            'text': text,
            'sender': sender
        })


@app.route('/', methods=['GET', 'POST'])
def pageLoader():
    print('session: ' + str(session))
    print('form: ' + str(request.form))
    if request.method == 'GET':
        if 'username' in session:
            username = session['username']
            return render_template('main.html', username=username)
        else:
            return render_template('login.html')
    else:
        if request.form['type'] == 'login':
            session['username'] = request.form['username']
            # return render_template('main.html')
        else:
            session.pop('username', None)
            # return render_template('login.html')
        return redirect('/')


@app.route('/api/message', methods=['GET', 'POST'])
def apiMessageHandler():
    if 'username' not in session or session['username'] not in message_queue:
        return '404'
    if request.method == 'GET':
        while len(message_queue[session['username']]) == 0:
            sleep(1)
        if session['username'] in message_queue:
            username = session['username']
            ans = dumps({
                'messages': message_queue[username],
                'info': {
                    'online_users': len(message_queue),
                    'users': [user for user in message_queue.keys()]
                }
            })
            message_queue[username] = []
            return ans
    else:
        # for user in message_queue.values():
        #     user.append({
        #         'text': request.form['text'],
        #         'sender': session['username']
        #     })
        sendMessage(session['username'], request.form['text'])
        print(message_queue)
        return '200'


@app.route('/api/connect', methods=['GET'])
def apiConnect():
    if 'username' not in session:
        return '404'
    username = session['username']
    message_queue[username] = []
    print(message_queue)
    sendMessage('SERVER', str(username) + ' присоединился к чату')
    return '200'


@app.route('/api/disconnect', methods=['GET'])
def apiDisconnect():
    if 'username' not in session:
        return '404'
    username = session['username']
    print(message_queue)
    message_queue.pop(username)
    sendMessage('SERVER', str(username) + ' покинул нас')

    return '200'


if __name__ == '__main__':
    app.run(threading=True)
