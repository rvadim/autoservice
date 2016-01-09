'use strict';

var app = angular.module('AutoService.Landing', [
    'ngTable',
    'AutoServiceAPI'
]);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/landing', {
        templateUrl: '/static/landing.html',
        controller: 'LandingController'
    });
}]);

app.controller('LandingController', ['$scope', 'Service', 'NgTableParams',
    function ($scope, Service, NgTableParams) {
        $scope.selectedServices = [];

         function isServiceSelected(service) {
            var out = _.find($scope.selectedServices, function (item) {
                return item.id === service.id;
            });
            if (out) { return true; } else {return false; }
         }

         function addServiceToSelected(item) {
            $scope.selectedServices.push(item);
         }

         function removeServiceFromSelected(item) {
            $scope.selectedServices.splice($scope.selectedServices.indexOf(item), 1);
         }

        Service.query().$promise.then(function(response) {
            $scope.serviceTable = new NgTableParams({count: 10}, {
                counts: [],
                dataset: response
            });
        });

        $scope.selectService = function (item) {
            if (isServiceSelected(item)) {
                removeServiceFromSelected(item);
                item.$selected = false;
            } else {
                addServiceToSelected(item);
                item.$selected = true;
            }
        };
    }
]);