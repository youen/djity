#!/bin/sh -xe

. ${WORKSPACE}/tools/jenkins_virtualenv.sh

ROOTDIR=${WORKSPACE}/../

echo "change directory to ${ROOTDIR}"
cd ${ROOTDIR}

ROOTDIR=`pwd`

rm -rf ${ROOTDIR}/${JOB_NAME}

echo "create new project"
echo "djity-admin.py create_project ${ROOTDIR}/${JOB_NAME} "
djity-admin.py create_project ${ROOTDIR}/${JOB_NAME} << EOF
Djity
admin
admin@djity.net
admin
y
y
y
y
EOF

pidfile=${ROOTDIR}/${JOB_NAME}.pid
logfile=${ROOTDIR}/${JOB_NAME}-error.log
echo "gunicorn's pid file : $pidfile" 
if [ -e $pidfile ]; then
	pid=`cat $pidfile`
	if kill  &>1 > /dev/null $pid; then
		echo "Already running"
	fi
fi

cd  ${ROOTDIR}/${JOB_NAME} 

./manage.py collectstatic --noinput

BUILD_ID="Don't kill my unicorn!"

gunicorn_django --bind 0.0.0.0:8002 --daemon --pid $pidfile --log-file $logfile
echo "gunicorn launch!"

