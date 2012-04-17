. ${WORKSPACE}/tools/jenkins_virtualenv.sh

ROOTDIR=${WORKSPACE}/../

echo "change directory to ${ROOTDIR}"
cd ${ROOTDIR}

ROOTDIR=`pwd`

echo "create new project"
echo "djity-admin.py create_project ${ROOTDIR}/${JOB_NAME} "
djity-admin.py create_project ${ROOTDIR}/${JOB_NAME} << EOF
Djity
admin
admin@djity.net
y
y
EOF


