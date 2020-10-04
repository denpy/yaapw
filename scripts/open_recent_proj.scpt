on run argv
  tell application "PyCharm"
	  if it is not running then launch
	  activate
  end tell

  set projName to item 1 of argv
  tell application "System Events"
    tell process "PyCharm"
      set frontmost to true
      click menu item projName of menu 1 of menu item "Open Recent" of menu "File" of menu bar 1
   end tell
 end tell
end run

