# -*- coding: utf-8 -*-

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from common.read_yaml import read_config
from common.logs import Log
import requests
import time


class OperateDomainRecords(object):
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> OpenApiClient:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=read_config('accesskey')['id'],
            access_key_secret=read_config('accesskey')['secret']
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-shanghai.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_describedomainrecords_api_info() -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='DescribeDomainRecords',
            # 接口版本,
            version='2015-01-09',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def create_updatedomainrecord_api_info() -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='UpdateDomainRecord',
            # 接口版本,
            version='2015-01-09',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def updatedomainrecord_main(
            # args: List[str],
            RR, RecordId, NewIP
    ) -> None:
        # 初始化 Client，采用 AK&SK 鉴权访问的方式，此方式可能会存在泄漏风险，建议使用 STS 方式。鉴权访问方式请参考：https://help.aliyun.com/document_detail/378659.html
        # 获取 AK 链接：https://usercenter.console.aliyun.com
        client = OperateDomainRecords.create_client('accessKeyId', 'accessKeySecret')
        params = OperateDomainRecords.create_updatedomainrecord_api_info()
        # query params
        queries = {}
        queries['RecordId'] = RecordId
        queries['RR'] = RR
        # queries['RR'] = read_config('domain')['name'].split('.')[0]
        queries['Type'] = 'A'
        queries['Value'] = NewIP
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        # 复制代码运行请自行打印 API 的返回值
        # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode
        resp = client.call_api(params, request, runtime)
        return resp

    @staticmethod
    def describedomainrecord_main(
            DomainName
    ) -> None:
        client = OperateDomainRecords.create_client('accessKeyId', 'accessKeySecret')
        params = OperateDomainRecords.create_describedomainrecords_api_info()
        # query params
        queries = {}
        queries['DomainName'] = DomainName
        # queries['DomainName'] = '.'.join(read_config('domain')['name'].split('.')[1:])
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        resp = client.call_api(params, request, runtime)
        return resp['body']['DomainRecords']['Record']


def query_external_ip():
    ip = requests.get('http://ifconfig.me/ip', timeout=10).text.strip()
    return ip


def update_new_record():
    log = Log()
    domain_names = read_config('domain')

    for i in domain_names:
        # 一级域名
        domain_name = '.'.join(i.split('.')[1:])
        # 二级域名
        rr = i.split('.')[0]
        # 一级域名下的所有解析记录
        records = OperateDomainRecords.describedomainrecord_main(domain_name)
        # 匹配到的二级域名的A记录信息
        data = [(i['Value'], i['RecordId']) for i in records if i['RR'] == rr]
        record_id = data[0][1]
        ip = data[0][0]

        # 比对当前最新出口IP与解析的IP
        new_ip = query_external_ip()
        if ip == new_ip:
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{t} {rr}.{domain_name}\t当前解析的IP为：{ip}\t当前出口IP为：{new_ip}")
            log.info('未更新', f"{rr}.{domain_name}\t当前解析的IP为：{ip}\t当前出口IP为：{new_ip}")
        else:
            # 更新A记录
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{t} {rr}.{domain_name}\t解析由{ip}更新为IP{new_ip}")
            resp = OperateDomainRecords.updatedomainrecord_main(rr, record_id, new_ip)
            log.info('已更新', f"{rr}.{domain_name}\t当前解析的IP为：{ip}\t当前出口IP为：{new_ip}\n{resp}")
