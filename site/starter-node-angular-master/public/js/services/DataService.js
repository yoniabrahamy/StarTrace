angular.module('DataService', []).factory('Data', ['$http','$q', function($http, $q) {
  
  var data = undefined;
  
  return {

  query: function(jsonObj) {
       return $http.post("http://localhost:5000/learning/api/v1.0/analyzeTweets", jsonObj);
  }
}

}]);