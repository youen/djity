

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


function manage_users_dialog(){
	/*
	 * Create users management dialog
	 */
	$('#manage_users_dialog').dialog({
		autoOpen:false,
		modal: true,
		show:'blind',
		buttons : {
			OK : function(){
				
				users = {};
				$(this).find('input:radio:checked')
				.each(function(i){
						users[this.name] = $(this).val();
				});

				Dajaxice.djity.project.manage_users(
					'Dajax.process',{
						'project_name':dj.project_name,
						'module_name':dj.module_name,
						'path':path,
						'users': users,
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


