function simple_page_content_callback(id,html) {
	/*
	 * save change for a simple
	 *
	 */					
	Dajaxice.djity.core.simplepage.save_simple_page(
			'Dajax.process',{
			'project_name':project_name,
			'LANGUAGE_CODE':lang_version,
			'module_name':module_name,
			'div_id':id,
			'html':html,
			}
	);	
}
