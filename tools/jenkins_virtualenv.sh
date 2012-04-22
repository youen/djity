export PATH=${WORKSPACE}/.env/bin:$PATH

if [ -d "${WORKSPACE}/.env" ]; then
	echo "**> Virtualenv exists"
else
	echo "**> Creating virtualenv"
	virtualenv --system-site-packages ${WORKSPACE}/.env
	echo "**> Creating PYTHON_EGG_CACHE"
	mkdir ${WORKSPACE}/.env/PYTHON_EGG_CACHE
fi




