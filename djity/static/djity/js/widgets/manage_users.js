dj.widgets.manage_users = 
{
		/*
		 *  Djity user's manager
		 */



	init : function(inherit,forbid)
	{
	   	//inherit permissions
		if(inherit === undefined ) inherit = false;
		this.inherit = inherit;

		//forbid subscriptions
		if(forbid === undefined ) forbid = false;
		this.forbid = forbid;
		
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
			this.element.addClass('ui-state-highlight');
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
						'forbid': dj.widgets.manage_users.forbid,
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
		
	
		this.dialog.html($(table));


		this.dialog.buttonset();
		this.dialog.find('label')
			.css('width','100%')
			.addClass('ui-corner-all');


		this.table = this.dialog.find('table');
		this.inherit_members = this.dialog.find('#inherit-members');

		this.inherit_element = this.dialog.find('#inherit-permissions')
			.change(function()
			{
				dj.widgets.manage_users.inherit_toggle();
			});

		this.forbid_element = this.dialog.find('#forbid-subscriptions')
			.change(function()
			{
				dj.widgets.manage_users.forbid_toggle();
			});

		this.table.find('th')
			.addClass('ui-widget-header');

		this.inherit_toggle(this.dialog.find("#inherit-permissions:checkbox:checked").get().length == 1);
		this.forbid_toggle(this.dialog.find("#forbid-subscriptions:checkbox:checked").get().length == 1);
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
		if(inherit !== undefined) 
		{
			if(inherit)
			{
				this.inherit = true;
				this.inherit_members.show();
			}
			else
			{
				this.inherit = false;
				this.inherit_members.hide();
			}

		}
		else
		{
			inherit = !this.inherit;
			if(inherit)
			{
				this.inherit = true;
				this.inherit_members.show('blind');
				this.dialog.find("#inherit-permissions").attr('checked',true);
			}
			else
			{
				this.inherit = false;
				this.inherit_members.hide('blind');
				this.dialog.find("#inherit-permissions").attr('checked',false);
			}
			dj.remote('djity.project.save_inherit_permissions',
				{
					js_target:'dj.widgets.manage_users',
					inherit:this.inherit,
				});
	    }
	},

	forbid_toggle : function(forbid)
	{
		if(forbid === undefined) { forbid = !this.forbid}
		else{ if(forbid == this.forbid){return}}
		if(forbid)
		{
			this.forbid = true;

		}
		else
		{
			this.forbid = false;
		}
		dj.remote('djity.project.save_forbid_subscriptions',
			{
				js_target:'dj.widgets.manage_users',
				forbid:this.forbid,
			});

	},

	close : function (awaiting_members)
	{
		if( awaiting_members !== undefined)
		{
			if(awaiting_members > 0)
			{
				this.element.addClass('ui-state-highlight');
				this.element.button('option','label',gettext('Manage users') + ' (' + awaiting_members + ' ' + gettext('awaiting members') + ')' );
			}
			else
			{
				this.element.removeClass('ui-state-highlight');
				this.element.button('option','label',gettext('Manage users'));
			}
		}
		this.dialog.dialog('close');

	}
	


};

