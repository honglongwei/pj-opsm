#_*_ coding:utf-8 _*_

import re
import json
import datetime
from pj_opsm.celery import app
from .models import TaskMsg
from devices.models import DiscoveryMsg
from subprocess import Popen, PIPE


class IPMIAPI(object):
    def __init__(self, host, username, password, trytime=1, timeout=1):
        self.host      = host
        self.username  = username
        self.password  = password
        self.trytime   = trytime
        self.timeout   = timeout

    def power(self, action):
        try:
            cmd = ("ipmitool -I lanplus -H {ip} -U {user} -P {passwd} chassis power {action} -R {trytime} -N {timeout}".format(ip=self.host, 
                    user=self.username, passwd=self.password, trytime=self.trytime, timeout=self.timeout, action=action)
                )    
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            return {'stdout': stdout, 'stderr': stderr}
        except:
            return False
        
    def get_sn(self):
        try:
            cmd = ("ipmitool -I lanplus -H {ip} -U {user} -P {passwd} -R {trytime} -N {timeout} fru|grep 'Product Serial'".format(ip=self.host, 
                    user=self.username, passwd=self.password, trytime=self.trytime, timeout=self.timeout)
                )    
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            if stdout:
                sn_list = str(stdout).split(':')[1]
                sn_list = sn_list.replace("\n", "")
                host_sn = sn_list.replace(" ", "")
            else:
                host_sn = ''
            return {'sn': host_sn}
        except:
            return False
        
    def get_brand(self):
        try:
            cmd = ("ipmitool -I lanplus -H {ip} -U {user} -P {passwd} -R {trytime} -N {timeout} fru print 0|grep -E 'Board Mfg|Board Product'|grep -v 'Date'".format(
                    ip=self.host, user=self.username, passwd=self.password, trytime=self.trytime, timeout=self.timeout)
                )    
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            if stdout:
                brand_list = str(stdout).split('\n')
                if len(brand_list) == 2:
                    brand = brand_list[0].split(':')[1].strip()
                    version = ''
                elif len(brand_list) == 3:
                    brand = brand_list[0].split(':')[1].strip()
                    version = brand_list[1].split(':')[1].strip()
                else:
                    brand = ''
                    version = ''
                return {'brand': brand, 'version': version}
            else:
                return {'brand': '', 'version': ''}
        except:
            return False

    def get_mac(self, brand):
        try:
            brd_map = {"DELL": "delloem mac|grep 'Enabled'", }
            cmd = ("ipmitool -I lanplus -H {ip} -U {user} -P {passwd} -R {trytime} -N {timeout} {brand}".format(ip=self.host, 
                    user=self.username, passwd=self.password, trytime=self.trytime, timeout=self.timeout, brand=brd_map[brand])
                )    
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            if stdout:
                macl = str(stdout.strip()).split('\n')
                if len(macl) > 2:
                    mac_list = []
                    for ma in macl:
                        try:
                            mc = ma.split('\t')[2]
                        except:
                            mc = ''
                        mac_list.append(mc)
                else:
                     mac_list = []
            else:
                mac_list = []
            return {'mac_list': mac_list}
        except:
            return False


@app.task
def TaskAuto(ID):
    starttime = datetime.datetime.now()
    dt = TaskMsg.objects.get(id=int(ID))
    cmd = 'fping -g -a {0} {1} -t 1'.format(str(dt.ipmiStart), str(dt.ipmiEnd))
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = proc.communicate()
    ipl = stdout.strip().split("\n")
    for ip in ipl:
        ipmiapi = IPMIAPI(ip, str(dt.ipmiUser), str(dt.ipmiPwd))
        power_status = ipmiapi.power('status')
        if power_status['stdout']:
            sn = ipmiapi.get_sn()['sn']
            brand = ipmiapi.get_brand()['brand']
            vers = ipmiapi.get_brand()['version']
            mac = ipmiapi.get_mac('DELL')['mac_list']
            try:
                aa = DiscoveryMsg.objects.get(devIpmiIp=ip)
                aa.deviceSn = sn
                aa.deviceName = brand
                aa.deviceType = vers
                aa.devIpmiIp = ip
                aa.devIpmiUser = str(dt.ipmiUser)
                aa.devIpmiPass = str(dt.ipmiPwd)
                aa.devicemac = mac
                aa.save()
            except:
                bb = DiscoveryMsg(deviceSn=sn, deviceName=brand, 
                                  deviceType=vers, devIpmiIp=ip, 
                                  devIpmiUser=str(dt.ipmiUser), 
                                  devIpmiPass=str(dt.ipmiPwd), 
                                  devicemac=mac)
                bb.save()
        else:
            pass
    endtime = datetime.datetime.now()
    costtime = (endtime - starttime).seconds
    dt.taskState = u'已完成'
    dt.taskCost = '{0} s'.format(costtime)
    dt.save()
    return ipl
