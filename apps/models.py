#_*_ coding:utf-8 _*_

from django.db import models  


class TaskMsg(models.Model):  
    id = models.AutoField(primary_key=True)
    taskName = models.CharField(u"任务名称", max_length=255)  
    ipmiStart = models.GenericIPAddressField(u"IPMI开始地址")
    ipmiEnd = models.GenericIPAddressField(u"IPMI结束地址")
    ipmiUser = models.CharField(u"IPMI帐号", max_length=255)  
    ipmiPwd = models.CharField(u"IPMI密码", max_length=255)  
    taskState = models.CharField(u"状态", max_length=255, default=u"未开始")  
    taskTime = models.DateTimeField(u"任务时间", auto_now_add=True)
    taskCost = models.CharField(u"任务耗时", max_length=255, default='0 s')  

    def __unicode__(self):  
        return self.taskName
      
    class Meta:  
        db_table = "taskmsg"    
        verbose_name = u"任务列表"
        verbose_name_plural = verbose_name 
