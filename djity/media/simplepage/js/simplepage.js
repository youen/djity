dj.functions.save_simple_page = function(html) {
	/*
	 * save change for a simple
	 *
	 */					
	dj.remote('djity.simplepage.save_simple_page',
			{
			'js_target':document,
			'html':html,
			}
	);	
}
