from pywinauto import findwindows, Application
import os
import time

os.chdir("C:\\RVT_1.3_Win64\\")

before = findwindows.find_elements()

before_id = []
for window in before:
	before_id.append(window.process_id)


app = Application()
app.start("C:\\RVT_1.3_Win64\\RVT_1.3_Win64.exe")


after = findwindows.find_elements()

after_id = []
for window in after:
	after_id.append(window.process_id)

ide_id = list(set(after_id)-set(before_id))[0]

ide_app = Application().connect(process=ide_id)
app_dialog = ide_app.top_window()

#app_dialog.minimize()
app_dialog.set_focus()
app_dialog.type_keys(r"{ENTER}")