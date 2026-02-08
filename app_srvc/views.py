from datetime import datetime,timedelta
import flask 
from flask import Flask, render_template, request, jsonify, make_response, Response, render_template_string
import cv2
import json
import logging
import datetime
import sys
import traceback
import os
import time
import cv2


from app_srvc.Errors import AppError, AppValidationError, InvalidAPIUsage


application = Flask(__name__)
app_title="Сервіс Flask "

camera = cv2.VideoCapture(0) # Ваша вбудована камера

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Оптимізуємо розмір для віртуалки
            frame = cv2.resize(frame, (640, 480))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@application.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    """
        Rest Api Error  handler
    """
    r=e.to_dict()
    return json.dumps(r), e.status_code, {'Content-Type':'application/json'}

"""
    Simple logger
"""
logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
def log( a_msg='NoMessage', a_label='logger' ):
	dttm = datetime.datetime.now()
	ls_dttm = dttm.strftime('%d-%m-%y %I:%M:%S %p')
	logging.info(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)
	print(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)

def add_cors_headers(response):
    """
        CORSA headers
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Content-Type"] = "applicaion/json"
    response.headers["Accept"] = "applicaion/json"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "DELETE,GET,POST"
    return response

@application.route("/")
def home():
    """
        Render main page
    """
    log("render home.html" )
    return render_template("home.html")

@application.route("/about/")
def about():
    """
        Render about pager
    """
    return render_template("about.html")


"""
   ===========================================================================
    *********** Rest API ******************************
    ===========================================================================
"""

@application.route("/api/health", methods=["GET"])
def health():
    """
        health check
    """
    label="health"
    log('Health check', label)
    result={ "ok": True,"app_title":app_title}
    log('Health check return result '+ json.dumps( result ), label)
    return json.dumps( result ), 200, {'Content-Type':'application/json'}

@application.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Простий HTML-шаблон прямо в коді
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Камера Ноутбука - Моніторинг</title>
    </head>
    <body>
        <h1>Стрім камери для Docker-контейнера</h1>
        <img src="{{ url_for('video_feed') }}" width="640" height="480" style="border: 2px solid black;">
        <p>URL для налаштування контейнера: <b>http://{{ host_ip }}:8080/video</b></p>
    </body>
</html>
"""

@application.route('/videotest')
def video_test():
    # Ви можете вказати свій IP вручну або залишити порожнім
    return render_template_string(HTML_TEMPLATE, host_ip="ВАШ_IP_ХОСТА")