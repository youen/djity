var login_dialog_html = 
		'<div id="login_dialog" class="ui-helper-hidden" title="' +gettext('Login') +'">' + 
			'<form method="post" action="." class="">' +
				'<label for="login_username">' + gettext("user")  + ' </label><br/>' + 
				'<input id="login_username" name="username" type="text"><br/>' +
				'<label for="login_password">' + gettext("password") + ' </label><br/>' + 
				'<input id="login_password" name="password" type="password"><br/>' +
			'</form>'+
		'</div>';


dj.widgets.login = 
{
	/*
	 * Djty user's login
	 */

	
	init : function(button)
	{
	/*
	 * Login Dialog
	 */

		this.button = button
			.click(function()
			{
				dj.widgets.login.open();
			})
			.addClass('dj-mini-button');

		this.dialog = $(login_dialog_html)
			.dialog(
			{
				autoOpen:false,
				modal:true,
				show:'blind',
				buttons:
				{
					'Login':function(){dj.widgets.login.login();},
					'Create an account':function()
						{
							dj.widgets.login.close();
							dj.widgets.register.open();
						
						},
				}
					
			});
		this.dialog
			.find('form').form();

	},

	open : function()
	{

		this.dialog.dialog('open');
		
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

		this.dialog.dialog('close');
		
	},

	next : function()
	{
		if(dj.context.next_page != undefined)
		{
			location.href = dj.context.next_page;
		}
		else
		{
			location.reload();
		}
	},



	

};

