#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from pprint import pprint


data = {
    "todo": [
        {"name": "Task saving", "detail": "posibility to saving tasks automaticaly"},
        {"name": "Due date field", "detail": "Add the due date field. This field turn to red if date is close to today"}
    ],
    "wip": [
        {"name": "Task detail description", "detail": "Sometime you need more than short note, because some tasks are more complicated and requires a bit more description", "due_date": "2020-12-24"}
    ],
    "check": [],
    "done": [
        {
          "name": "Drag&Drop",
          "detail": "Spousta poznamek jak by to asi mohlo vypadat, mozna nejaky obrazek a video. Odhaduju, ze to zabere alespon tyden casu.",
          "due_date": "2020-11-02"
        }
    ]
}



app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/v1/tasks", methods = ["GET", "POST", "UPDATE", "PATCH"])
def tasks():
    if request.method == "POST":
        print("get data")
        new_data = request.get_json()
        pprint(new_data)
        data["todo"].append(new_data)

    if request.method in ["UPDATE", "PATCH"]:
        print("update data")
        new_data = request.get_json()
        pprint(new_data)
        data.update(new_data)
    
    r = make_response(jsonify(data), 200)
    r.headers.add("Access-Control-Allow-Origin", "*")
    r.headers.add('Access-Control-Allow-Headers', "*")
    r.headers.add('Access-Control-Allow-Methods', "*")
    r.content_type = "application/json"

    return r


if __name__ == "__main__":
    app.run()
