class BaseOwnAdmin(object):
    """
        1. 用来自动补充文章、分类、标签、友链、侧边栏这些Model的owner字段
        2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    # def get_queryset(self, request):
    #     qs = super(BaseOwnAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # xadmin里面为 get_list_queryset(self)
    def get_list_queryset(self):
        qs = super().get_list_queryset()
        return qs.filter(owner=self.request.user)

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(BaseOwnAdmin, self).save_model(request, obj, form, change)

    # save_model变成了save_models(self)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()