var AnonymousUser = 'AnonymousUser';

var login_dialog_html = 
		'<div id="login_dialog" class="ui-helper-hidden" title="' +gettext('Login') +'">' + 
			'<p id="login_dialog_error"></p>' +
			'<form method="post" action="." class="">' +
				'<label for="login_username">' + gettext("user")  + ' </label>' + 
				'<input id="login_username" name="username" type="text">' +
				'<label for="login_password">' + gettext("password") + ' </label>' + 
				'<input id="login_password" name="password" type="password">' +
			'</form>'+
		'</div>';


$.widget("ui.portal_parameters",
{
	/*
	 * Djty portal's parameter
	 */

	
	_create : function()
	{
		var self=this,
	    element = self.element;

		self.JS_target = dj.widgets.portal_parameters;
		dj.widgets.portal_parameters = self.element;

		if( dj.context.user != AnonymousUser)
		{
			self.logout_button = $('<a id="logout_button" >' + gettext("Sign out") + ' </a>')
				.addClass('dj-mini-button')
				.click(function()
				{
					dj.remote('djity.portal.logout',{});
				})
				.appendTo(self.element);

			self.profile_dialog = $('<div id="profile_dialog" class="ui-helper-hidden" title="' + gettext('Your profile') +'"></div>')
				.user_profile();

			self.profile_button = $('<a id="profile_button">' + dj.context.user  + '</a>')
				.addClass('dj-mini-button')
				.click(function()
				{
					self.profile_dialog.user_profile('open');
				})
				.appendTo(self.element);

		}
		else
		{
			
			self.login_dialog = $(login_dialog_html)
				.dialog(
				{
					autoOpen:false,
					modal:true,
					show:'blind',
					buttons:
					{
						'Login': function() 
						{
							dj.remote('djity.portal.login',
							{
									'path':dj.context.path,
									'username':$('#login_username').val(),
									'password':$('#login_password').val(),
							})

						}
					}
					
				});


			self.login_button = $('<a id="login_button" >' + gettext("Sign in") + '</a>')
				.click(function()
				{
					self.login_dialog.dialog('open');
				})
				.addClass('dj-mini-button')
				.appendTo(self.element);

			self.signup_button = $('<a id="signup_button" >' + gettext("Create an account") + '</a>')
				.addClass('dj-mini-button')
				.appendTo(self.element);


		}

		self.choose_language_button = $('<a id="choose_language_button" class="dj-mini-button">' +gettext("Language") + '</a>')
			.appendTo(self.element);

	},

	_init : function()
	{
		var self=this;

		self.element
			.buttonset()
			.show();
	}


});

$.widget("ui.user_profile",
{
	/*
	 * Djty user's profile
	 */

	
	_create : function()
	{
	/*
	 * Profile Dialog
	 */
		var self=this,
	    element = self.element;
		
		self.JS_target = 'dj.widgets.user_profile';
		dj.widgets.user_profile = self.element;
		
		self.element
			.keyup(function(e)
			{
				
				if( e.keyCode == 13){ self.element.user_profile('validate')};
			})
			.dialog(
			{
				autoOpen:false,
				modal: true,
				show:'blind',
				buttons : {
					OK : self.validate,

					Cancel : function()
					{
						$(this).dialog('close');
					}
				},
			});

	},

	keyup:function(e)
	{
		var self=this,
	    element = self.element;


	},

	validate : function()
	{
		var self=this,
	    element = self.element;
		dj.remote('djity.portal.save_profile',
			{
				'JS_target':'dj.widgets.user_profile',
				'password1': $('#id_password1').val(),
				'password2': $('#id_password2').val(),
			});

	},

	open : function()
	{

		var self=this,
	    element = self.element;
		dj.remote('djity.portal.get_profile',{'JS_target':self.JS_target});
	
		self.element.dialog('open');
		
	},

	set_profile : function(profile_html)
	{

		var self=this,
	    element = self.element;

		self.element
			.html(profile_html)
			.dialog("option","width","auto")
			.dialog("option","height","auto")
			.dialog("option","position","center")
			.find("form").form();
	},

	close : function(){
			
		var self=this,
	    element = self.element;

		self.element.dialog('close');
	},

	error : function(id,errors)
	{
		
		var self=this,
	    element = self.element;

		self.element.find(' .errorlist').remove();
		$('#'+id).before($(errors));
	}

});

$.widget("ui.register",
{
	/*
	 * Djty user's register
	 */

	
	_create : function()
	{
	/*
	 * Register Dialog
	 */

	}

});

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

	}

});
/*
 *  UGLY CODE
 */

function portal_parameters() {


	$('#login_dialog').dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
		buttons:{
			'Login': function() {
				Dajaxice.djity.portal.login(
				'Dajax.process',{
					'project_name':dj_context.project_name,
					'module_name':dj_context.module_name,
					'path':dj_context.path,
					'username':$('#login_username').val(),
					'password':$('#login_password').val(),
				});
			}
		}
	})

	register_dialog();
	profile_dialog();
	
	$('#portal_parameters a,button')
		.addClass('dj-mini-button');

	choose_language_button();
};

function login_dialog_close(){
	$('#login_dialog').dialog('close');
};

function login_dialog_error(message) {
	$('#login_dialog_error')
	.text(message)
	.addClass('ui-state-error');
};


function register_dialog(){
	/*
	 * Create users management dialog
	 */
	$('#register_dialog').dialog({
		autoOpen:false,
		modal: true,
		show:'blind',
		buttons : {
			OK : function(){

				Dajaxice.djity.portal.register(
					'Dajax.process',{
						'username': $('#id_username').val(),
						'email': $('#id_email').val(),
						'password1': $('#id_password1').val(),
						'password2': $('#id_password2').val(),
						
					});

			},
			Cancel : function(){
				$(this).dialog('close');
			}
		},
		open: function(event,ui){
			Dajaxice.djity.portal.register(
				'Dajax.process',{
					'username': '',
					'email': '',
					'password1': '',
					'password2': '',
				});
		},
	});

	$('#signup_button').click(function(){
			$('#register_dialog').dialog('open');
			return false;
		});

};

function register_dialog_post_assign(){
	$('#register_dialog')
		.dialog("option","width","auto")
		.dialog("option","height","auto")
		.dialog("option","position","center");
}



function profile_dialog_post_assign(){
	$('#profile_dialog')
		.dialog("option","width","auto")
		.dialog("option","height","auto")
		.dialog("option","position","center");
}

function choose_language_button(){
	$("#choose_language_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
	});

	$("#choose_language_dialog a")
	.each(function(i,head){
			$(head).button({
				icons:{
					primary:'dj-icon-' + $(head).attr('id').substring (5,7)
				}
				
			});
	});
		
	$("#choose_language_button")
		.button({
			icons: {
				primary: 'dj-icon-'+dj.LANGUAGE_CODE
			},
			text: false
		})
		.click(function(){
			$('#choose_language_dialog').dialog('open');
			return false;
		});
};
