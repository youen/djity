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
		
		self.js_target = 'dj.widgets.user_profile';
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


	validate : function()
	{
		var self=this,
	    element = self.element;
		dj.remote('djity.portal.save_profile',
			{
				'js_target':'dj.widgets.user_profile',
				'password1': $('#id_password1').val(),
				'password2': $('#id_password2').val(),
			});

	},

	open : function()
	{

		var self=this,
	    element = self.element;
		dj.remote('djity.portal.get_profile',{'js_target':'dj.widgets.user_profile'});
	
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

