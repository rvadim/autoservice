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

app.controller('LandingController', ['$scope', 'Service', 'Job', 'NgTableParams',
    function ($scope, Service, Job, NgTableParams) {
        $scope.selectedServices = [];
        $scope.week = getWeek();
        $scope.times = getTimes();
        $scope.day = null;
        $scope.time = null;

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

        // EventHandlers

        $scope.selectService = function (item) {
            if (isServiceSelected(item)) {
                removeServiceFromSelected(item);
                item.$selected = false;
            } else {
                addServiceToSelected(item);
                item.$selected = true;
            }
        };

        $scope.selectTime = function (day, time) {
            $scope.day = day;
            $scope.time = time;
        };

        $scope.sendServiceRequest = function () {
            var arr = $scope.time.split(':');
            var job = new Job();
            job.client = $scope.client;
            $scope.day.setHours(arr[0]);
            $scope.day.setMinutes(arr[1]);
            console.log($scope.day);
            job.date = $scope.day;
            job.selected_services = $scope.selectedServices;
            Job.save({}, job,
                function (result) {
                    console.log(result);
                },
                function (result) {
                    console.log(result);
                }
            );
            /*
            if ($scope.form.$invalid) {
                console.log('Form is invalid')
            }
            */
        }
    }
]);