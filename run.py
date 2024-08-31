# app.py
from flask import Flask, jsonify, request
from crawler import login_and_send_message, login_and_send_file
import webbrowser
import threading
import os

app = Flask(__name__, static_folder='./frontend/dist', static_url_path='')


@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')


@app.route('/api/crawler/message', methods=['POST'])
def web_crawler_message():
    try:
        url = request.json['url']
        message = request.json['message']
        login_and_send_message(url, message)
        return jsonify({'message': 'Message sent successfully',
                        'status': 'success'})
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'})


@app.route('/api/crawler/file', methods=['POST'])
def web_crawler_file():
    try:
        url = request.form['url']
        # get file binary data
        file = request.files['file']
        file_path = f'file/{file.filename}'
        # clear file directory
        if os.path.exists('file'):
            for file_name in os.listdir('file'):
                os.remove(f'file/{file_name}')
        else:
            os.makedirs('file')
        file.save(file_path)
        # switch to absolute path
        file_path = os.path.abspath(file_path)
        login_and_send_file(url, file_path)
        return jsonify({'message': 'File sent successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'})


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=False)
