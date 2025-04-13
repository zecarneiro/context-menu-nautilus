# context-menu-nautilus

NOTE: This repository was based on https://github.com/harry-cpp/code-nautilus

This repo provides a `ini` configs files extension for Nautilus.

## Install Extension

If not the first time that you install this app on your PC, please, run uninstall first.

```
wget -qO- https://raw.githubusercontent.com/zecarneiro/context-menu-nautilus/master/install.sh | bash
```

If you clone this project, to install you need to run this command: `./install.sh local`

## Uninstall Extension

```
wget -qO- https://raw.githubusercontent.com/zecarneiro/context-menu-nautilus/master/uninstall.sh | bash
```

## Configs files actions

All configs files must be on directory: `~/.config/context-menu-nautilus`

Example for VSCode: `~/.config/context-menu-nautilus/vscode.ini`

```
; TAG __CURRENT_FILE__ will replaced with selected current file
; For example: code __CURRENT_FILE__
; If you selected file name /path/to/file
; The command will be: code "/path/to/file"

[DEFAULT]
Name = VSCodeOpen
Label = Open with Code
BackgroundLabel = Open Code Here

[DIRECTORIES]
Tip = Opens the current directory in VSCode
Command = code --new-window __CURRENT_FILE__

[FILES]
Tip = Opens the selected files with VSCode
Command = code --new-window __CURRENT_FILE__
```

IMPORTANT: After inserting into the folder(`~/.config/context-menu-nautilus`), its necessary to restart nautilus with command `nautilus -q`
