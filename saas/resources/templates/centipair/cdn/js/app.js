var app = angular.module("app", ['ngRoute']);

app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
    
});


app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
	when('/', {templateUrl: '/admin/dashboard', controller:"AdminCtrl"}).
	when('/sites', {templateUrl: '/admin/sites', controller:"AdminCtrl"}).
	when('/site/edit/:id', {templateUrl: function(params){return '/admin/site/edit/'+params.id}, controller:"SiteCtrl"}).
	otherwise({redirectTo: '/'});
}]);


app.controller('AdminCtrl', function($scope, $controller, Page){
    $controller('NotifierCtrl', {$scope:$scope});
    $scope.loaderMessage = "Loading...";
    $scope.notify(102);
    $scope.page = Page;
    $scope.page.title = 'Admin Hoooi'
    $scope.$on('$routeChangeStart', function() {
	$scope.notify(102);
    });
    $scope.$on('$routeChangeSuccess', function() {
	$scope.hideNotification();
    });
    $scope.$on('$routeChangeError', function() {
	console.log('route change error');
    });
});

app.controller('SiteCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Site controller"
    $scope.siteData = {};
    $scope.callback = function(data){
	console.log('callback');
    }
});


app.factory("Page", function(){
    return {title: "Site Administration"};
});


app.factory("Notifier", function(){
    return {show:false, message:"Loading...", class:"notify-loading"};
});

app.service("Callback", function(){
    this.registrationSuccess = function(data){
	console.log(data);
    };
});

app.service("PostData", function($http, $q, Notifier){
    
    return {submitForm: function(url, data){
	var deferred = $q.defer();
	$http(
	    {url: url, 
	     data: data,
	     method: 'POST',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
	    }).error(function (data, status) {
		response = {data: data, status: status};
		deferred.reject(response);
		
	    }).success(function (data){
		response = {data:data, status:200};
		deferred.resolve(response);
	    });
	return deferred.promise;
    }};
});

app.service("GetData", function($http, $q, Notifier){
    return {getData:function(url, data){
	var deferred = $q.defer();
	$http(
	    {url: url, 
	     data: data,
	     method: 'GET',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
	    }).error(function (data, status) {
		response = {data: data, status: status};
		deferred.reject(response);
		
	    }).success(function (data){
		response = {data:data, status:200};
		deferred.resolve(response);
	    });
	return deferred.promise;
	
    }};
});


app.directive("submit", function(){
    return function (scope, element, attrs){
	element.bind("click", function (){
	    scope.submitFormService(attrs.url);
	})
    }
});


function NotifierCtrl($scope, Notifier){
    $scope.notifier = Notifier;
    $scope.loaderMessage = "Loading";
    $scope.notify = function(code, message){
	var show = true;
	switch (code)
	{
	    case 102:
	    Notifier.class = "notify-loading";
	    Notifier.message = $scope.loaderMessage
	    break;
	    case 404:
	    Notifier.class = "notify-error";
	    Notifier.message = "Requested resource not found";
	    break;
	    case 500:
	    Notifier.class = "notify-error";
	    Notifier.message = "Server error. Please try again after sometime";
	    break;
	    case 422:
	    Notifier.class = "notify-error";
	    Notifier.message = "Submitted data is invalid";
	    break;
	    case 403:
	    Notifier.class = "notify-error";
	    Notifier.message = "Permission denied for this process";
	    break;
	    case 200:
	    console.log("200 ok");
	    console.log(message);
	    show = true;
	    break;
	    default:
	    Notifier.class = "notify-loading";
	    Notifier.message = "Unknown response";
	    
	}
	if (message != undefined){
	    Notifier.message = message;
	}
	Notifier.show = show;
	
    };
    $scope.hideNotification = function(){
	Notifier.show = false;
	Notifier.message = "";
    };
}


app.controller('SubmitCtrl', function($scope, $controller, $http, PostData){
    $controller('NotifierCtrl', {$scope:$scope});
    $scope.errors = {};
    $scope.form = {}
    $scope.allErrors = false;
    $scope.data = {};
    $scope.submitButton={disabled: false};
    $scope.callback=function(data){
	
    };
    $scope.submitFormService=function(url){
	$scope.submitButton.disabled = true;
	$scope.submitButton.text = 'Submitting';
	$scope.notify(102, $scope.loaderMessage)
	$scope.errors = {};
	submit_data = $scope.form;
	submit_data["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	$scope.response  = PostData.submitForm(url, $.param(submit_data)).then(
	    function (data){
		//this is success data
		$scope.submitButton.disabled=false;
		$scope.notify(200)
		$scope.callback(data);
	    },
	    function (data){
		//this is invoked during error
		$scope.submitButton.disabled=false;
		data = response.data;
		status = response.status;
		if (status==422){
		    $scope.notify(422, data.message)
		    errors = {};
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
		    $scope.notify(500);
		}
		
	    }
	);//posdata service ends
	$scope.getResponse  = GetData.getData(url, $.param(submit_data)).then(
	    function (data){
		//this is success data
		console.log(data);
		$scope.notify(200)
		$scope.callback(data);
	    },
	    function (data){
		//this is invoked during error
		data = response.data;
		status = response.status;
		console.log(data);
		
	    }
	);
	
    };
    
});

app.controller('RegisterCtrl', function($scope, $controller){
    $controller('SubmitCtrl', {$scope:$scope});
    $scope.callback = function(data){
	alert("registraion success");
	console.log("Registration success");
	console.log(data);
    }
});

app.controller('LoginCtrl', function($scope, $controller){
    $controller('SubmitCtrl', {$scope:$scope});
    $scope.loaderMessage = "Logging in...";
    $scope.callback = function(data){
	window.location = "/admin"
    }
});


