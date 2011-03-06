function simple_page_content_callback(id,html) {
	/*
	 * save change for a simple
	 *
	 */					
	Dajaxice.djity.simplepage.save_simple_page(
			'Dajax.process',{
			'project_name':project_name,
			'LANGUAGE_CODE':context.LANGUAGE_CODE,
			'module_name':module_name,
			'div_id':id,
			'html':html,
			}
	);	
}
