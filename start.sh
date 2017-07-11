#!/bin/bash
echo "--------------sdt build---------------------"
pwd
echo "--------------create virtualenv-----------------"
rm -rf log
mkdir log
rm -fR .pyenv
virtualenv .pyenv
echo "--------------pip install requirements----------"
.pyenv/bin/pip install -r requirements.txt

PYTHON='.pyenv/bin/python'
echo "PYTHON: ", ${PYTHON}
SUPERVISOR='.pyenv/bin/supervisord'
echo "SUPERVISOR: ", ${SUPERVIOSR}

# 生成supervisor配置文件
${PYTHON} build.pyc --env=pro
${SUPERVISOR} -c confs/supervisor.conf
echo "--------------sdt installed------------------"