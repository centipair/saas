var app = angular.module("app", ['ngRoute']);

app.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
    
});

function makeUrl(url, params){
    return url+params.id;
}
app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
	when('/', {templateUrl: '/admin/dashboard', controller:"AdminCtrl"}).
	when('/sites', {templateUrl: '/admin/sites', controller:"SitesCtrl"}).
	when('/sites/edit/:id', {templateUrl: function(params){return '/admin/sites/edit/'+params.id}, controller:"SiteEditCtrl"}).
	when('/app/:app/:model/:action',  {templateUrl: function(params){
	    return '/admin/'+params.app+'/'+params.model+'?action='+params.action}}).
	when('/app/:app/:model/:action/:id', {templateUrl: function(params){
	    return '/admin/'+params.app+'/'+params.model+'?action='+params.action+'&id='+params.id}}).
	otherwise({templateUrl: '/admin/404',controller:"Admin404Ctrl"});
}]);


app.controller('AdminCtrl', function($scope, $controller, $location, Page){
    $controller('SubmitCtrl', {$scope:$scope});
    $scope.loaderMessage = "Loading...";
    $scope.notify(102);
    $scope.page = Page;
    $scope.page.title = 'Admin';
    $scope.editUrl = '';
    $scope.$on('$routeChangeStart', function() {
	$scope.notify(102);
    });
    $scope.$on('$routeChangeSuccess', function() {
	$scope.hideNotification();
    });
    $scope.$on('$routeChangeError', function(data, status) {
	console.log(data.status);
	$scope.notify(404, "Page not found");
    });
    $scope.editData = function(object){
	$location.url($scope.editUrl+object.id);
    };
});


app.controller('Admin404Ctrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Page not found"
    $scope.callback = function(data){
	console.log(data);
    }
});

app.controller('SiteEditCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Site controller"
    $scope.siteData = {};
    $scope.loaderMessage="Saving..";
    $scope.callback = function(data){
	console.log('Site Callback');
    }

});


app.controller('SitesCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "My sites"
    $scope.getDataService('/admin/sites/mine');
    $scope.editUrl = '/sites/edit/';
    $scope.getCallback = function(data){
	$scope.siteData = data;
    }
});

app.controller('PageListCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Page"
    $scope.siteData = {};
    $scope.getDataService('/admin/cms/page?action=list-data');
    $scope.editUrl = '/page/edit/';
    $scope.getCallback = function(data){
	$scope.pageData = data;
    }

});

app.service("CkEditor", function(){
    return {initEditor: function(id){
	

	CKEDITOR.replace(
	    id, 
	    {filebrowserBrowseUrl : '/login',
	     filebrowserImageBrowseUrl : '/login',
	     filebrowserFlashBrowseUrl : '/core-cdn/ckfinder/ckfinder.html?type=Flash',
	     filebrowserUploadUrl : '/file-upload',
	     filebrowserImageUploadUrl : '/admin/image-upload',
	     filebrowserFlashUploadUrl : '/core-cdn/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Flash'}
			      );
	return ;
    }};
    
    
    
});


app.filter('urlize', function(){
    return function (text){
	return text.toLowerCase().replace(/[^\w ]+/g,'').replace(/ +/g,'-');
	//return "urlized? filter?";
    }
});

app.controller('PageEditCtrl', function($scope, $controller, CkEditor){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.siteData = {};
    $scope.form = {url:"", title:""};
    $scope.loaderMessage="Saving..";
    $scope.callback = function(data){
	console.log('Page Callback');
    };
    $scope.$on('$routeChangeSuccess', function() {
	CkEditor.initEditor('description');
	
    });
    $scope.$watch('form.title', function(v){
	$scope.form.url = $scope.form.title.toLowerCase().replace(/[^\w ]+/g,'').replace(/ +/g,'-');
    });

});

app.controller('BlogListCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Blog"
    $scope.siteData = {};
    $scope.getDataService('/admin/cms/blog?action=list-data');
    $scope.editUrl = '/blog/edit/';
    $scope.getCallback = function(data){
	$scope.pageData = data;
    }

});


app.controller('BlogEditCtrl', function($scope, $controller){
    $controller('AdminCtrl', {$scope:$scope});
    $scope.page.title = "Blog"
    $scope.siteData = {};
    $scope.loaderMessage="Saving..";
    $scope.callback = function(data){
	console.log('Page Callback');
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
	console.log(data);
	var deferred = $q.defer();
	$http(
	    {url: url, 
	     data: data,
	     method: 'POST',
	     headers : {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			"X-Requested-With":"XMLHttpRequest"}
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
	    show = false;
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


app.controller('SubmitCtrl', function($scope, $controller, $http, PostData, GetData){
    $controller('NotifierCtrl', {$scope:$scope});
    $scope.errors = {};
    $scope.form = {}
    $scope.allErrors = false;
    $scope.data = {};
    $scope.submitButton={disabled: false};
    $scope.callback=function(data){
	
    };
    $scope.getCallback=function(data){
    };
    $scope.serialize = function(obj, prefix) {
	var str = [];
	for(var p in obj) {
	    var k = prefix ? prefix + "[" + p + "]" : p, v = obj[p];
	    str.push(typeof v == "object" ?
		     serialize(v, k) :
		     encodeURIComponent(k) + "=" + encodeURIComponent(v));
	}
	return str.join("&");
    };
    $scope.submitFormService=function(url){
	$scope.submitButton.disabled = true;
	$scope.submitButton.text = 'Submitting';
	$scope.notify(102, $scope.loaderMessage)
	$scope.errors = {};
	submit_data = $scope.form;
	console.log(submit_data);
	submit_data["csrfmiddlewaretoken"] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	$scope.response  = PostData.submitForm(url, $scope.serialize(submit_data)).then(
	    function (response){
		//this is success data
		$scope.submitButton.disabled=false;
		$scope.notify(200)
		$scope.callback(response.data);
	    },
	    function (response){
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
		else if(status=404){
		    $scope.notify(404);
		}
		
	    }
	);//posdata service ends
	
    };
    $scope.getDataService = function(url, data){
	$scope.getData  = GetData.getData(url).then(
	    function (response){
		//this is success data
		$scope.notify(200);
		$scope.getCallback(response.data);
	    },
	    function (response){
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
	window.location = data.redirect;
    }
});


