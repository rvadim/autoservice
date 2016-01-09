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
        var weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Cб', 'Вc'];
        $scope.week = getWeek();
        $scope.times = getTimes();

        function getTimes() {
            var output = [];
            var init = 9;
            for (var i = 0; i < 9; i++) {
                output.push(init + i + ':00')
                output.push(init + i + ':30')
            }
            return output;
        }

        function getWeek() {
            var now = new Date();
            var week = [];
            for (var i = 0; i < 7; i++) {
                var date = new Date();
                date.setDate(date.getDate() + i);
                week.push(date);
            }
            return week;
        }


        $scope.selectedServices = [];

         function isServiceSelected(service) {
            var out = _.find($scope.selectedServices, function (item) {
                return item.id === service.id;
            });
            if (out) { return true; } else { return false; }
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