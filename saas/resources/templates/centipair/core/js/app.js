var app = angular.module("app", []);
 
app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
    
});

app.factory("Alert", function(){
    return {"message": "" ,"class":""};
});

app.factory("Loader", function(){
    return {show:false, message:""};
})

app.service("Callback", function(){
    this.registrationSuccess = function(data){
	console.log(data);
    };
});

app.service("PostData", function($http, $q, Alert, Loader){
    
    return {submitForm: function(url, data){
	var deferred = $q.defer();
	$http(
	    {url: url, 
	     data: data,
	     method: 'POST',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
	    }).error(function (data, status) {
		Loader.show=false;
		response = {data: data, status: status};
		deferred.reject(response);
		
	    }).success(function (data){
		response = {data:data, status:200};
		deferred.resolve(response);
	    });
	return deferred.promise;
    }}
});


app.directive("submit", function(){
    return function (scope, element, attrs){
	element.bind("click", function (){
	    scope.submitFormService(attrs.url);
	})
    }
});



function AlertCtrl($scope, Alert){
    $scope.alert = Alert;
}

function LoaderCtrl($scope, Loader){
    $scope.loader = Loader;
}



function SubmitCtrl($scope, $http, Alert, Loader, PostData){
    $scope.errors = {};
    $scope.form = {}
    $scope.allErrors = false;
    $scope.alert = Alert;
    $scope.loader = Loader;
    $scope.data = {};
    $scope.callback = function(data){
    };
    $scope.submitFormService=function(url){
	Loader.show=true;
	$scope.errors = {};
	$scope.alert.class = "";
	$scope.alert.message = "";
	submit_data = $scope.form;
	submit_data["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	$scope.response  = PostData.submitForm(url, $.param(submit_data)).then(
	    function (data){
		$scope.loader.show=false;
		$scope.callback(data);
	    },
	    function (data){
		data = response.data;
		status = response.status;
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
		    $scope.loader.show=false;
		    alert("server error");
		}
		
	    }
	);
	
    };
    
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
		$scope.data = data;
		$scope.$apply("registrationSuccess");
		$scope.loader.show=false;
		$scope.data = data;
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
	
    };
}

app.controller('RegisterCtrl', function($scope, $controller){
    $controller('SubmitCtrl', {$scope:$scope});
    $scope.callback = function(data){
	console.log("register control callback");
	console.log(data);
    }
});

app.controller('LoginCtrl', function($scope, $controller){
    $controller('SubmitCtrl', {$scope:$scope});
    $scope.callback = function(data){
	console.log("login control callback");
	console.log(data);
    }
});
