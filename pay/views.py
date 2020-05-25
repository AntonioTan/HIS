from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.conf import settings
from django.urls import reverse
import logging
import traceback
from datetime import datetime
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HIS.settings")  # project_name 项目名称
django.setup()
from appoint.models import Order, Schedule
from login.models import User
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


def pay_result(request):
    return render(request, 'pay/success.html')


def pay_test(request, price, schedule_id):
    print(request.method)
    if request.method == 'POST':
        if 'user_id' not in request.COOKIES:
            return render(request, 'login/home_page_test.html')
        user_id = request.COOKIES['user_id']
        patient = User.objects.get(id=user_id)
        registration = Schedule.objects.get(id=schedule_id)
        registration.num = registration.num-1
        Order.objects.create(
            patient=patient,
            registration=registration,
            status=2,
            description=request.POST['description'],
            order_time=datetime.now()
        )
        print('Order Created')
        """
        设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
        """

        with open('pay/alipay/alipay_keys/app_private.txt', 'r') as f:
            private_key = f.readlines()[0]
        with open('pay/alipay/alipay_keys/alipay_public.txt', 'r') as f:
            ali_public_key = f.readlines()[0]
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
        alipay_client_config.app_id = '2016102100732681'
        alipay_client_config.app_private_key = private_key
        alipay_client_config.alipay_public_key = ali_public_key

        """
        得到客户端对象。
        注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
        logger参数用于打印日志，不传则不打印，建议传递。
        """
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

        """
        #    页面接口示例：alipay.trade.page.pay
        #    """
        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        model.out_trade_no = 'pay'+str(time.time()).replace('.', '')[0:16]
        # model.out_trade_no = "pay201905020000220"
        model.total_amount = price
        model.subject = "测试"
        model.body = "支付宝测试"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        settle_detail_info = SettleDetailInfo()
        settle_detail_info.amount = price
        settle_detail_info.trans_in_type = "userId"
        settle_detail_info.trans_in = "2088102180529084"
        settle_detail_infos = list()
        settle_detail_infos.append(settle_detail_info)
        settle_info = SettleInfo()
        settle_info.settle_detail_infos = settle_detail_infos
        model.settle_info = settle_info
        # sub_merchant = SubMerchant()
        # sub_merchant.merchant_id = "2088102180529084"
        # model.sub_merchant = sub_merchant
        ali_request = AlipayTradePagePayRequest(biz_model=model)
        ali_request.return_url= '127.0.0.1:8000/pay/pay_result/'
        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
        response = client.page_execute(ali_request, http_method="GET")
        print("alipay.trade.page.pay response:" + response)
        return redirect(response)

    else:
        return render(request, 'pay/index.html')




# /order/alipay
class AlipayView(LoginRequiredMixin, View):
    """支付宝支付"""
    @staticmethod
    def sign(logger=None):
        # 构造签名基础参数
        alipay_client_config = AlipayClientConfig(sandbox_debug=True)
        alipay_client_config.app_id = settings.ALIPAY_APPID
        alipay_client_config.app_private_key = settings.APP_PRIVATE_KEY
        alipay_client_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY
        client = DefaultAlipayClient(alipay_client_config, logger)
        return client

    @staticmethod
    def logger():
        """初始化日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            filemode='a', )
        logger = logging.getLogger('')
        return logger

    def post(self, request):
        # 获得支付宝客户端
        client = AlipayView.sign()
        # 构造请求参数
        model = AlipayTradePagePayModel()
        model.out_trade_no = "x2" + str(time.time())
        model.total_amount = str(1)
        model.subject = "天天生鲜订单支付"
        model.timeout_express = str(settings.ALIPAY_TIMEOUT_MINUTE) + 'm'

        pay_request = AlipayTradePagePayRequest(biz_model=model)
        url = 'http://127.0.0.1:8000' + reverse('pay:pay_result')
        pay_request.notify_url = url  # 支付后回调地址
        pay_url = client.page_execute(pay_request, http_method='GET')  # 获取支付链接
        return JsonResponse({'res': 0, 'msg': '正在支付中...', 'url': pay_url})


# /order/alipay_result
class AlipayResult(View):

    def check_pay(self, params):  # 定义检查支付结果的函数
        from alipay.aop.api.util.SignatureUtils import verify_with_rsa
        sign = params.pop('sign', None)  # 取出签名
        params.pop('sign_type')  # 取出签名类型
        params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
        message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
        # with open(settings.ALIPAY_PUBLIC_KEY_PATH, 'rb') as public_key: # 打开公钥文件
        try:
            #     status =verify_with_rsa(public_key.read().decode(),message,sign) # 验证签名并获取结果
            status = verify_with_rsa(settings.ALIPAY_PUBLIC_KEY.encode('utf-8').decode('utf-8'), message,
                                     sign)  # 验证签名并获取结果
            return status  # 返回验证结果
        except:  # 如果验证失败，返回假值。
            return False

    def post(self, request):
        """支付宝POST回应"""
        params = request.POST.dict()  # type: dict
        if self.check_pay(params):  # 调用检查支付结果的函数
            '''
                此处编写支付失败后的业务逻辑
            '''
            return HttpResponse('success')  # 返回成功信息到支付宝服务器
        else:
            '''
                此处编写支付失败后的业务逻辑
            '''
            print('支付失败!')
            return HttpResponse('')

    def get(self, request):
        """支付宝的GET回应"""
        params = request.GET.dict()  # 获取参数字典
        if self.check_pay(params):  # 调用检查支付结果的函数
            '''
                此处编写支付成功后的业务逻辑
            '''
            return HttpResponse('支付成功！')
        else:
            '''
                此处编写支付失败后的业务逻辑
            '''
            return HttpResponse('支付失败！')


from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
import time


# /order/alipay_check
class AlipayCheck(LoginRequiredMixin, View):
    """支付宝结果用户查询"""

    def post(self, request):
        """查询POST请求"""
        while True:
            # 检测订单状态
            if order.order_status > 1:
                print('支付宝内部修改成功!')
                return JsonResponse({'res': 0, 'msg': '支付成功!'})
            # 发送查询请求
            client = AlipayView.sign(AlipayView.logger())

            # 构造请求对象
            model = AlipayTradeQueryModel()
            model.out_trade_no = "x2" + str(time.time())
            req = AlipayTradeQueryRequest(biz_model=model)

            # 执行请求操作
            try:
                response_content = client.execute(req)
            except Exception as e:
                return JsonResponse({'res': -1, 'msg': e})
            if response_content:
                # 解析响应结果
                response = AlipayTradeQueryResponse()
                response.parse_response_content(response_content)
                # 响应成功的业务处理
                if response.is_success():
                    # 成功
                    if response.trade_status == 'TRADE_SUCCESS':
                        return JsonResponse({'res': 0, 'msg': '支付成功!'})
                    # 等待付款
                    elif response.trade_status == 'WAIT_BUYER_PAY':
                        time.sleep(settings.ALIPAY_TIMEOUT_SLEEP_SECS)
                        continue
                    else:
                        return JsonResponse({'res': -1, 'msg': '支付失败'})
                # 等待创建交易
                elif response.code == '40004':
                    # 创建交易超时
                    if (expire_time > settings.ALIPAY_TIMEOUT_MINUTE * 60):
                        return JsonResponse({'res': -1, 'msg': '创建交易超时'})
                    expire_time += settings.ALIPAY_TIMEOUT_SLEEP_SECS
                    time.sleep(settings.ALIPAY_TIMEOUT_SLEEP_SECS)
                    continue
                else:
                    return JsonResponse({'res': -1, 'msg': '支付失败'})