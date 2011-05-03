

function init_right_tabs() {
	/*
	 * Function called when document is loaded
	 * Create a scrolling menu for the right navigation tabs
	 *
	 */
		
	if (dj.context.perm.manage){
		$("#right_tabs_list").disableSelection();
		$('#right_tabs_list').sortable({

			placeholder: 'dj.context.sorting-tab ui-state-highlight dj.context.mini-button',
			update: function(event, ui) { 
				dj.remote('djity.project.save_tab_order',{js_target:Document,'array':$('#right_tabs_list').sortable('toArray')});
			}
		});
	}

	/*
	 * Create delete tab dialog 
	 */

	$('#' + dj.context.module_name + '-delete')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					dj.remote('djity.project.delete_tab',{js_target:Document});
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind delete tab dialog
	$('#' + dj.context.module_name + ' .ui-icon-close')
		.click(function(){
				$('#' + dj.context.module_name + '-delete').dialog('open');
				return false;
		});

	/*
	 * Create a edit dialog 
	 */

	$('#' + dj.context.module_name + '-edit')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			open: function(event,ui){ 
				$('#' + dj.context.module_name + '-title').val(
					$('#' + dj.context.module_name ).find('a')[0].textContent
					);
				
			},
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					$('#' + dj.context.module_name ).find('a')[0].textContent = $('#' + dj.context.module_name + '-title').val();
					dj.remote('djity.project.edit_tab',{
						'label':$('#' + dj.context.module_name + '-title').val(),
						'status':$('#' + dj.context.module_name + '-status').val(),
						});
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind edit name dialog
	$('#' + dj.context.module_name + ' .ui-icon-wrench')
		.click(function(){
				$('#' + dj.context.module_name + '-edit').dialog('open');
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
				dj.remote('djity.project.get_module',{js_target:Document});
				
				$("#module_list").change(function () {
						$('#new_tab_name')
							.val($("#module_list option:selected").text())
							.select();	
					});
			},
			
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					dj.remote('djity.project.add_module',{
							js_target:Document,
							'tab_name':$('#new_tab_name').val(),
							'module_type':$("#module_list option:selected").val(),
						});
				},
				Cancel: function() {
					$(this).dialog('close');
					}
			}
			});
	$('#right_tabs').removeClass('ui-helper-hidden');
};
