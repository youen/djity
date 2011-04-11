function simple_page_content_callback(id,html) {
	/*
	 * save change for a simple
	 *
	 */					
	dj.remote('djity.simplepage.save_simple_page',
			{
			'div_id':id,
			'html':html,
			}
	);	
}
