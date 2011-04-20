function project_manage_buttons () {

		dj.widgets.create_project.init();

		dj.widgets.manage_users.init();
	
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
