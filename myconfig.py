# custom parameters
out_dir = ".."
group_id = "com.demo.serve"
name = "demo-serve"
mysql = {
    "url": "127.0.0.1",
    "database": "myblog",
    "port": "3306",
    "username": "root",
    "password": "123456",
    # tables need to generate api
    # cms: content
    # ums：user
    "tableNames": ["ums_emp"],
    # data type of id which is usually the first column
    "idTypes": ["Integer"]
}

# don't care
temp_group_id = "com.macro.mall"
JAVA_MAIN = ["src", "main", "java"]
template = "mytemplate"
run = True
