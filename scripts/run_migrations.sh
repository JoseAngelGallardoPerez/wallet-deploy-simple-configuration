#!/bin/sh

PY_VER_MAJOR=$(python3 -c "import sys; print('{0[0]}'.format(sys.version_info))")
PY_VER_MINOR=$(python3 -c "import sys; print('{0[1]}'.format(sys.version_info))")

echo "Python 3 version is: ${PY_VER_MAJOR}.${PY_VER_MINOR}"

if [ "$PY_VER_MAJOR" -ne 3 ] || [ "$PY_VER_MINOR" -lt 6 ] || [ "$PY_VER_MINOR" -gt 7 ]; then
  printf "\e[31mSupported Python versions are \e[93m3.6\e[31m and \e[93m3.7\e[31m!\e[0m\n"; 1>&2
  exit 1
fi

python3 -m pip --version
if [ $? -ne 0 ]; then
  printf "\e[31mPlease install \e[93mpip module\e[31m for your Python version\e[0m\n"; 1>&2
  exit 1
fi

python3 -m pip install -r requirements.txt
python3 ./scripts/run_migrations.py