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
		var self=this,
	    element = self.element;
		
		self.JS_target = 'dj.widgets.register';
		dj.widgets.register = self.element;
		
		self.element
			.keyup(function(e)
			{
				
				if( e.keyCode == 13){ self.element.register('validate')};
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
						$(this).register('close');
					}
				},
			});


	},

	validate : function()
	{
		var self=this,
	    element = self.element;
		dj.remote('djity.portal.register',
			{
				'js_target':'dj.widgets.register',
				'username': $('#id_username').val(),
				'email': $('#id_email').val(),
				'password1': $('#id_password1').val(),
				'password2': $('#id_password2').val(),
			});

	},

	open : function()
	{

		var self=this,
	    element = self.element;
		dj.remote('djity.portal.get_register',{'js_target':'dj.widgets.register'});
	
		self.element.dialog('open');
		
	},

	set_form : function(form_html)
	{

		var self=this,
	    element = self.element;

		self.element
			.html(form_html)
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

