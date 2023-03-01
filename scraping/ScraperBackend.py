from flask import Flask, request, jsonify
from replit import db
import logging
import traceback
app = Flask(__name__)


@app.route('/')
def index():
  matches = db.prefix("product")
  res = []
  print(matches)
  for match in matches:
    r = db[match]
    res.append(r)
  print(res)
  return jsonify(dict(res))


@app.route('/price', methods=['POST'])
def index2():
  try:
    print(request.headers.get('Content-Type'))
  
    data = request.form
    print(data)
  
    url = data["url"]
    urlparts = url.split("/")
    productid = urlparts[-1]
  
    db["product" + productid] = data
  
    return "Accepted"
  except Exception as e:
    traceback.print_exception(e)
    return "Error"
    

app.run(host='0.0.0.0', port=81)
