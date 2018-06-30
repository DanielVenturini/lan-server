var app = angular.module('Venturini/1.1', []);

// function to request the status.json

app.controller('myCtrl', function($scope, $http, $interval){
    var funRequest = function() {
        $http.get("virtual/telemetria/status.json")
       .then(function(response){

            $scope.requests = response.data['requests'];
            $scope.uptime = response.data['uptime'];
            $scope.connecteds = response.data['connecteds'];
            $scope.currenttime = response.data['currenttime'];
       });
    }

    funRequest()
    $interval(funRequest, 1000);
});