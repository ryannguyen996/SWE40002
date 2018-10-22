var app = angular.module('myApp', ['angularjs-dropdown-multiselect', ]);
app.controller('TestCtrl', ['$scope', '$http', function ($scope, $http) {
    $scope.submitButtonText = 'Download';
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
        smartButtonMaxItems: 3
    };
    $scope.topicSetting = {
        smartButtonMaxItems: 3
    };

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
        console.log($scope.selection)
        if (userInput0.length === 0) {
            $scope.message = "Invalid input";
            $scope.loading = false;
            $scope.submitButtonText = 'Download';
        } else {
            //$scope.img1 = "";
            //            $http.post('/downloadcsv', {
            //                "unitnumber": userInput0,
            //                "topic": userInput1
            //            }, {
            //                responseType: "arraybuffer"
            //            }).
            //            then(function (response) {
            //                    console.log(response);
            //                    var str = _arrayBufferToBase64(response.data);
            //                    console.log(str);
            //                    $scope.img1 = str;
            //                    $scope.result = true;
            //                    $scope.loading = false;
            //                    $scope.submitButtonText = 'Download';
            //                },
            //                function (response) {
            //                    $scope.message = response.data;
            //                    $scope.loading = false;
            //                    $scope.submitButtonText = 'Download';
            //                });
            $http.post('/downloadcsv', {
                "unitnumber": userInput0,
                "topic": userInput1
            }, {
                responseType: "arraybuffer"
            }).then(function (response) {
                    headers = response.headers();
                    console.log(response.headers['x-filename']);
                    var filename = headers['x-filename'];
                    var contentType = headers['content-type'];

                    var linkElement = document.createElement('a');
                    try {
                        var blob = new Blob([response.data], {
                            type: contentType
                        });
                        var url = window.URL.createObjectURL(blob);

                        linkElement.setAttribute('href', url);
                        linkElement.setAttribute("download", filename);

                        var clickEvent = new MouseEvent("click", {
                            "view": window,
                            "bubbles": true,
                            "cancelable": false
                        });
                        linkElement.dispatchEvent(clickEvent);
                        $scope.loading = false;
                        $scope.submitButtonText = 'Download';
                    } catch (ex) {
                        console.log(ex);
                    }
                },
                function (response) {
                    $scope.message = response.data;
                    $scope.loading = false;
                    $scope.submitButtonText = 'Download';
                });

        }
    };

            }]);
