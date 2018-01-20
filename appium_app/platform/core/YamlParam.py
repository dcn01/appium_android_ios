from ThinkCore.TYaml import *

__author__ = 'banketree@qq.com'

class YamlParam:
    case = None
    param = None
    tyaml = None
    yamlPath = ""

    # 脚本+ 脚本参数
    def __init__(self, yamlPath, yamlParam=None):
        self.tyaml = TYaml()
        self.yamlPath = yamlPath;
        try:
            self.case = self.tyaml.getYam(yamlPath)
            self.param = yamlParam
        except Exception as e:
            print(e)

    def __del__(self):
        if (self.tyaml != None):
            del self.tyaml;


if __name__ == '__main__':
    pass
