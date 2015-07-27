angular.module('MainCtrl', []).controller('MainController', function($scope, Data) {

	$scope.celebrity;
	$scope.city;
	$scope.getDataStatus = "beforeGetData";
	$scope.isError = false;
	$scope.dataObject = {}

	$scope.getDataFromServer = function () {

		$scope.isError = false;
		
		//use dataService to get the json 
		$scope.getDataStatus = "getDataProccess";
		$scope.dataObject = {}
		//$scope.isError = true;

		var reqObject = {
			"keyword": $scope.celebrity,
			"location":$scope.city
		}

		return (Data.query(JSON.stringify(reqObject))
 			.then (function (value) {
 				$scope.dataObject = value.data;
 				$scope.currCelebrity = JSON.parse(JSON.stringify($scope.celebrity));
 				$scope.currCity = JSON.parse(JSON.stringify($scope.city));

 				if ((($scope.dataObject.positive == 0) &&
 					($scope.dataObject.negative == 0) &&
 					($scope.dataObject.neutral == 0)) ||
 					(!($scope.dataObject))) {
 					
 					$scope.isError = true;			
 				}
 				else {
 					$scope.isError = false;
 					$scope.getDataStatus = "getDataSuccess";

 					// Pie chart 
					nv.addGraph(function() {
					  var chart = nv.models.pieChart()
					      .x(function(d) { return d.label })
					      .y(function(d) { return d.value })
					      .color(GetColors())
					      .labelThreshold(.05) 
					      .showLabels(true)
					      .pieLabelsOutside(false)
					      .labelType("percent") 
					      .donut(true)          
					      .donutRatio(0.35);

					    d3.select("#chart svg")
					        .datum(InitData(value.data))
					        .transition().duration(1200)
					        .call(chart);
					  return chart;
					});
					 				}
 			},
 			function (error) {
 				console.log("error while getting data: " + error.textMessage);
 				$scope.dataObject = {};
 				$scope.isError = true;
 				$scope.getDataStatus = "getDataError"
 			}));
		};

		// define pie chart colors
		function GetColors(dataObject) {
			var colors = [
			    'rgb(22, 158, 36)', // positive
			    'rgb(190, 13, 13)', // negative
			    'rgb(48, 141, 193)' // neutral
			];

			return colors;
		}

		// define pie chart data
		function InitData(dataObject) {
			return [{"label" : "positive", "value" : dataObject.positive},
					{"label" : "negative", "value" : dataObject.negative},
					{"label" : "neutral", "value" : dataObject.neutral}];
		}
/*
		$scope.dataObject = {
			"positive":33,
			"negative":33,
			"neutral":33
		}*/
});