. ${WORKSPACE}/tools/jenkins_virtualenv.sh

pylint --rcfile ${WORKSPACE}/tools/pylintrc -f parseable `find djity  -name "*.py"` > ${WORKSPACE}/pylint.txt
echo "pylint complete"

pep8  `find djity  -name "*.py"` > ${WORKSPACE}/pep8.txt
echo "pep8 complete"

java -jar ${WORKSPACE}/tools/jslint4java-2.0.1.jar --undef --maxerr 300 --report xml ${WOKSPACE}djity/static/djity/js/djity.js ${WORKSPACE}/djity/static/djity/js/widgets/*.js  > ${WORKSPACE}/jslint.xml
echo "jslint complete"

