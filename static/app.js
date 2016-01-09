'use strict';

var app = angular.module('AutoService', [
    'angular-loading-bar',
    'ngRoute',
    'AutoService.Landing',
    'AutoServiceAPI'
]);

app.config(['$routeProvider', '$resourceProvider',
    function ($routeProvider, $resourceProvider) {
        $routeProvider.otherwise({ redirectTo: '/landing' });
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }
]);

app.directive('loadingContainer', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function(scope, element, attrs) {
            var loadingLayer = angular.element('<div class="loading"></div>');
            element.append(loadingLayer);
            element.addClass('loading-container');
            scope.$watch(attrs.loadingContainer, function(value) {
                loadingLayer.toggleClass('ng-hide', !value);
            });
        }
    };
})
