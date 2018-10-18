// the javascript
var app = angular.module('myapp', []);
//
// Reusable Uploader service.
//
app.factory('Uploader', function($q, $rootScope) {
    this.upload = function(url, file) {
        var deferred = $q.defer(),
            formdata = new FormData(),
            xhr = new XMLHttpRequest();
        formdata.append('file', file);
        xhr.onreadystatechange = function(r) {
            if (4 === this.readyState) {
                if (xhr.status == 200) {
                    $rootScope.$apply(function() {
                        deferred.resolve(xhr);
                    });
                } else {
                    $rootScope.$apply(function() {
                        deferred.reject(xhr);
                    });
                }
            }
        }
        xhr.open("POST", url, true);
        xhr.send(formdata);
        return deferred.promise;
    };
    return this;
})
//
// fileChange directive because ng-change doesn't work for file inputs.
//
app.directive('fileChange', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('change', function() {
                scope.$apply(function() {
                    scope[attrs['fileChange']](element[0].files);
                })
            })
        },
    }
})
//
// Example controller
//
app.controller('UploadController', function($log, $scope, $http, Uploader) {
    $scope.loading = false;
    $scope.message ="";

    $scope.upload = function(files) {
        $scope.loading = true;
        var r = Uploader.upload('/uploads', files[0]);
        r.then(
            function(r) {
                $scope.loading = false;
                console.log(r.response);
                $scope.message = r.response;
            },
            function(r) {
                $scope.loading = false;
                console.log(r.response);
                $scope.message = r.response;
            });
    }
});
