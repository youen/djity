. ${WORKSPACE}/tools/jenkins_virtualenv.sh

py.test --junitxml=${WORKSPACE}/unit.xml
echo "py.test completed"

