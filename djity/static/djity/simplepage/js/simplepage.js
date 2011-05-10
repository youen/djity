dj.functions.save_simple_page = function(html,id,lang) {
	/*
	 * save change for a simple
	 *
	 */					
	dj.remote('djity.simplepage.save_simple_page',
			{
			'LANGUAGE_CODE':lang,
			'js_target':document,
			'html':html,
			}
	);	
}
