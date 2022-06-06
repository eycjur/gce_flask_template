import os
from flask import Flask

print("Starting app...")
app = Flask(__name__)
print("App started!")

@app.route('/')
def index():
	return '<h1>Hello World!</h1>'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
