$.widget("ui.manage_users",{
		/*
		 *  Djity user's manager
		 */

	options : {
		inherit_permissions:true, //inherit permissions
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
		self._users_roles = options.users_roles;
		self._roles = options.roles;
		self._id =  self.element.attr('id');

		self.element.dialog(
		{
			autoOpen:false,
			modal: true,
			show:'blind',
			buttons : 
			{
				OK : function()
				{
					users = {};
					$(this).find('input:radio:checked')
						.each(function(i){
							users[this.name] = parseInt($(this).val());
						});

					dj.remote('djity.project.save_manage_users',
						{
						'inherit': self.options.inherit_permissions,
						'users': users,
						'js_target':'dj.widgets.manage_users',
						});
				},
		
				Cancel : function()
				{
					$(this).dialog('close');
				}
			},
		});


	},

	create_table : function(table)
	{
		var self = this,
		options = self.options;
		
		self.table =  $(table)
		self.element.html(self.table);
		self.element.buttonset();
		self.element.find('label')
		.css('width','100%')
		.addClass('ui-corner-all');


		self.element.find('#inherit-permissions')
			.change(function()
			{
				dj.widgets.manage_users.manage_users('inherit_toggle');
			});

		self.table.find('th')
			.addClass('ui-widget-header');

		self.element
			.dialog("option","width",'500px')
			.dialog("option","height",'auto')
			.dialog("option","position",'center')


	},

	error : function (message)
   	{
		var self = this,
		options = self.options;
		self.element.find('.error')
			.text(message)
			.addClass('ui-state-error');
	},

	open : function()
	{
		var self = this,
		options = self.options;
		dj.remote('djity.project.get_manage_users',
			{
				js_target:'dj.widgets.manage_users',
			})
		self.element.dialog('open');
	},

	inherit_toggle : function(inherit)
	{
		var self = this,
		options = self.options;
		if(inherit === undefined) { inherit = !self.options.inherit_permissions}
		else{ if(inherit == self.options.inherit_permissions){return}}
		if(inherit)
		{
			self.element.find('table').hide('blind');
			self.options.inherit_permissions = true;
		}
		else
		{
			self.element.find('table').show('blind');
			self.options.inherit_permissions = false;
		}

	},

	close : function ()
	{
		var self = this,
		options = self.options,
		inherit = self._inherit;
		self.element.dialog('close');

	}
	


});


function manage_users_dialog(){
	/*
	 * Create users management dialog
	 */
	/*
		buttons : {
			OK : function(){
				
				users = {};
				$(this).find('input:radio:checked')
				.each(function(i){
						users[this.name] = $(this).val();
				});

				Dajaxice.djity.project.manage_users(
					'Dajax.process',{
						'project_name':dj_context.project_name,
						'module_name':dj_context.module_name,
						'path':dj_context.path,
						'users': dj_context.users,
						'target':'#manage_users_dialog'
					});

			},
			Cancel : function(){
				$(this).dialog('close');
			}
		},
	});
	*/
};





