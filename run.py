import numpy as np
import pandas as pd
from os import system as cmd
from os import remove as rm
from os import walk as osw
from pathlib import Path
import shutil
from myconfig import *


def change_package(filename):
    text = np.loadtxt(filename, dtype="str",
                      encoding="utf-8", delimiter="xxxxxxx")
    text = pd.Series(text)
    text = text.str.replace(temp_group_id, group_id, regex=False)
    np.savetxt(filename, text.values, fmt="%s", encoding="utf-8")


def split_table_name(full_table_name):
    table_type = full_table_name.split("_")[0]
    table_name = full_table_name.split("_")[1:]
    return (table_type, table_type[0].upper()+table_type[1:], table_name[0]+"".join([name[0].upper()+name[1:] for name in table_name[1:]]), "".join([name[0].upper()+name[1:] for name in table_name]))


template_dir = Path(template)
sub_dirs = group_id.split(".")
temp_sub_dirs = temp_group_id.split(".")
out_dir = Path(out_dir)

out_dir.joinpath(name).mkdir(exist_ok=True)
out_dir.joinpath(name, "src").mkdir(exist_ok=True)
for type in ("main", "test"):
    out_dir.joinpath(name, "src", type).mkdir(exist_ok=True)
    out_dir.joinpath(name, "src", type, "java").mkdir(exist_ok=True)
    for i in range(len(sub_dirs)):
        out_dir.joinpath(name, "src", type, "java", *
                         sub_dirs[:i], sub_dirs[i]).mkdir(exist_ok=True)
    out_dir.joinpath(name, "src", type, "java", *
                     sub_dirs, "tiny").mkdir(exist_ok=True)
# generate model and mapper
# pom.xml
pom_xml = np.loadtxt(str(template_dir.joinpath("pom.xml")),
                     dtype="str", encoding="utf-8", delimiter="xxxxxxx")
pom_xml = pd.Series(pom_xml)
pom_xml = pom_xml.str.replace(temp_group_id, group_id, regex=False)
pom_xml = pom_xml.str.replace("mytemplate", name, regex=False)
np.savetxt(str(out_dir.joinpath(name, "pom.xml")),
           pom_xml.values, fmt="%s", encoding="utf-8")
cmd("cd %s && mvn dependency:tree" % (str(out_dir.joinpath(name))))
# generator properties
out_dir.joinpath(name, "src", "main", "resources").mkdir(exist_ok=True)
for filename in ["generator.properties", "application.yml"]:
    property = np.loadtxt(str(template_dir.joinpath(
        "src", "main", "resources", filename)), dtype="str", encoding="utf-8", delimiter="xxxxxxx")
    property = pd.Series(property)
    property = property.str.replace("localhost", mysql["url"], regex=False)
    property = property.str.replace("3306", mysql["port"], regex=False)
    property = property.str.replace("mall", mysql["database"], regex=False)
    property = property.str.replace("root", mysql["username"], regex=False)
    property = property.str.replace("123456", mysql["password"], regex=False)
    np.savetxt(str(out_dir.joinpath(name,  "src", "main", "resources",
               filename)), property.values, fmt="%s", encoding="utf-8")
# generatorConfig.xml
generator_config = np.loadtxt(str(template_dir.joinpath(
    "src", "main", "resources", "generatorConfig.xml")), dtype="str", encoding="utf-8", delimiter="xxxxxxx")
generator_config = "\n".join(generator_config)
generator_config = generator_config.replace(temp_group_id, group_id)
generator_config = generator_config.replace("mytemplate", name)

tables = [
    '        <table tableName="%s">\n' % tn +
    '            <generatedKey column="id" sqlStatement="MySql" identity="true"/>\n' +
    '        </table>'
    for tn in mysql["tableNames"]
]
default_table = \
    '        <table tableName="pms_brand">\n' +\
    '            <generatedKey column="id" sqlStatement="MySql" identity="true"/>\n' +\
    '        </table>'
generator_config = generator_config.replace(default_table, "\n".join(tables))
np.savetxt(str(out_dir.joinpath(name,  "src", "main", "resources", "generatorConfig.xml")),
           generator_config.split("\n"), fmt="%s", encoding="utf-8")
