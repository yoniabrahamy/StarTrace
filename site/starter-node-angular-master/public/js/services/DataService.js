angular.module('DataService', []).factory('Data', ['$http','$q', function($http, $q) {
  
  var data = undefined;
  /*
  get = function(id) {
    return $http.get('/api/vinyls/' + id).then(function(res){
      return res.data;
    });
  };
  
  return {
    getAll: function() { // promise for some data
        return $http.get('/api/vinyls')
          .then(function(value) { 
            data = value.data; 
            return data; 
          });
   },
   getById: function(id) {
    return $http.get('/api/vinyls/' + id)
      .then(function(value) {
        data = value.data;
        return data;
      });
  },
  query: function(queryString) {
      return $http.get('/api/vinyls' + queryString);
  },
  save: function(vinyl) {
       return $http.post("/api/vinyls", vinyl);
  },
  delete: function(id) {
       return $http.delete('/api/vinyls/' + id);
  },
  update: function(vinyl) {
       return $http.put('/api/vinyls/' + vinyl._id, vinyl);
  }
}
*/
}]);