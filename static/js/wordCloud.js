var app = angular.module('myApp', ['tangcloud', 'angularjs-dropdown-multiselect']);
app.controller('TestCtrl', ['$scope', '$http', '$timeout', '$element', '$compile', function ($scope, $http, $timeout, $element, $compile) {
    $scope.loading = false;
    $scope.submitButtonText = 'Submit';
    $scope.result = false;

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
        scrollable: true,
        scrollableHeight: '200px',
        selectionLimit: 1,
        smartButtonMaxItems: 1
    };

    angular.forEach($scope.lists, function (value, index) {
        $scope.topic.push({
            id: value,
            label: value
        });
        $scope.topic1.push({
            id: value,
            label: value
        });
    });

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
        angular.forEach($scope.unitnumberSelected, function (value, index) {
            userInput0.push(value.id);
        });
        $scope.message = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput0.length === 0 || $scope.topicSelected.length === 0) {
            $scope.message = "Invalid input";
            $scope.loading = false;
            $scope.submitButtonText = 'Submit';
        } else {
            $http.post('/getwordcloud', {
                "unitnumber": userInput0,
                "topic": $scope.topicSelected[0].id
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
        var userInput1 = [];
        angular.forEach($scope.unitnumber1Selected, function (value, index) {
            userInput1.push(value.id);
        });
        $scope.message1 = "";
        $scope.loading = true;
        $scope.submitButtonText = 'Loading...';
        if (userInput1.length === 0 || $scope.topicSelected.length === 0) {
            $scope.message1 = "Invalid input";
            $scope.loading = false;
            $scope.submitButtonText = 'Submit';
        } else {
            $http.post('/getwordcloud', {
                "unitnumber": userInput1,
                "topic": $scope.topic1Selected[0].id
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
