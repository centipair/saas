var app = angular.module("app", []);
 
app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
    
});

app.factory("callbacks", function(){
    return {"hello":"world"}
});

function redirect(url){
    window.location.href=url;
}

function invalidAction(){
    console.log("Submit success.Invalid action sepcified");
}

function SubmitCtrl($scope, $http){
    $scope.errors = {};
    $scope.showForm = true;
    $scope.form = {}
    $scope.allErrors = false;
    $scope.handleSuccess = function(data){
	if (data.action){
	    switch (data.action){
		case "redirect":
		redirect(data.url);
		break;
		default:
		invalidAction();
	    }
	}
    }
    $scope.callbackFunction = function(){
	console.log("scope callback")
    }
    $scope.submit=function(url, showResult){
	$scope.errors = {};
	console.log($scope.form);
	//$scope.form["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	submit_data = $scope.form
	submit_data["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	console.log(submit_data);
	$http(
	    {url: url, 
	     data: $.param(submit_data),
	     method: 'POST',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
	    }).success(function (data) {
		console.log(data);
		if (showResult){
		    $scope.showForm = false;
		    $scope.showSubmitResult = true;
		}
	    }).error(function(data, status, headers, config) {
		// called asynchronously if an error occurs
		// or server returns response with an error status.
		if (status==422){
		    errors = data.errors;
		    for(var index in data.errors) {
			errors[index + "Class"] = "has-error";
		    }
		    $scope.errors = errors;
		    $scope.all_errors = '__all__' in data.errors;
		    console.log($scope.errors);
		}else if (status==500){
		    alert("server error");
		}
		
	    });
	
    }
}

