import sys
import traceback
import re
import _winreg

arch_keys = ['KEY_WOW64_64KEY', 'KEY_WOW64_32KEY']
regs = [
    'HKEY_CLASSES_ROOT',
    'HKEY_CURRENT_CONFIG',
    'HKEY_CURRENT_USER',
    'HKEY_LOCAL_MACHINE',
    'HKEY_USERS'
]

# arch_keys = ['KEY_WOW64_64KEY']
# regs = ['HKEY_CLASSES_ROOT']

outFile = open(r'C:\Users\hugo\work\registryfix.txt', 'w')

# key = _winreg.OpenKey(
#   _winreg.HKEY_CLASSES_ROOT, r'ocsmeet_auto_file\shell', 0, _winreg.KEY_ALL_ACCESS | _winreg.KEY_WOW64_64KEY
# )
#
# traverse_registry_tree(_winreg.HKEY_CLASSES_ROOT, r'jsx_auto_file', _winreg.KEY_WOW64_64KEY)


def examineValue(key, valname, keypath):
    thisVal = _winreg.QueryValueEx(key, valname)
    if re.search(r'\\programx86\\|\\program\\', valname, re.IGNORECASE) is not None:
        newVal = valname
        pattern = re.compile(r'\\program\\', re.IGNORECASE)
        newVal = pattern.sub(r'\\Program Files\\', newVal)
        pattern = re.compile(r'\\programx86\\', re.IGNORECASE)
        newVal = pattern.sub(r'\\Program Files (x86)\\', newVal)
        print keypath + ' - ' + valname + ' - ' + newVal
        try:
            _winreg.SetValueEx(key, newVal, 0, thisVal[1], thisVal[0])
            _winreg.DeleteValue(key, valname)
        except:
            print sys.exc_info()[0]
            pass
        return

    try:
        re.search(r'\\programx86\\|\\program\\', str(thisVal[0]), re.IGNORECASE)
    except:
        return
    if re.search(r'\\programx86\\|\\program\\', str(thisVal[0]), re.IGNORECASE) is not None:
        newVal = str(thisVal[0])
        pattern = re.compile(r'\\program\\', re.IGNORECASE)
        newVal = pattern.sub(r'\\Program Files\\', newVal)
        pattern = re.compile(r'\\programx86\\', re.IGNORECASE)
        newVal = pattern.sub(r'\\Program Files (x86)\\', newVal)
        print keypath + ' - ' + str(thisVal[0]) + ' - ' + newVal
        try:
            _winreg.SetValueEx(key, valname, 0, thisVal[1], newVal)
        except:
            print sys.exc_info()[0]
            pass


def subkeys(key):
    i = 0
    while True:
        try:
            subkey = _winreg.EnumKey(key, i)
            yield subkey
            i += 1
        except WindowsError:
            break


def traverse_registry_tree(hkey, keypath, arch_key):
    try:
        key = _winreg.OpenKey(hkey, keypath, 0, (_winreg.KEY_ALL_ACCESS + arch_key))
        for subkeyname in subkeys(key):
            if keypath == '':
                subkeypath = subkeyname
            else:
                subkeypath = '%s\\%s' % (keypath, subkeyname)
            outFile.write(subkeypath + '\n')
            traverse_registry_tree(hkey, subkeypath, arch_key)
        i = 0
        while True:
            try:
                value = _winreg.EnumValue(key, i)
                examineValue(key, value[0], keypath)
                i += 1
            except SystemExit:
                raise
            except WindowsError:
                break
            except:
                print keypath
                print value
                raise
    except SystemExit:
        raise
    except:
        e = sys.exc_info()
        outFile.write('!!!' + str(e) + keypath + '\n')
        traceback.print_tb(e[2], None, outFile)
        pass

for arch_key in arch_keys:
    for reg in regs:
        print '\n\n---- %s (%s)' % (reg, arch_key)
        traverse_registry_tree(eval('_winreg.' + reg), '', eval('_winreg.' + arch_key))

outFile.close()
