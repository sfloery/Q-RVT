from pywinauto import findwindows, Application
import os
import datetime
import psutil
import sys
import time
import warnings

def run_rvt(rvt_exe, rvt_dir):

	os.chdir(rvt_dir)

	before = findwindows.find_elements()

	before_id = []
	for window in before:
		before_id.append(window.process_id)


	app = Application()
	app.start(rvt_exe)
	start_time = datetime.datetime.now()
	start_time = start_time

	after = findwindows.find_elements()

	after_id = []
	for window in after:
		after_id.append(window.process_id)

	ide_id = list(set(after_id)-set(before_id))[0]

	ide_app = Application().connect(process=ide_id)
	app_dialog = ide_app.top_window()

	app_dialog.set_focus()
	app_dialog.type_keys(r"{ENTER}")

	while psutil.pid_exists(ide_id):
		time.sleep(0.5)

	return start_time.strftime("%Y-%m-%d_%H-%M-%S")

if __name__ == '__main__':

	warnings.filterwarnings("ignore")
	
	rvt_exe_path = sys.argv[1]
	rvt_dir_path = sys.argv[2]

	start_time = run_rvt(rvt_exe_path, rvt_dir_path)

	print(start_time)
	sys.exit(0)
	