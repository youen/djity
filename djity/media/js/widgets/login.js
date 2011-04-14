var login_dialog_html = 
		'<div id="login_dialog" class="ui-helper-hidden" title="' +gettext('Login') +'">' + 
			'<p id="login_dialog_error"></p>' +
			'<form method="post" action="." class="">' +
				'<label for="login_username">' + gettext("user")  + ' </label><br/>' + 
				'<input id="login_username" name="username" type="text"><br/>' +
				'<label for="login_password">' + gettext("password") + ' </label><br/>' + 
				'<input id="login_password" name="password" type="password"><br/>' +
			'</form>'+
		'</div>';


$.widget("ui.login",
{
	/*
	 * Djty user's login
	 */

	
	_create : function()
	{
	/*
	 * Login Dialog
	 */
		var self=this,
	    element = self.element;

		dj.widgets.login =  self.element;

		self.element.dialog(
		{
			autoOpen:false,
			modal:true,
			show:'blind',
			buttons:
			{
				'Login':self.login,
			}
					
		})
		.find('form').form();

	},

	open : function()
	{
		var self=this,
	    element = self.element;

		self.element.dialog('open');
		
	},

	login : function()
	{
		dj.remote('djity.portal.login',
			{
				'js_target':'dj.widgets.login',
				'path':dj.context.path,
				'username':$('#login_username').val(),
				'password':$('#login_password').val(),
			})
	},

	close : function()
	{
		var self=this,
	    element = self.element;

		self.element.dialog('close');
		
	},

	error : function(message) {
		$('#login_dialog_error')
		.text(message)
		.addClass('ui-state-error');
	
	}

	

});

