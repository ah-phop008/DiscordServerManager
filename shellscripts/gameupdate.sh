echo "[LOG] ================ START gameupdate.sh ================"

if [ $# -eq 2 ]; then
    DIR=$1
    GAMEID=$2
else
    echo "must 2 args, DIR and GAMEID"
    exit 0
fi


STEAMCMD="/home/steam/Steam/steamcmd.sh"

cd /home/steam/Steam/steamapps/common
echo "# Environment Check"
date

# Retrieve the current Build ID
OLD_Build=`$STEAMCMD +login anonymous +app_status $GAMEID +quit | grep -e "BuildID" | awk '{print $8}'`
echo "Current BuildID: $OLD_Build"

# Attempt to fetch the New Build ID using curl
query=.data[\"$GAMEID\"].depots.branches.public.buildid
NEW_Build=$(curl -s https://api.steamcmd.net/v1/info/$GAMEID | jq -r "$query")

# Fallback to SteamCMD method if curl fails to retrieve data
if [ -z "$NEW_Build" ] || [ "$NEW_Build" = "null" ]; then
    echo "Failed to fetch New BuildID with curl. Resorting to SteamCMD."
    $STEAMCMD $GAMEID+login anonymous +app_update $GAMEID validate +quit > /dev/null
    NEW_Build=`$STEAMCMD $GAMEID+login anonymous +app_status $GAMEID +quit | grep -e "BuildID" | awk '{print $8}'`
fi

echo "Fetched New BuildID: $NEW_Build"

# Update the server if the Build IDs do not match
if [ "$OLD_Build" = "$NEW_Build" ]; then
    echo "No update required. Build numbers are identical."
else
    echo "# Updating the game server..."
    $STEAMCMD $GAMEID+login anonymous +app_update $GAMEID validate +quit > /dev/null
    echo "Game server updated successfully to BuildID: $NEW_Build"
fi

echo "[LOG] ================ END gameupdate.sh ================"