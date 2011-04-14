var AnonymousUser = 'AnonymousUser';



dj.functions.portal_parameters = function (){
	dj.widgets.portal_parameters = $('#portal_parameters')

		var self=this,
	    element = dj.widgets.portal_parameters;

		self.JS_target = dj.widgets.portal_parameters;
		dj.widgets.portal_parameters = dj.widgets.portal_parameters;

		if( dj.context.user != AnonymousUser)
		{
			self.logout_button = $('<a id="logout_button" >' + gettext("Sign out") + ' </a>')
				.addClass('dj-mini-button')
				.click(function()
				{
					dj.remote('djity.portal.logout',{});
				})
				.appendTo(dj.widgets.portal_parameters);

			self.profile_dialog = $('<div id="profile_dialog" class="ui-helper-hidden" title="' + gettext('Your profile') +'"></div>')
				.user_profile();

			self.profile_button = $('<a id="profile_button">' + dj.context.user  + '</a>')
				.addClass('dj-mini-button')
				.click(function()
				{
					self.profile_dialog.user_profile('open');
				})
				.appendTo(dj.widgets.portal_parameters);

		}
		else
		{
			
			self.login_dialog = $(login_dialog_html)
				.login();



			self.login_button = $('<a id="login_button" >' + gettext("Sign in") + '</a>')
				.click(function()
				{
					self.login_dialog.login('open');
				})
				.addClass('dj-mini-button')
				.appendTo(dj.widgets.portal_parameters);

			self.register_dialog = $('<div id="register_dialog" class="ui-helper-hidden" title="' + gettext('Create an account') +'"></div>')
				.register();
			
			self.register_button = $('<a id="register_button" >' + gettext("Create an account") + '</a>')
				.click(function()
				{
					self.register_dialog.register('open');
				})
				.addClass('dj-mini-button')
				.appendTo(dj.widgets.portal_parameters);


		}

		//language dialog widgetify

		$("#choose_language_dialog").dialog({
			autoOpen:false,
			modal:true,
			show:'blind',
		})
		.buttonset();

		$("#choose_language_dialog a")
		.each(function(i,head){
			$(head).button({
				icons:{
					primary:'dj-icon-' + $(head).attr('id').substring (5,7)
				}
				
			});
		});

		self.choose_language_button = $('<a id="choose_language_button" class="dj-mini-button">' +gettext("Language") + '</a>')
			.button(
			{
				icons: {primary: 'dj-icon-'+dj.context.LANGUAGE_CODE},
				text: false
			})
			.click(function(){
				$('#choose_language_dialog').dialog('open');
			})
			.appendTo(dj.widgets.portal_parameters);

		var self=this;

		dj.widgets.portal_parameters
			.buttonset()
			.show();


};




