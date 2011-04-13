function project_manage_buttons () {

		create_project_dialog();
		$('#create_project_button').button({
			icons: {
				primary: 'ui-icon-circle-plus'
			},
			text: false
		})
		.addClass('ui-corner-tl ui-corner-tr')
		.click(function(){
				$('#create_project_dialog').dialog('open');
				return false;
		});

		manage_users_dialog();
		$('#manage_users_button').button({
			icons: {
				primary: 'ui-icon-person'
			},
			text: false
		})
		.click(function(){
				dj.manage_users.role_manager('open');
				return false;
		});

		//project_style_dialog();
		$('#project_style_button').button({
			icons: {
				primary: 'ui-icon-pencil'
			},
			text: false
		})
		.addClass('ui-corner-bl ui-corner-br')
		.click(function(){
				themeroller_frame();
				return false;
				}		
		);

		$('#project_buttons a')
			.removeClass('ui-corner-all');

		$('#project_buttons').removeClass('ui-helper-hidden');
};



function create_project_dialog(){
	/*
	 * Create project creation dialog 
	 */
	$("#create_project_dialog").dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					Dajaxice.djity.project.create_project(
						'Dajax.process',{
						'project_name':dj.project_name,
						'module_name':dj.module_name,
						'path':dj.path,
						'name': $('#new_project_name').val(),
					});	
					
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});
};


function themeroller_frame(){
	if($("#themeroller_frame").attr('src') == undefined){
		var themeroller_url = $("#themeroller_url").attr('href');
		$("#themeroller_frame").attr('src',themeroller_url);
		$("#themeroller_container").draggable({handle:'#themeroller_handle'});
	};
	if($("#themeroller_container").css('display') == 'block'){
		$("#themeroller_container").css('display','none');
		$("#project_style_button").toggleClass('ui-state-highlight')
	}else{
		$("#themeroller_container").css('display','block');
		$("#project_style_button").toggleClass('ui-state-highlight')
	};
}

function project_style_dialog(){
	/*
	 * Create project style edition dialog
	 */
	$('#project_style_dialog').dialog({
		autoOpen:false,
		modal: false,
		show:'blind',
		resizable:true,
		autoResize:true,
		height:'400',
		dialogClass:'themeroller_dialog',
	});
};
