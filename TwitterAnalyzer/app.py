from flask import Flask, jsonify, request, abort
from AnalyzingHandler import AnalyzingHandler

app = Flask(__name__)
handler = handler = AnalyzingHandler()

@app.route('/learning/api/v1.0/analyzeTweets', methods=['POST'])
def analyzeTweets():
	print "Entered function"

	if not request.json or not 'keyword' in request.json:
		abort(400)

	#print "Passed if"

	keyword = request.json['keyword']
	location = request.json['location']

	print "passed extraction"

	return jsonify(handler.analyzeTweets(keyword, location=location)), 201
#end

#def index():
#    return "Hello, World!"

#def setup_app(app):


if __name__ == '__main__':
    app.run(debug=True)