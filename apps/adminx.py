#coding: utf-8

import datetime
import xadmin
import netaddr
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from xadmin.util import User
from xadmin.views.base import filter_hook, ModelAdminView, csrf_protect_m
from xadmin.plugins.actions import BaseActionView
from models import TaskMsg
from record.models import RecordLogMsg
from .tasks import TaskAuto
#from models import TaskMsg, DiscoveryMsg


class LoginSetting(object):
    title = u"OPSM | 运维部"


class BaseSetting(object):
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u'OPSM | 运维部'
    site_footer = 'iflytek.com'
    apps_label_title = {'apps': u'任务管理', 'devices': u'设备管理', 'record': u'日志审计', 'auth': u'权限管理'}
    menu_style = 'accordion'


class MaintainInline(object):
   # model = TaskMsg
    extra = 1
    style = 'accordion'


class AutoDiscvAction(BaseActionView):
    action_name = "autodisc"
    description = u'自动发现'
    icon = 'fa fa-cog fa-spin fa-1x'

    @filter_hook
    def do_action(self, queryset):
        request = self.request
        ur = User.objects.get(username=request.user).first_name
        n = queryset.count()
        tskl = []
        ipl = []
        tm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in queryset:
             tskl.append(str(i.taskName))
             TaskAuto.delay(int(i.id))
             i.taskState = u"进行中"
             i.save()
             ips = netaddr.IPRange(str(i.ipmiStart), str(i.ipmiEnd))
             for ip in ips:
                 ipl.append(str(ip))
        bb = RecordLogMsg(logmsg=u'{0}  -  {1}  -  执行任务: {2}'.format(tm, ur, ',  '.join(tskl)))
        bb.save()
        if n >= 1:
            self.message_user(u'{0} 台服务器自动发现进行中，请耐心等待几分钟!'.format(len(ipl)), 'success')


class TaskMsgAdmin(object):
    fields = ('taskName', 'ipmiStart', 'ipmiEnd', 'ipmiUser', 'ipmiPwd')
    list_display = ('taskTime', 'taskName', 'ipmiStart', 'ipmiEnd', 'taskState', 'taskCost')
    search_fields = ['id', 'taskName', 'ipmiStart', 'ipmiEnd', 'taskState', 'taskTime']
    list_display_links = ( 'taskName')
    actions = [AutoDiscvAction ]
    ordering = ["-id"]
    refresh_times = (5, 10, 30)

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(TaskMsg, TaskMsgAdmin)
