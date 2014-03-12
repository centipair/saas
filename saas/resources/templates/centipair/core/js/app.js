var app = angular.module("app", []);
 
app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
    
});

app.factory("callbacks", function(){
    return {"hello":"world"}
});

app.factory("Alert", function(){
    return {"message": "" ,"class":""};
});

app.factory("Loader", function(){
    return {show:false, message:""};
})


app.directive("submit", function(){
    return function (scope, element, attrs){
	element.bind("click", function (){
	    scope.submitForm(attrs.url);
	})
    }
});



function AlertCtrl($scope, Alert){
    $scope.alert = Alert;
}

function LoaderCtrl($scope, Loader){
    $scope.loader = Loader;
}



function SubmitCtrl($scope, $http, Alert, Loader){
    $scope.errors = {};
    $scope.form = {}
    $scope.allErrors = false;
    $scope.alert = Alert;
    $scope.loader = Loader;
    
    $scope.submitForm=function(url){
	$scope.loader.show=true;
	$scope.errors = {};
	$scope.alert.class = "";
	$scope.alert.message = "";
	submit_data = $scope.form;
	submit_data["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	$http(
	    {url: url, 
	     data: $.param(submit_data),
	     method: 'POST',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
	    }).success(function (data) {
		$scope.loader.show=false;
		
	    }).error(function(data, status, headers, config) {
		// called asynchronously if an error occurs
		// or server returns response with an error status.
		$scope.loader.show=false;
		if (status==422){
		    errors = {};
		    $scope.alert.message = data.message;
		    $scope.alert.class = "alert-danger";
		    for(var index in data.errors) {
			errors[index + "Class"] = "has-error";
			error_string = "";
			for(var i=0;i<data.errors[index].length;i++){
			    error_string = error_string + data.errors[index][i] ;
			}
			errors[index] = error_string;
		    }
		    $scope.errors = errors;
		    $scope.allErrors = '__all__' in data.errors;
		    
		}else if (status==500){
		    alert("server error");
		}
		
	    });
	
    }
}

