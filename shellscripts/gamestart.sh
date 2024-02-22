echo "[LOG] ================ START gamestart.sh ================"

# Directory name under startapps/common/, commonly game title named.
DIR=PalServer
# runner filename
RUNNER=PalServer.sh

LOGROOT=/tmp
LOGFILE_PREFIX=gameserver_
LOGPATH=$LOGROOT/$LOGFILE_PREFIX$DIR.txt


cd /home/steam/Steam/steamapps/common

# RUN!!!
echo "[LOG] Start running $(pwd)/$DIR/$RUNNER"
./$DIR/$RUNNER > $LOGPATH 2>&1
# MEMO: Not use async command since this will be executed from systemd with Restart=always

echo "[LOG] ================ END gamestart.sh ================"
