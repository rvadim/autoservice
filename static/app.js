'use strict';

var app = angular.module('AutoService', [
    'angular-loading-bar',
    'ngRoute',
    'ngMessages',
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
});

var phoneRegexp = /^\(?(\d{3})\)?[ .-]?(\d{3})[ .-]?(\d{4})$/;
app.directive('phone', function($q, $timeout) {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$asyncValidators.phone = function(modelValue, viewValue) {
        if (ctrl.$isEmpty(modelValue)) {
          // consider empty model valid
          return $q.when();
        }
        var def = $q.defer();
        $timeout(function() {
          // Mock a delayed response
          if (phoneRegexp.test(modelValue)) {
            def.resolve();
          } else {
            def.reject();
          }

        }, 1000);

        return def.promise;
      };
    }
  };
});
