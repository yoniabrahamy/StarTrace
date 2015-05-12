angular.module('MainCtrl', []).controller('MainController', function($scope, Data) {

	$scope.celebrity;
	$scope.city;
	$scope.getDataStatus = "beforeGetData";
	$scope.dataObject = {}

	$scope.getDataFromServer = function () {
		//use dataService to get the json 
		$scope.getDataStatus = "getDataProccess";

		var reqObject = {
			"keyword": $scope.celebrity,
			"location":$scope.city
		}

		/*return (Data.query(JSON.stringify(reqObject);)
 			.then (function (value) {
 				$scope.dataObject = value;
 			},
 			function (error) {
 				console.log("error while getting data: " + error.textMessage);
 				$scope.dataObject = {];
 			}));
		}*/

		$scope.dataObject = {
			"positive":33,
			"negative":33,
			"neutral":33
		}

		$scope.getDataStatus = "getDataSuccess"
	}
});