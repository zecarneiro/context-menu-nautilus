# VSCode Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call
import os
import configparser
import logging

REMOTE_URI_SCHEME = ['ftp', 'sftp']

class ContextMenuExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        self.configDir = os.path.expanduser("~") + "/.config/context-menu-nautilus"
        self.logFile = self.configDir + "/context-menu.log"

        if not os.path.exists(self.configDir):
            os.makedirs(self.configDir)

        if os.path.exists(self.logFile):
          os.remove(self.logFile)

        logging.basicConfig(
            filename=self.logFile,
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

        logging.info("Starting ...")

    def get_all_context_menu_config(self):
        configs = []
        files = os.listdir(self.configDir)
        for file in files:
            config = configparser.ConfigParser()
            filePath = self.configDir + "/" + file
            if not os.path.isdir(filePath) and filePath != self.logFile:
                config.read(filePath)
                configs.append({
                    "file": file,
                    "config": config
                })

        return configs

    def get_config(self, file_, config):
        isValid = True
        mapConfig = {
            'Name': '',
            'Label': '',
            'BackgroundLabel': '',
            'DirTip': '',
            'DirCommand': '',
            'FileTip': '',
            'FileCommand': '',
            'IsValid': False
        }
        if 'DEFAULT' in config and 'Name' in config['DEFAULT'] and 'Label' in config['DEFAULT'] and 'BackgroundLabel' in config['DEFAULT']:
            mapConfig['Name'] = config['DEFAULT']['Name']
            mapConfig['Label'] = config['DEFAULT']['Label']
            mapConfig['BackgroundLabel'] = config['DEFAULT']['BackgroundLabel']
        else:
            logging.error("Must be set Name, Label and BackgroundLabel on config file:" + file_)
            isValid = False

        if isValid:
            if 'DIRECTORIES' in config and 'Command' in config['DIRECTORIES']:
                mapConfig['DirCommand'] = config['DIRECTORIES']['Command']
                if 'Tip' in config['DIRECTORIES']:
                    mapConfig['DirTip'] = config['DIRECTORIES']['Tip']

            if 'FILES' in config and 'Command' in config['FILES']:
                mapConfig['FileCommand'] = config['FILES']['Command']
                if 'Tip' in config['FILES']:
                    mapConfig['FileTip'] = config['FILES']['Tip']

            if len(mapConfig['DirCommand']) == 0 and len(mapConfig['FileCommand']) == 0:
                logging.error("Must be set one of command(File or Dir) on config file:" + file_)
                isValid = False

        mapConfig['IsValid'] = isValid
        return mapConfig

    def launch_context_menu(self, menu, command: str, files):
        currentFileKey = "__CURRENT_FILE__"
        safepaths = ''
        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

        command = command.replace(currentFileKey, safepaths) + " &"
        logging.info("Execute command: " + command)
        call(command, shell=True)

    def build_item(self, name: str, label: str, tip: str, command: str, isBackground: bool, file_):
        backgroundSuffix = "Background"
        if file_.get_uri_scheme() in REMOTE_URI_SCHEME:
            remoteSuffix = "Remote"
            if isBackground:
                name = name + backgroundSuffix + remoteSuffix
        else:
            if isBackground:
                name = name + backgroundSuffix

        item = Nautilus.MenuItem(
            name=name,
            label=label,
            tip=tip
        )
        item.connect('activate', self.launch_context_menu, command, [file_])
        if isBackground:
            logging.info("Add directory context menu entry to: " + label)
        else:
            logging.info("Add file context menu entry to: " + label)

        return item

    def get_file_items(self, *args):
        items = []
        files = args[-1]
        file_ = files[0]
        configs = self.get_all_context_menu_config()
        for config in configs:
            mapedConfig = self.get_config(config['file'], config['config'])
            if mapedConfig['IsValid']:
                if not file_.is_directory() and len(mapedConfig['FileCommand']) > 0:
                    items.append(self.build_item(mapedConfig['Name'], mapedConfig['Label'], mapedConfig['FileTip'], mapedConfig['FileCommand'], False, file_))
                if file_.is_directory() and len(mapedConfig['DirCommand']) > 0:
                    items.append(self.build_item(mapedConfig['Name'], mapedConfig['Label'], mapedConfig['DirTip'], mapedConfig['DirCommand'], False, file_))

        return items

    def get_background_items(self, *args):
        items = []
        current_dir = args[-1]
        configs = self.get_all_context_menu_config()
        for config in configs:
            mapedConfig = self.get_config(config['file'], config['config'])
            if mapedConfig['IsValid'] and len(mapedConfig['DirCommand']) > 0:
                items.append(self.build_item(mapedConfig['Name'], mapedConfig['BackgroundLabel'], mapedConfig['DirTip'], mapedConfig['DirCommand'], True, current_dir))

        return items
