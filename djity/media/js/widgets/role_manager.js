$.widget("ui.role_manager",{
		/*
		 *  Djity user's role manager
		 */

	options : {
		inherit_permissions:true, //inherit permissions
		users_role:{youen:"admin"},// users
		roles:[('admin',1)],// permission
		error_messages:[],
		var_name:'role_manager', //name for callback function (no DOM access optimisation)
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
		self._var_name = options.var_name;

		self.element.dialog(
		{
			autoOpen:false,
			modal: true,
			show:'blind',
		});


	},

	create_table : function(table)
	{
		var self = this,
		options = self.options;
		
		self.table =  $(table);
		self.element.html(self.table);
		self.table.find('label')
		.css('width','100%')
		.addClass('ui-corner-all');

		self.table.find('.role').button({'disabled':true});

		$('#inherit-permissions-label').click(function(){
			$('#manage_users_dialog_table .role').button('option','disable',false);
			});

		self.table.buttonset();
		self.table.find('th')
			.addClass('ui-widget-header');

		self.element
			.dialog("option","width",'auto')
			.dialog("option","height",'auto')
			.dialog("option","position",'center')


	},

	error : function (message)
   	{
		var self = this,
		options = self.options;
		self.errorbox
			.text(message)
			.addClass('ui-state-error');
	},

	open : function()
	{
		var self = this,
		options = self.options;
		dj.remote('djity.project.manage_users',{JS_target:self._var_name})
		self.element.dialog('open');
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
		var self = this,
		options = self.options,
		inherit = self._inherit;
		self.element.dialog('close');

	}
	


});

var manage_users;

function manage_users_dialog(){
	/*
	 * Create users management dialog
	 */
	dj.manage_users = $('#manage_users_dialog').role_manager({
		var_name:'dj.manage_users',
	});
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





