function simple_page_content_callback(id,html) {
	/*
	 * save change for a simple
	 *
	 */					
	Dajaxice.djity.simplepage.save_simple_page(
			'Dajax.process',{
			'project_name':dj_context.project_name,
			'LANGUAGE_CODE':dj_context.LANGUAGE_CODE,
			'module_name':dj_context.module_name,
			'div_id':id,
			'html':html,
			}
	);	
}
