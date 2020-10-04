tell application "System Events"
	tell process "PyCharm"
		-- set frontmost to true
		set menuItems to (name of every menu item of menu 1 of menu item "Open Recent" of menu "File" of menu bar 1)
	end tell
end tell

-- https://stackoverflow.com/questions/37289223/convert-applescript-list-into-string
on list2string(theList, theDelimiter)

	-- First, we store in a variable the current delimiter to restore it later
	set theBackup to AppleScript's text item delimiters

	-- Set the new delimiter
	set AppleScript's text item delimiters to theDelimiter

	-- Perform the conversion
	set theString to theList as string

	-- Restore the original delimiter
	set AppleScript's text item delimiters to theBackup

	return theString

end list2string

list2string(menuItems, "+")
