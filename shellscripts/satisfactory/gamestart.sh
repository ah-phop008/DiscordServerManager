echo "[LOG] ================ START gamestart.sh ================"

### Settings
# Directory name under startapps/common/, commonly game title named.
DIR=SatisfactoryDedicatedServer
# runner filename
RUNNER=FactoryServer.sh
# flg to do auto update if needed
AUTOUPDATE=true
# [Optional] Steam game id to specify its source, use only if AUTOUPDATE=true
GAMEID="1690800"

###

LOGROOT=/tmp
LOGFILE_PREFIX=gameserver_
LOGPATH=$LOGROOT/$LOGFILE_PREFIX$DIR.txt

# Update if needed
cd /home/steam
UPDATE_SH="./gameupdate.sh"
if $AUTOUPDATE; then
    if [ -f "$UPDATE_SH" ]; then
        echo "[LOG] Run gameupdate.sh"
        $UPDATE_SH "$DIR" "$GAMEID"
    else
        echo "[LOG] gameupdate.sh dont exist, skip it"
    fi
else
    echo "[LOG] auto update is disabled"
fi

# RUN!!!
cd /home/steam/Steam/steamapps/common
echo "[LOG] Start running $(pwd)/$DIR/$RUNNER"
./$DIR/$RUNNER > $LOGPATH 2>&1
# MEMO: Not use async command since this will be executed from systemd with Restart=always

echo "[LOG] ================ END gamestart.sh ================"
