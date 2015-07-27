module.exports = function(app) {

	// server routes ===========================================================
	// handle things like api calls
	// authentication routes

	// frontend routes =========================================================
	// route to handle all angular requests
	app.get('*', function(req, res) {
		res.sendfile('./public/index.html');
	});

	app.post('Http://localhost:5000/learning/api/v1.0/analyzeTweets', 
		function(req, res, next) {
			
	});

};