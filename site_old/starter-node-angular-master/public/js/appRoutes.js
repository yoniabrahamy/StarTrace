angular.module('appRoutes', []).config(['$stateProvider', '$urlRouterProvider', 
	function($stateProvider, $urlRouterProvider) {
	
	// For any unmatched url, send to /home
  	$urlRouterProvider.otherwise("/home");
      
  	$stateProvider
	    .state('home', {
	        url: "/home",
			templateUrl: 'views/home.html',
			controller: 'MainController'
	    });
}]);