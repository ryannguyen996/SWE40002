var app = angular.module('myApp', ['angular-d3-word-cloud', 'angularjs-dropdown-multiselect']);
app.controller('TestCtrl', ['$scope', '$http', '$timeout', '$element', '$compile', function ($scope, $http, $timeout, $element, $compile) {
    $scope.loading = false;
    $scope.submitButtonText = 'Submit';
    $scope.result = false;
    $scope.result1 = false;
    console.log($scope.lists);
    $scope.unitnumberSelected = [];
    $scope.unitnumber = [];
    $scope.topicSelected = [];
    $scope.topic = [{
        id: "assessment",
        label: "assessment"
    }, {
        id: "class",
        label: "class"
    }, {
        id: "teacher",
        label: "teacher"
    }, {
        id: "resource",
        label: "resource"
    }, {
        id: "other",
        label: "other"
    }];
    $scope.unitnumber1Selected = [];
    $scope.unitnumber1 = [];
    $scope.topic1Selected = [];
    $scope.topic1 = $scope.topic;

    $scope.unitSetting = {
        scrollable: true,
        scrollableHeight: '250px',
        enableSearch: true,
        smartButtonMaxItems: 3
    };
    $scope.topicSetting = {
        smartButtonMaxItems: 3
    };

//        angular.forEach($scope.lists, function (value, index) {
//            $scope.topic.push({
//                id: value,
//                label: value
//            });
//            $scope.topic1.push({
//                id: value,
//                label: value
//            });
//        });

    $scope.$watch('lists', function (value) {
        angular.forEach($scope.lists, function (value, index) {
            $scope.unitnumber.push({
                id: value,
                label: value
            });
            $scope.unitnumber1.push({
                id: value,
                label: value
            });
        });
    });

    $scope.getResults = function () {
        $scope.result = false;
        $scope.words = [];
        var userInput0 = [];
        var userInput1 = [];
        $scope.count = "";
        $scope.avg = "";
        angular.forEach($scope.unitnumberSelected, function (value, index) {
            userInput0.push(value.id);
        });
        angular.forEach($scope.topicSelected, function (value, index) {
            userInput1.push(value.id);
        });
        $scope.message = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput0.length === 0) {
            $scope.message = "Invalid input";
            $scope.loading = false;
            $scope.submitButtonText = 'Submit';
        } else {
            $http.post('/getwordcloudcount', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    console.log(response.data);
                    $scope.count = response.data;
                },
                function (response) {
                    console.log(response.data);
                    $scope.count = response.data;
                });
            $http.post('/getavg', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    console.log(response.data);
                    $scope.avg = response.data;
                },
                function (response) {
                    console.log(response.data);
                    $scope.avg = response.data;
                });
            $http.post('/getwordcloud', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    console.log(response.data);
                    $scope.words = JSON.parse(response.data);
                    $scope.result = true;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                },
                function (response) {
                    $scope.message = response.data;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                });
        }
    };

    $scope.getResults1 = function () {
        $scope.result1=false;
        $scope.words1 = [];
        var userInput0 = [];
        var userInput1 = [];
        $scope.count1 = "";
        $scope.avg1= "";
        angular.forEach($scope.unitnumber1Selected, function (value, index) {
            userInput0.push(value.id);
        });
        angular.forEach($scope.topic1Selected, function (value, index) {
            userInput1.push(value.id);
        });
        $scope.message1 = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput0 === 0) {
            $scope.message1 = "Invalid input";
            $scope.loading = false;
            $scope.submitButtonText = 'Submit';
        } else {
            $http.post('/getwordcloudcount', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    console.log(response.data);
                    $scope.count1 = response.data;
                },
                function (response) {
                    console.log(response.data);
                    $scope.count1 = response.data;
                });
            $http.post('/getavg', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    console.log(response.data);
                    $scope.avg1 = response.data;
                },
                function (response) {
                    console.log(response.data);
                    $scope.avg1 = response.data;
                });
            $http.post('/getwordcloud', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    $scope.words1 = JSON.parse(response.data);
                    $scope.result1 = true;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                },
                function (response) {
                    $scope.message1 = response.data;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                });
        }
    };


    }]);
