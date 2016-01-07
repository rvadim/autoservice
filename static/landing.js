'use strict';

var app = angular.module('AutoService.Landing', []);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/landing', {
        templateUrl: '/static/landing.html',
        controller: 'LandingController'
    });
}]);

app.controller('LandingController', ['$scope',
    function ($scope) {
    }
]);