# DEPLOY

## 公网地址
http://8.153.173.192:8787

服务器：阿里云 ECS cn-shanghai，目录 /opt/arb-radar-web。
systemd 已绑定 HOST=0.0.0.0 PORT=8787。

## 访问口令
与本机 data/keys.json 的 dashToken 相同。
服务器副本：/opt/arb-radar-web/data/keys.json（权限 600）。
不要把 SSH 密码或完整 API key 写进本文件。

## systemd
sudo systemctl status arb-radar
sudo systemctl restart arb-radar
sudo systemctl stop arb-radar
sudo journalctl -u arb-radar -f
单元文件：/etc/systemd/system/arb-radar.service
- WorkingDirectory=/opt/arb-radar-web
- Environment=HOST=0.0.0.0
- Environment=PORT=8787
- ExecStart=/usr/bin/node src/server.js
- Restart=always

## 安全组（必做，否则外网不通）
本机防火墙 ufw 已放行 8787/tcp（ufw 当前未启用）。
阿里云控制台安全组入方向需要放行 TCP 8787（或 80 若你自己反代）。

部署实测（2026-08-17 20:35 CST）：
- 服务器本机 curl http://127.0.0.1:8787/ 返回 HTTP 200，systemd active (running)。
- 从部署机 curl -m 10 http://8.153.173.192:8787/ 超时。
- 结论：服务已起来，外网被安全组挡住。放行 TCP 8787 后再访问公网 URL。

## 更新代码
同步 src/ public/ package.json 到 /opt/arb-radar-web 后：systemctl restart arb-radar
