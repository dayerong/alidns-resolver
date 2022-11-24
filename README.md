# alidns-resolver
动态阿里云域名解析

```
适用于拨号宽带无固定外网IP的使用场景下动态解析DNS，类似花生壳DDNS
```

- 配置文件：conf.yaml

```
logging:
  logformat: "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
  file: ./logs/app.log
  datefmt: "%Y-%m-%d %H:%M:%S"
accesskey:
  id: 111111       #阿里云账号accesskey id
  secret: 2222222  #阿里云账号accesskey secret
domain:
  # 此域名需在阿里云DNS解析管理中已存在
  - docs.yao.com
  - www.yao.com
  - less.yao.com
job:
  trigger_type: interval
  name: DNS动态解析
  schedule_time:
    minutes: 60   # 设置多少分钟去检查更新

```

- 日志文件：app.log
```
root@749eea654e60:/app/logs# cat app.log
2022-11-24 15:35:54 - INFO - 已更新 - docs.yao.com        当前解析的IP为：218.81.23.214  当前出口IP为：106.15.175.92
{'body': {'RequestId': '50857CC4-BD8A-56F6-9BE4-1E82AE4FC943', 'RecordId': '797664933924548608'}, 'headers': {'date': 'Thu, 24 Nov 2022 07:35:54 GMT', 'content-type': 'application/json;charset=utf-8', 'content-length': '84', 'connection': 'keep-alive', 'access-control-allow-origin': '*', 'x-acs-request-id': '50857CC4-BD8A-56F6-9BE4-1E82AE4FC943', 'x-acs-trace-id': 'e914b044770a4a4fa36a2ec95ab6336e'}, 'statusCode': 200}
2022-11-24 15:35:55 - INFO - 已更新 - www.yao.com 当前解析的IP为：218.81.23.214  当前出口IP为：106.15.175.92
{'body': {'RequestId': '33BBEFD2-3444-548E-BF9F-27292289C9A6', 'RecordId': '797617005325379584'}, 'headers': {'date': 'Thu, 24 Nov 2022 07:35:55 GMT', 'content-type': 'application/json;charset=utf-8', 'content-length': '84', 'connection': 'keep-alive', 'access-control-allow-origin': '*', 'x-acs-request-id': '33BBEFD2-3444-548E-BF9F-27292289C9A6', 'x-acs-trace-id': 'a2f6b526e780aa374655110dde939284'}, 'statusCode': 200}
2022-11-24 15:35:55 - INFO - 已更新 - less.yao.com        当前解析的IP为：218.81.23.214  当前出口IP为：106.15.175.92
{'body': {'RequestId': '82F43C3C-602F-597F-A1D4-A97867CA956F', 'RecordId': '797664968368094208'}, 'headers': {'date': 'Thu, 24 Nov 2022 07:35:55 GMT', 'content-type': 'application/json;charset=utf-8', 'content-length': '84', 'connection': 'keep-alive', 'access-control-allow-origin': '*', 'x-acs-request-id': '82F43C3C-602F-597F-A1D4-A97867CA956F', 'x-acs-trace-id': 'c0abf5b4d13dcd2937ba6bec1ce19b62'}, 'statusCode': 200}
2022-11-24 15:36:54 - INFO - 未更新 - docs.yao.com        当前解析的IP为：106.15.175.92   当前出口IP为：106.15.175.92
2022-11-24 15:36:54 - INFO - 未更新 - www.yao.com 当前解析的IP为：106.15.175.92   当前出口IP为：106.15.175.92
2022-11-24 15:36:55 - INFO - 未更新 - less.yao.com        当前解析的IP为：106.15.175.92   当前出口IP为：106.15.175.92
root@749eea654e60:/app/logs#
```