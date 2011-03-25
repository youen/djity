
function parent_projects() {
	$('#parent_projects a').button({
		icons:{
		    primary:'ui-icon-carat-1-e'
			}
	})
	.addClass('dj-mini-button');
};


function children_projects () {
	$('#children_projects a').button({
		icons : {
			primary : 'ui-icon-triangle-1-se'
			}
	});
};
