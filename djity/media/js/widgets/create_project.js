dj.widgets.create_project = 
{
		/*
		 *  Djity user's manager
		 */



	init : function()
	{
	   	//inherit permissions

		//init button
		this.element = $('#create_project_button')
			.button(
			{
				icons: {primary: 'ui-icon-circle-plus'},
				text: false
			})
			.addClass('ui-corner-tl ui-corner-tr')
			.click(function()
			{
				dj.widgets.create_project.open();
				return false;
			});


		//init dialog
		this.dialog = $("#create_project_dialog")
		.dialog(
		{
			autoOpen:false,
			modal: true,
			show:'blind',
			resizable:false,
			buttons : 
			{
				OK : function()
				{
					dj.widgets.create_project.validate();
				},
		
				Cancel : function()
				{
					$(this).dialog('close');
				}
			},
		});


	},

	validate : function ()
	{
		dj.remote('djity.project.create_project',
						{	
							'js_target':document,
							'name': $('#new_project_name').val()}
					);	

		
	},
	open : function ()
	{
		this.dialog.dialog('open');

	},

	close : function ()
	{
		this.dialog.dialog('close');

	}
	


};

