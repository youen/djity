function project_subscribe_button(){
	$("#project_subscribe_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
		buttons:{
			Ok:function(){
			},
			Cancel:function(){
				$(this).dialog('close');
				return false;
			}
		}

	})

	switch(dj_context.role){
		case 'awaiting':
			button_label = "Cancel subscription";
			break;
		case 'anonymous':
			button_label = "Subscribe";
			break;
		default:
			button_label = "Unsubscribe";
	}
		
	$("#project_subscribe_button")
		.button({
			disabled:(dj_context.role=='awaiting'),
			icons: {
				primary:'ui-icon-person'
			},
			text:false,
			label:button_label,
		});
	
	if(dj_context.user == "anonymous"){
		$("#project_subscribe_button")
			.click(function(){
					$('#project_subscribe_dialog').dialog('open');
					return false;
			});
	}
	else{
		$("#project_subscribe_button")
			.click(function(){
					Dajaxice.djity.project.project_subscribe(
						'Dajax.process',{				
							'project_name':dj_context.project_name,
							'module_name':dj_context.module_name,
						});
					})
	}
	$('#project_buttons').removeClass('ui-helper-hidden');
};


