from sqladmin import ModelView

from ...db.models import UserOrm

class UserView(ModelView, model=UserOrm):
    column_list = [
        UserOrm.id,
        UserOrm.yandex_id,
        UserOrm.login,
        UserOrm.email,
    ]

    column_details_list = [
        UserOrm.id,
        UserOrm.yandex_id,
        UserOrm.login,
        UserOrm.email,
    ]

    column_labels = {
        UserOrm.id: "User ID",
        UserOrm.yandex_id: "Yandex ID",
        UserOrm.login: "Логин",
        UserOrm.email: "Email",
    }  

    column_searchable_list = [
        UserOrm.login,
    ]

    form_excluded_columns = [
        UserOrm.audio_files,
        UserOrm.yandex_id
    ]
    
    can_delete = True
    can_create = True
    can_edit = True
    can_view_details = True

    icon = 'fa fa-user'
    name = "Пользователь"
    name_plural = "Пользователи"