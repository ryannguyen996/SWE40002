var app = angular.module('myApp', ['angularjs-dropdown-multiselect', ]);
app.controller('TestCtrl', ['$scope', '$http', function ($scope, $http) {
    function _arrayBufferToBase64(buffer) {
        var binary = '';
        var bytes = new Uint8Array(buffer);
        var len = bytes.byteLength;
        for (var i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }
    $scope.submitButtonText = 'Submit';
    $scope.loading = false;
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
    $scope.topicSetting = {};

    $scope.$watch('lists', function (value) {
        angular.forEach($scope.lists, function (value, index) {
            $scope.unitnumber.push({
                id: value,
                label: value
            });
        });
    });

    $scope.getResults = function () {
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

            $http.get('/getimage', {responseType: "arraybuffer"}).
            then(function (response) {
                    console.log(response);
                    var str = _arrayBufferToBase64(response.data);
                    console.log(str);
                    $scope.img1 = str;
                    $scope.result = true;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                },
                function (response) {
                    $scope.message = response.data;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Submit';
                });

    };

}]);
