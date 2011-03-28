

function init_right_tabs() {
	/*
	 * Function called when document is loaded
	 * Create a scrolling menu for the right navigation tabs
	 *
	 */
		
	if (dj_context.perm.manage){
		$("#right_tabs_list").disableSelection();
		$('#right_tabs_list').sortable({

			placeholder: 'dj-sorting-tab ui-state-highlight dj-mini-button',
			update: function(event, ui) { 
				Dajaxice.djity.project.save_tab_order(
					'Dajax.process',{
						'project_name':dj_context.project_name,
						'array':$('#right_tabs_list').sortable('toArray')
				
					});	
			}
		});
	}

	/*
	 * Create delete tab dialog 
	 */

	$('#' + dj_context.module_name + '-delete')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					Dajaxice.djity.project.delete_tab(
						'Dajax.process',{
						'project_name':dj_context.project_name,
						'module_name':dj_context.module_name,
				
					});	
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind delete tab dialog
	$('#' + dj_context.module_name + ' .ui-icon-close')
		.click(function(){
				$('#' + dj_context.module_name + '-delete').dialog('open');
				return false;
		});

	/*
	 * Create a edit dialog 
	 */

	$('#' + dj_context.module_name + '-edit')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			open: function(event,ui){ 
				$('#' + dj_context.module_name + '-title').val(
					$('#' + dj_context.module_name ).find('a')[0].textContent
					);
				
			},
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					$('#' + dj_context.module_name ).find('a')[0].textContent = $('#' + dj_context.module_name + '-title').val();
					Dajaxice.djity.project.edit_tab(
						'Dajax.process',{
						'project_name':dj_context.project_name,
						'module_name':dj_context.module_name,
						'LANGUAGE_CODE':dj_context.LANGUAGE_CODE,
						'label': $('#' + dj_context.module_name + '-title').val(),
						'status': $('#' + dj_context.module_name + '-status').val(),
					});	
					
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind edit name dialog
	$('#' + dj_context.module_name + ' .ui-icon-wrench')
		.click(function(){
				$('#' + dj_context.module_name + '-edit').dialog('open');
				return false;
		});


	
	/*
	 *  Bind add tab button
	 */
	$('#create_tab_button')
		.click(function(){
				$('#create_tab_dialog').dialog('open');
				return false;
		})
		.button({
			icons: {
				primary: 'ui-icon-circle-plus'
			},
			text : false,
		})
	
	$('#create_tab_dialog')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			open: function(event,ui){
				Dajaxice.djity.project.get_module(
					'Dajax.process',{
					'project_name' : dj_context.project_name,
					}
				
				);
				$("#module_list").change(function () {
						$('#new_tab_name')
							.val($("#module_list option:selected").text())
							.select();	
					});
			},
			
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					Dajaxice.djity.project.add_module(
						'Dajax.process',{
							'project_name':dj_context.project_name,
							'tab_name':$('#new_tab_name').val(),
							'module_type':$("#module_list option:selected").val(),
						}
					);		
				},
				Cancel: function() {
					$(this).dialog('close');
					}
			}
			});
	$('#right_tabs').removeClass('ui-helper-hidden');
};
