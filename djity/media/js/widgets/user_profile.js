dj.widgets.user_profile = 
{
	/*
	 * Djty user's profile
	 */

	
	init : function(button)
	{
	/*
	 * Profile Dialog
	 */
		this.button= button	
				.addClass('dj-mini-button')
				.click(function()
				{
					dj.widgets.user_profile.open();
				});
		
		this.dialog = $('<div id="profile_dialog" class="ui-helper-hidden" title="' + gettext('Your profile') +'"></div>')
			.keyup(function(e)
			{
				
				if( e.keyCode == 13){ dj.widgets.user_profile.validate()};
			})
			.dialog(
			{
				autoOpen:false,
				modal: true,
				show:'blind',
				buttons : {
					OK : function()
					{
						dj.widgets.user_profile.validate();
					},

					Cancel : function()
					{
						dj.widgets.user_profile.close();
					}
				},
			});

	},


	validate : function()
	{
		dj.remote('djity.portal.save_profile',
			{
				'js_target':'dj.widgets.user_profile',
				'password1': $('#id_password1').val(),
				'password2': $('#id_password2').val(),
			});

	},

	open : function()
	{

		dj.remote('djity.portal.get_profile',{'js_target':'dj.widgets.user_profile'});
	
		this.dialog.dialog('open');
		
	},

	set_profile : function(profile_html)
	{


		this.dialog
			.html(profile_html)
			.dialog("option","width","auto")
			.dialog("option","height","auto")
			.dialog("option","position","center")
			.find("form").form();
	},

	close : function(){
			

		this.dialog.dialog('close');
	},


};

