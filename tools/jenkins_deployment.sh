. ${WORKSPACE}/tools/jenkins_virtualenv.sh

echo "change directory to /srv/web/test.djity.net"
cd /srv/web/test.djity.net

echo "create new project"
djity-admin create_project /srv/web/test.djity.net/project


