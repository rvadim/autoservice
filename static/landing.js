'use strict';

var app = angular.module('AutoService.Landing', [
    'smart-table',
    'AutoServiceAPI'
]);

app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/landing', {
        templateUrl: '/static/landing.html',
        controller: 'LandingController'
    });
}]);

app.controller('LandingController', ['$scope', 'Service',
    function ($scope, Service) {
        $scope.selectedServices = 'Услуги пока не выбраны...';
        $scope.serviceTable = [];
        Service.query().$promise.then(function(response) {
            $scope.serviceTable = response;
            //tableState.pagination.numberOfPages = response.length; //set the number of pages so the pagination can update
        });

        $scope.selectService = function (item) {
            item.$selected = !item.$selected;
        };

        $scope.updateSelected = function () {
            $scope.selectedServices = 'Выбраны услуги: ';
            var output = [];
            _.each($scope.servicesTable.data, function (service) {
                if (service.$selected) {
                    output.push(service.name);
                }
            });
            $scope.selectedServices += output.join();
        }
    }
]);