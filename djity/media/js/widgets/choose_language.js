
function choose_language_button(){
	$("#choose_language_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
	});

	$("#choose_language_dialog a")
	.each(function(i,head){
			$(head).button({
				icons:{
					primary:'dj-icon-' + $(head).attr('id').substring (5,7)
				}
				
			});
	});
		
	$("#choose_language_button")
		.button({
			icons: {
				primary: 'dj-icon-'+dj.LANGUAGE_CODE
			},
			text: false
		})
		.click(function(){
			$('#choose_language_dialog').dialog('open');
			return false;
		});
};
