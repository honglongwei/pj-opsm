#coding: utf-8

import datetime
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from xadmin.util import User
from xadmin.views.base import filter_hook, ModelAdminView, csrf_protect_m
from xadmin.plugins.actions import BaseActionView
from models import RecordLogMsg


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
    extra = 1
    style = 'accordion'


class RecordLogMsgAdmin(object):
    #def save_models(self):
    #    obj = self.new_obj
    #    request = self.request
    #    obj.responser = User.objects.get(username=request.user).first_name
    #    obj.save()

    fields = ('logmsg')
    list_display = ('id', 'logmsg')
    search_fields = ['id', 'recordtime', 'responser', 'logmsg']
    #list_display_links = ('id')
    ordering = ["-id"]
    refresh_times = (5, 10, 30)


xadmin.site.register(RecordLogMsg, RecordLogMsgAdmin)