# mybatis generator
out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs,
                 "tiny", "mbg").mkdir(exist_ok=True)
shutil.copy(str(template_dir.joinpath(*JAVA_MAIN, *temp_sub_dirs, "tiny", "mbg",
            "CommentGenerator.java")), str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", "mbg")))
shutil.copy(str(template_dir.joinpath(*JAVA_MAIN, *temp_sub_dirs, "tiny", "mbg",
            "Generator.java")), str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", "mbg")))
change_package(str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs,
               "tiny", "mbg", "CommentGenerator.java")))
change_package(str(out_dir.joinpath(name, *JAVA_MAIN, *
               sub_dirs, "tiny", "mbg", "Generator.java")))
if out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", "MyApp.java").is_file():
    rm(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", "MyApp.java"))
cmd("cd %s && mvn package" % (str(out_dir.joinpath(name))))
cmd("cd %s && java -jar target/%s-0.0.1-SNAPSHOT.jar" %
    (str(out_dir.joinpath(name)), name))
rm(str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs,
   "tiny", "mbg", "CommentGenerator.java")))
rm(str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", "mbg", "Generator.java")))
# generate myservice and mycontroller
out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny",
                 "service").mkdir(exist_ok=True)
out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny",
                 "service", "impl").mkdir(exist_ok=True)
out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny",
                 "controller").mkdir(exist_ok=True)
for i, table_name in enumerate(mysql["tableNames"]):
    mynames = split_table_name(table_name)
    print(mynames)
    for tempfile, newfile in zip((["service", "PmsBrandService.java"], ["service", "impl", "PmsBrandServiceImpl.java"], ["controller", "PmsBrandController.java"]),
                                 (["service", "%s%sService.java" % (mynames[1], mynames[3])], ["service", "impl", "%s%sServiceImpl.java" % (mynames[1], mynames[3])], ["controller", "%s%sController.java" % (mynames[1], mynames[3])])):
        jfile = np.loadtxt(str(template_dir.joinpath(*JAVA_MAIN, *temp_sub_dirs,
                           "tiny", *tempfile)), dtype="str", encoding="utf-8", delimiter="xxxxxxx")
        jfile = pd.Series(jfile)
        jfile = jfile.str.replace(temp_group_id, group_id, regex=False)
        jfile = jfile.str.replace("Pms", mynames[1], regex=False)
        jfile = jfile.str.replace("brand", mynames[2], regex=False)
        jfile = jfile.str.replace("Brand", mynames[3], regex=False)
        jfile = jfile.str.replace("Long id", "%s id" %
                                  mysql["idTypes"][i], regex=False)
        np.savetxt(str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs,
                   "tiny", *newfile)), jfile.values, fmt="%s", encoding="utf-8")
# other files
for package in ["common", "config"]:
    out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny",
                     package).mkdir(exist_ok=True)
    proot = template_dir.joinpath(*JAVA_MAIN, *temp_sub_dirs, "tiny", package)
    for root, dirs, files in osw(str(proot)):
        root = Path(root)
        for dir in dirs:
            out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny", package,
                             root.relative_to(proot), dir).mkdir(exist_ok=True)
        for file in files:
            newfile = out_dir.joinpath(
                name, *JAVA_MAIN, *sub_dirs, "tiny", package, root.relative_to(proot), file)
            shutil.copy(str(root.joinpath(file)), str(newfile))
            change_package(newfile)
# MyApp
shutil.copy(str(template_dir.joinpath(*JAVA_MAIN, *temp_sub_dirs, "tiny",
            "MyApp.java")), str(out_dir.joinpath(name, *JAVA_MAIN, *sub_dirs, "tiny")))
change_package(out_dir.joinpath(name, *JAVA_MAIN,
               *sub_dirs, "tiny", "MyApp.java"))
# Run
if run:
    cmd("cd %s && mvn package" % (str(out_dir.joinpath(name))))
    cmd("cd %s && java -jar target/%s-0.0.1-SNAPSHOT.jar" %
        (str(out_dir.joinpath(name)), name))
print("finished.")
