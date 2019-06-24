# -*- coding: utf-8 -*-

import sys
import json

import blueprintDesc
import element
import action
import hypnosConfig
import outputDesc
import resource

def createDesignMap():
    designMap = {
        'elements': [],
        'actions': [],
        'blueprintDesc': {},
        "outputDesc": {},
        "resource": {}
    }
    return designMap

def main():
    print(sys._getframe().f_code.co_name)
    designMap = createDesignMap()
    designMap['elements'].append(element.create('name','type','source','value',))
    designMap['actions'].append(action.create('name','element',1000,4000,'1,1,0,0','0,0,1,1'))
    print(json.dumps(designMap, ensure_ascii=False, sort_keys=True, indent=4))

if __name__=="__main__":
    print("Hi, this is IVF blueprint program")
    main()
