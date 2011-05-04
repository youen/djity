dj.functions.project_subscribe_button = function (){
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
	switch(dj.context.role){
		// Awaiting
		case 1:
			button_label = "Cancel subscription";
			break;
		// Anonymous
		case 0:
			button_label = "Subscribe";
			break;
		default:
			button_label = "Unsubscribe";
	}
		
	$("#project_subscribe_button")
		.button({
			disabled:(dj.role=='awaiting'),
			icons: {
				primary:'ui-icon-person'
			},
			text:false,
			label:button_label,
		});
	
	if(dj.context.user == "AnonymousUser"){
		$("#project_subscribe_button")
			.click(function(){
					$('#project_subscribe_dialog').dialog('open');
					return false;
			});
	}
	else{
		$("#project_subscribe_button")
			.click(function()
			{
					dj.remote('djity.project.project_subscribe',{js_target:Document});
			});
	}
	$('#project_buttons').removeClass('ui-helper-hidden');
};


