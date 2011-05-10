

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

		bt_opts ={};
		bt_opts[gettext('Sign in')] = function(){dj.widgets.login.login();};
		bt_opts[gettext('Create an account')] = function()
		{
			dj.widgets.login.close();
			dj.widgets.register.open();
	
		};

		this.dialog = $('#login_dialog')
			.keyup(function(e)
			{
				if( e.keyCode == 13){ dj.widgets.login.login()};
			})
			.dialog(
			{
				autoOpen:false,
				modal:true,
				show:'blind',
				buttons:bt_opts,
					
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

