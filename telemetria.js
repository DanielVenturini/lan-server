var app = angular.module('Venturini/1.1', []);

app.controller('myCtrl', function($scope, $http, $timeout) {
    $http.get("virtual/telemetria/status.json")
   .then(function(response){

        $scope.requests = response.data['requests'];
        $scope.uptime = response.data['uptime'];
        $scope.connecteds = response.data['connecteds'];
        $scope.currenttime = response.data['currenttime'];
   });
});