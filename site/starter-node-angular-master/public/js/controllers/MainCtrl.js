angular.module('MainCtrl', []).controller('MainController', function($scope) {

	alert("ddd");
	$scope.tagline = 'To the moon and back!';

	$scope.celebrity;
	$scope.city;

	$scope.getDataFromServer = function () {
		//use dataService to get the json 
	}
});