#_*_ coding:utf-8 _*_

from django.db import models


POWER_TYPES = (
     (0, u'关闭'),
     (1, u'开启'),
)

OSINFO_TYPES = (
     (0, u'未安装'),
     (1, u'安装中'),
     (2, u'已安装'),
)

SSH_TYPES = (
     (0, u'可连接'),
     (1, u'不可用'),
)

IPMI_TYPES = (
     (0, u'可连接'),
     (1, u'不可用'),
)

OSHEALTH_TYPES = (
     (0, u'正常'),
     (1, u'异常'),
)

AGENT_TYPES = (
     (0, u'未安装'),
     (1, u'正在运行'),
     (2, u'已停止'),
)

class DiscoveryMsg(models.Model):  
    id = models.AutoField(primary_key=True)
    deviceSn = models.CharField(u"设备SN号", max_length=255, default=u'未知')  
    deviceName = models.CharField(u"设备名称", max_length=255, default=u'未知') 
    deviceType = models.CharField(u"设备类型", max_length=255, default=u'未知')
    devIpmiIp = models.GenericIPAddressField(u"设备ipmi地址")  
    devIpmiUser = models.CharField(u"设备ipmi帐号", max_length=255)  
    devIpmiPass = models.CharField(u"设备ipmi密码", max_length=255)  
    deviceIp = models.GenericIPAddressField(u"设备ip地址", default=u'未分配')   
    devicemac = models.CharField(u"设备mac地址", max_length=255, default=u'未知')   
    powerStatus = models.IntegerField(u"电源状态", choices=POWER_TYPES, default=1)  
    osStatus = models.IntegerField(u"操作系统状态", choices=OSINFO_TYPES, default=0)   
    sshStatus = models.IntegerField(u"连接状态", choices=SSH_TYPES, default=0)
    ipmiStatus = models.IntegerField(u"设备ipmi状态", choices=IPMI_TYPES, default=0)
    osInfoStatus = models.IntegerField(u"系统健康状态", choices=OSHEALTH_TYPES, default=0)
    agentStatus = models.IntegerField(u"Agent状态", choices=AGENT_TYPES, default=0)

    def __unicode__(self):  
        return self.deviceSn
          
    class Meta:  
        db_table = "discoverymsg"     
        verbose_name = u"设备列表"
        verbose_name_plural = verbose_name 
