var app = angular.module('myApp', ['tangcloud']);
app.controller('TestCtrl', ['$scope', '$http', '$timeout', '$element', '$compile', function ($scope, $http, $timeout, $element, $compile) {
    $scope.loading = false;
    $scope.submitButtonText = 'Submit';
    $scope.result = false;

    $scope.getResults = function () {
        var userInput0 = $scope.unitnumber;
        var userInput1 = $scope.topic;
        $scope.message = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';

        $http.post('/getwordcloud', {
            "unitnumber": userInput0,
            "topic": userInput1
        }).
        then(function (response) {
                $scope.words=JSON.parse(response.data);
                $scope.result = true;
                $scope.loading = false;
                $scope.submitButtonText = 'Submit';
            },
            function (response) {
                console.log(response.data);
                $scope.message = response.data;
                $scope.loading = false;
                $scope.submitButtonText = 'Submit';
            });


    };

    $scope.test = function (word) {
        alert("clicked on " + word);
    }
    }]);
