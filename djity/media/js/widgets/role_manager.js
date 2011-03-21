

$.widget("ui.role_manager",{
		/*
		 *  Djity user's role manager
		 */

	options : {
		inherit_permissions:true, //inherit permissions
		errors:[],// error messages
		},

	_create : function()
	{
		var self=this,
		options =self.options,
		id = self.element.id;
	},

	_init : function()
	{
		var self = this,
		options = self.options;

		self._inherit_permissions = options.inherit_permissions;

	},

	inherit_toggle : function()
	{
		var self = this,
		options = self.options,
		inherit = self._inherit;
		if( inherit)
		{
			self._inherit = false;
		}
		else
		{
			self._inherit = true;
		}

	},

	close : function ()
	{

	}
	


});

