#_*_ coding:utf-8 _*_

from django.db import models


class RecordLogMsg(models.Model):  
   # recordtime= models.DateTimeField(u"时间", auto_now_add=True)
   # responser = models.CharField(u"成员", max_length=255)  
    logmsg = models.TextField(u"日志", ) 

    def __unicode__(self):  
        return self.logmsg
          
    class Meta:  
        db_table = "recordlogmsg"     
        verbose_name = u"日志管理"
        verbose_name_plural = verbose_name 
