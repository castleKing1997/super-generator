# custom parameters
out_dir = "."
group_id = "com.github.blog"
name = "myblog"
mysql = {
    "url": "10.254.4.24",
    "database": "myblog",
    "username": "root",
    "password": "123456",
    # tables need to generate api
    "tableNames": ["cms_article", "cms_comment", "cms_leave_message", "ums_user"],
    # data type of id which is usually the first column
    "idTypes": ["Integer", "Long", "Integer", "Integer"]
}
# don't care
temp_group_id = "com.macro.mall"
JAVA_MAIN = ["src", "main", "java"]
template = "mytemplate"
run = True
