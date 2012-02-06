. ${WORKSPACE}/tools/jenkins_virtualenv.sh

ROOTDIR=${WORKSPACE}/../

echo "change directory to ${ROOTDIR}"
cd ${ROOTDIR}

echo "create new project"
djity-admin.py create_project ${ROOTDIR} << EOF Djity
admin
admin@djity.net
y
y
EOF


