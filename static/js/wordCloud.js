var app = angular.module('myApp', ['tangcloud', 'angularjs-dropdown-multiselect']);
app.controller('TestCtrl', ['$scope', '$http', '$timeout', '$element', '$compile', function ($scope, $http, $timeout, $element, $compile) {
    $scope.loading = false;
    $scope.submitButtonText = 'Submit';
    $scope.result = false;
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
        id: "lecture",
        label: "lecture"
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
        smartButtonMaxItems: 4
    };
    $scope.topicSetting = {
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
        $scope.words = [];
        var userInput0 = [];
        var userInput1 = [];
        angular.forEach($scope.unitnumberSelected, function (value, index) {
            userInput0.push(value.id);
        });
        angular.forEach($scope.topicSelected, function (value, index) {
            userInput1.push(value.id);
        });
        $scope.message = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput0.length === 0 || userInput1.length === 0) {
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
            $http.post('/getwordcloud', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
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
        $scope.words1 = [];
        var userInput0 = [];
        var userInput1 = [];
        angular.forEach($scope.unitnumber1Selected, function (value, index) {
            userInput0.push(value.id);
        });
        angular.forEach($scope.topic1Selected, function (value, index) {
            userInput1.push(value.id);
        });
        $scope.message1 = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput1.length === 0 || userInput0 === 0) {
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
            $http.post('/getwordcloud', {
                "unitnumber": userInput0,
                "topic": userInput1
            }).
            then(function (response) {
                    $scope.words1 = JSON.parse(response.data);
                    $scope.result = true;
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

    $scope.test = function (word) {
        alert("clicked on " + word);
    };

    }]);
