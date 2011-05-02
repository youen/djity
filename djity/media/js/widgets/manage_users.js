dj.widgets.manage_users = 
{
		/*
		 *  Djity user's manager
		 */



	init : function(inherit)
	{
	   	//inherit permissions
		if(inherit === undefined ) inherit = false;
		this.inherit = inherit;

		//init button
		this.element = $('#manage_users_button')
			.button(
			{
				icons: {primary: 'ui-icon-person'},
				text: false,
				
			})
			.click(function()
			{
				dj.widgets.manage_users.open();
				return false;
			});

		//subscription notification
		if(dj.context.awaiting_members > 0)
		{
			this.element.addClass('ui-state-error');
		}

		//init dialog
		this.dialog = $('<div/>')
		.dialog(
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
						'inherit': dj.widgets.manage_users.inherit,
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
		
	
		this.inherit_toggle(false);
		this.dialog.html($(table));
		this.dialog.buttonset();
		this.dialog.find('label')
			.css('width','100%')
			.addClass('ui-corner-all');


		this.table = this.dialog.find('table');

		this.inherit_element = this.dialog.find('#inherit-permissions')
			.change(function()
			{
				dj.widgets.manage_users.inherit_toggle();
			});

		this.table.find('th')
			.addClass('ui-widget-header');

		this.dialog
			.dialog("option","width",'500px')
			.dialog("option","height",'auto')
			.dialog("option","position",'center')

	},


	open : function()
	{
		dj.remote('djity.project.get_manage_users',
			{
				js_target:'dj.widgets.manage_users',
			})
		this.dialog.dialog('open');
	},

	inherit_toggle : function(inherit)
	{
		if(inherit === undefined) { inherit = !this.inherit}
		else{ if(inherit == this.inherit){return}}
		if(inherit)
		{
			this.table.hide('blind');
			this.inherit = true;
		}
		else
		{
			this.table.show('blind');
			this.inherit = false;
		}

	},

	close : function ()
	{
		this.dialog.dialog('close');

	}
	


};

