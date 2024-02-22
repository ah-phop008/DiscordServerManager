# Setup steam cmd
```bash {iscopy=true}
sudo useradd -m steam
```
```bash {iscopy=true}
sudo passwd -d steam
```
* `sudo passwd steam`
* `MEMO: type password`
```bash {iscopy=true}
sudo visudo
```
* see file content and write below command under root ALL= ...
```bash {iscopy=true}
steam    ALL=(ALL:ALL) ALL
```
----
```bash {iscopy=true}
sudo -u steam -s
```
```bash {iscopy=true}
cd ~
```
----
```bash {iscopy=true}
sudo apt update
```
```bash {iscopy=true}
sudo apt-get install lib32gcc-s1
```
```bash {iscopy=true}
sudo -iu steam
```
```bash {iscopy=true}
mkdir ~/Steam && cd ~/Steam
```
```bash {iscopy=true}
curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
```

# Do initial setup
```bash {iscopy=true}
~/Steam/steamcmd.sh
```
* `setup alias after initial setup`
```bash {iscopy=true}
echo "alias steamcmd='~/Steam/steamcmd.sh'" >> ~/.bashrc
```

# Setup Palworld
```bash {iscopy=true}
sudo -u steam -s
```
----
* `steamcmd +login anonymous +app_update 2394010 validate +quit`
```bash {iscopy=true}
~/Steam/steamcmd.sh +login anonymous +app_update 2394010 validate +quit
```
----
```bash {iscopy=true}
cd ~/Steam/steamapps/common/PalServer
```
----
* `Start Palworld Once`
```bash {iscopy=true}
./PalServer.sh
```
* `Ctrl + c to kill`
----
```bash {iscopy=true}
mkdir -p ~/.steam/sdk64/
```
```bash {iscopy=true}
~/Steam/steamcmd.sh +login anonymous +app_update 1007 +quit
```
```bash {iscopy=true}
cp ~/Steam/steamapps/common/Steamworks\ SDK\ Redist/linux64/steamclient.so ~/.steam/sdk64/
```
----
* `起動確認`
```bash {iscopy=true}
./PalServer.sh
```

# 自動起動設定
* `scp (Windows Command Prompt)`
```bash {iscopy=true}
set X={} # {}内に対象のファイルパス
```
```bash {iscopy=true}
scp %X% ubuntu@game:/tmp/
```
----
* `# after scp (Linux)`
```bash {iscopy=true}
sudo chown steam:steam /tmp/gamestart.sh
```
```bash {iscopy=true}
sudo chmod 755 /tmp/gamestart.sh
```
```bash {iscopy=true}
sudo mv /tmp/gamestart.sh /home/steam/gamestart.sh
```
----
```bash {iscopy=true}
sudo chown steam:steam /tmp/game_dedicatedsrv.service
```
```bash {iscopy=true}
sudo chmod 755 /tmp/game_dedicatedsrv.service
```
```bash {iscopy=true}
sudo mv /tmp/game_dedicatedsrv.service /etc/systemd/system/game_dedicatedsrv.service
```
* `デーモンの再起動`
```bash {iscopy=true}
sudo systemctl daemon-reload
```
```bash {iscopy=true}
sudo systemctl start game_dedicatedsrv.service
```
```bash {iscopy=true}
sudo systemctl status game_dedicatedsrv.service
```
----
```bash {iscopy=true}
sudo systemctl enable game_dedicatedsrv.service
```
