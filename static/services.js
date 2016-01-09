'use strict';

var services = angular.module('AutoServiceAPI', ['ngResource']);

var API_PATH = '/api/';

services.factory('Station', ['$resource',
    function ($resource) {
        return $resource(API_PATH + 'station/:stationId', {}, {
            query: { method: 'GET' }
        });
    }
]).factory('Service', ['$resource',
    function ($resource) {
        return $resource(API_PATH + 'service/', {}, {
            query: { method:'GET', isArray: true }
        });
    }
]);