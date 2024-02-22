# Setup steam cmd
* sudo useradd -m steam
* sudo passwd -d steam
* `sudo passwd steam`
* `MEMO: type password`
* sudo visudo
* `see file content and write below command under **root ALL= ...**`
* steam    ALL=(ALL:ALL) ALL
----
* sudo -u steam -s
* cd ~
----
* sudo apt update
* sudo apt-get install lib32gcc-s1
* sudo -iu steam
* mkdir ~/Steam && cd ~/Steam
* curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -

# Do initial setup
* ~/Steam/steamcmd.sh
* `setup alias after initial setup`
* echo "alias steamcmd='~/Steam/steamcmd.sh'" >> ~/.bashrc

# Setup Palworld
* sudo -u steam -s
----
* `steamcmd +login anonymous +app_update 2394010 validate +quit`
* ~/Steam/steamcmd.sh +login anonymous +app_update 2394010 validate +quit
----
* cd ~/Steam/steamapps/common/PalServer
----
* `Start Palworld Once`
* ./PalServer.sh
* `Ctrl + c to kill`
----
* mkdir -p ~/.steam/sdk64/
* ~/Steam/steamcmd.sh +login anonymous +app_update 1007 +quit
* cp ~/Steam/steamapps/common/Steamworks\ SDK\ Redist/linux64/steamclient.so ~/.steam/sdk64/
----
* `起動確認`
* ./PalServer.sh

# 自動起動設定
* `scp (Windows Command Prompt)`
* set X={} # {}内に対象のファイルパス
* scp %X% ubuntu@game:/tmp/
----
* `# after scp (Linux)`
* sudo chown steam:steam /tmp/gamestart.sh
* sudo chmod 755 /tmp/gamestart.sh
* sudo mv /tmp/gamestart.sh /home/steam/gamestart.sh
----
* sudo chown steam:steam /tmp/game_dedicatedsrv.service
* sudo chmod 755 /tmp/game_dedicatedsrv.service
* sudo mv /tmp/game_dedicatedsrv.service /etc/systemd/system/game_dedicatedsrv.service
* `デーモンの再起動`
* sudo systemctl daemon-reload
* sudo systemctl start game_dedicatedsrv.service
* sudo systemctl status game_dedicatedsrv.service
----
* sudo systemctl enable game_dedicatedsrv.service
