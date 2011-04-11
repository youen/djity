

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

	create_table : function()
	{
		alert(options.users_roles);
		var self = this,
		options = self.options;
		
		self.table =  $("<table></table>");
		$.each(self._users_roles,function(username,role)
			{
			row_str = "<tr><th>" + username + "</th>"
			$.each(self._role,function(i,role)
				{
					row_str += '<td><input type="radio" ';
					row_str += 'name="'+ username + '"';
				    row_str += 'value="' + role + '"';
				    row_str += 'id="' + username + '-' + role + '"';
				    if( users_roles[user] = role)
					{	
						row_str += "checked"
					}
					row_str += "/>";
					row_str += "<label	for=" + user_name + "-" + role + " class='role'>";
					row_str += role + "</label></td>";

				});
			row_str += "</tr>";
			self.table.append($(row_str));
			});
		self.element.append(self.table);
	},

	open : function()
	{
		var self = this,
		options = self.options;
		dj.remote('djity.project.manage_users',{target:self._var_name})
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

	}
	


});

var manage_users;

function manage_users_dialog(){
	/*
	 * Create users management dialog
	 */
	manage_users = $('#manage_users_dialog').role_manager({
		var_name:'manage_users',
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
		open: function(event,ui){
			Dajaxice.djity.project.manage_users(
				'Dajax.process',{
					'project_name':dj.project_name,
					'module_name':dj.module_name,
					'target':'#manage_users_dialog_table'
				});
		},
	});
	*/
};

function manage_users_dialog_widgetify(){
	$('#manage_users_dialog_table label')
	.css('width','100%')
	.addClass('ui-corner-all');

	$('#manage_users_dialog_table .role').button({'disabled':true});

	$('#inherit-permissions-label').click(function(){
		$('#manage_users_dialog_table .role').button('option','disable',false);
			});

	$('#manage_users_dialog_table').buttonset();
	$('#manage_users_dialog_table th')
		.addClass('ui-widget-header');

	$('#manage_users_dialog')
		.dialog("option","width",'auto')
	    .dialog("option","height",'auto')
	    .dialog("option","position",'center')


}
function manage_users_dialog_close(){
	$('#manage_users_dialog').dialog('close');
};

function manage_users_dialog_error(message) {
	$('#manage_users_dialog_error')
	.text(message)
	.addClass('ui-state-error');
};


