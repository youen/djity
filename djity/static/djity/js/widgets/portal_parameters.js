var AnonymousUser = 'AnonymousUser';



dj.functions.portal_parameters = function (){
	dj.widgets.portal_parameters = $('#portal_parameters')

		var self=this,
	    element = dj.widgets.portal_parameters;

		self.JS_target = dj.widgets.portal_parameters;
		dj.widgets.portal_parameters = dj.widgets.portal_parameters;

		if( dj.context.user != AnonymousUser)
		{
			logout_button = $('<a id="logout_button" >' + gettext("Sign out") + ' </a>')
				.addClass('dj-mini-button')
				.click(function()
				{
					dj.remote('djity.portal.logout',{});
				})
				.appendTo(dj.widgets.portal_parameters);


			profile_button = $('<a id="profile_button">' + dj.context.user  + '</a>')
				.appendTo(dj.widgets.portal_parameters);

			dj.widgets.user_profile.init(profile_button);
		}
		else
		{
			

			login_button = $('<a id="login_button" >' + gettext("Sign in") + '</a>')
				.appendTo(dj.widgets.portal_parameters);

			dj.widgets.login.init(login_button);
			
			register_button = $('<a id="register_button" >' + gettext("Create an account") + '</a>')
				.addClass('dj-mini-button')
				.appendTo(dj.widgets.portal_parameters);

			dj.widgets.register.init(register_button)

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

		choose_language_button = $('<a id="choose_language_button" class="dj-mini-button">' +gettext("Language") + '</a>')
			.button(
			{
				icons: {primary: 'dj-icon-'+dj.context.LANGUAGE_CODE},
				text: false
			})
			.click(function(){
				$('#choose_language_dialog').dialog('open');
			})
			.appendTo(dj.widgets.portal_parameters);


		dj.widgets.portal_parameters
			.buttonset()
			.show();


};




