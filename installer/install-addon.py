import os
import hashlib
import shutil
import sys
import urllib3
import importlib.util

#     connect = urllib3.PoolManager()
            # with open(file_and_path, "wb") as out_file, connect.request('GET',package_url, preload_content=False) as resp:
            #     shutil.copyfileobj(resp, out_file)\
                
                
def _check_hashsums(name: str, file: str):
    dictation = {"arg_parser.py": "226a0e699ed05d844dc34219d5ed7f6e8d543630aead80610b210b44b87e3fd5", "config.py": "5e03bf6ec877fd43d5b63152e85986391e5923828da31c97a6fecdeaa4b5b0ce", "formattext.py": "a44784cf450bfcc456c4d372d7ac5dd57ab103f3305bd0a808a606ab43368002",}
    try:
        hash_here = "A"
        with open(file, "rb") as f:
            hash_here = hashlib.sha256(f).hexdigest().lower()
            f.close()
        if hash_here == dictation[name]:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def _import_frozen(name: str, file: str):
    if not (spec := importlib.util.spec_from_file_location(name, file))  == None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    else:
        if name in sys.modules:
            return sys.modules[name]
        else:
            raise Exception(f"Cannot import '{name}' module!")

def _get_install_paths():
    path_main = os.path.dirname(__file__)
    path = os.path.join(path_main, "plugins")
    try:
        os.makedirs(path)
    except:
        pass
    return path_main, path

def _install_default_addons():
    _main, _plugindir = _get_install_paths()
    socket = urllib3.PoolManager()
    # /home/user/git_repos/github.com/Kovalit31/python-addons/branch/installer/installer/install-addon.py
    url_main_repo = "file:///home/user/git_repos/github.com/Kovalit31/python-addons/branch/main"
    addon_urls = [["addons/argument-parser/0.1-alpha/argument-parser.py", "addons/config/0.2-alpha/config.py", "addons/text-formatter/0.2/text-formatter.py"],["arg_parser.py","config.py", "formattext.py"]]
    for x in range(len(addon_urls[0])):
        _out = os.path.join(_plugindir, addon_urls[1][x])
        _in = os.path.join(url_main_repo, addon_urls[0][x])
        try:
            if not _in.startswith("file://"):
                with open(_out, "wb") as out_file, socket.request("GET", _in, preload_content=False) as in_file:
                    shutil.copyfileobj(in_file, out_file)
            else:
                _in = _in.split("file://")[1]
                shutil.copyfile(_in, _out)
        except Exception as e:
            print(e)

def _import_default_addons():
    _main, _addonpath = _get_install_paths()
    try:
        text_decor = _import_frozen("text_decor", os.path.join(_addonpath, "formattext.py"))
    except:
        text_decor = None
    conf_parse = _import_frozen("conf_parse", os.path.join(_addonpath, "config.py"))
    arg_parse = _import_frozen("arg_parse", os.path.join(_addonpath, "arg_parser.py"))
    return text_decor, arg_parse, conf_parse

def _check_if_can_run():
    _main, _plugindir = _get_install_paths()
    list_required = ["arg_parser.py","config.py"]
    list_recommended = ["formattext.py"]
    for x in range(len(list_required)):
        if os.path.exists(os.path.join(_plugindir, list_required[x])):
            if _check_hashsums(list_required[x], os.path.join(_plugindir, list_required[x])):
                pass
            else:
                return False, 1
        else:
            return False, 1
    for x in range(len(list_recommended)):
        not_found = 0
        if os.path.exists(os.path.join(_plugindir, list_recommended[x])):
            if _check_hashsums(list_recommended[x], os.path.join(_plugindir, list_recommended[x])):
                pass
            else:
                not_found = 1
        else:
            not_found = 1
    else:
        if not not_found:
            print("All recommends is satished, continue...\n")
    return True, not_found
    
def main(args):
    attempts = 3
    current = 0
    while current < attempts:
        runnable, *other = _check_if_can_run() # BUG #1: hashlib: object supporting the buffer API required
        if runnable:
            break
        else:
            _install_default_addons()
            current += 1
    else:
        raise Exception("Can't continue, excepted cyclic deleting and/or modificing!")
    text_decor, arg_parse, conf_parse = _import_default_addons()

if __name__ == "__main__":
    main(sys.argv)