# pj-opsm
自动发现物理机设备
```python
class TaskMsgAdmin(object):
    icon = 'fa fa-cog fa-spin fa-1x'
    fields = ('taskName', 'ipmiStart', 'ipmiEnd', 'ipmiUser', 'ipmiPwd')
    fieldsets = [
        ('adadf', {'fields': ['taskState']}),
        ('Date information', {'fields': ['taskTime', 'taskCost']}),
    ]

    form_layout = (
            Fieldset(u'',
                     Row('taskName'),
                     css_class = 'unsort no_title'
               ),
            Fieldset(u'',
                     Row('ipmiStart', 'ipmiEnd'),
                     Row('ipmiUser', 'ipmiPwd'),
                     css_class = 'unsort no_title'

               )
         )


    list_display = ('taskTime', 'taskName', 'ipmiStart', 'ipmiEnd', 'taskState', 'taskCost')
    search_fields = ['id', 'taskName', 'ipmiStart', 'ipmiEnd', 'taskState', 'taskTime']
    list_display_links = ( 'taskName')
    actions = [AutoDiscvAction ]
    ordering = ["-id"]
    refresh_times = (5, 10, 30)
    model_icon =  'fa fa-cogs'
    list_per_page = 5
   # user_owned_objects_field = 'taskName'
    #user_can_access_owned_objects_only = True

```
