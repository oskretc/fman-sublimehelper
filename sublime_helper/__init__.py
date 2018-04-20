from fman import DirectoryPaneCommand, show_alert, load_json, save_json, YES, NO
from fman.fs import is_dir, exists
from fman.url import splitscheme, as_url
from subprocess import DEVNULL, Popen

import os
import shlex

# TODO, Add this path to Settings file
_SUBLIMETEXTPATHDEFAULT = 'C:/Program Files/Sublime Text 3/subl.exe'
_SUBLIMETEXTCONFIGFILE = 'Sublime Text Config.json'
_SUBLIMETEXTPATH = ''

settings = load_json(_SUBLIMETEXTCONFIGFILE, default={'path': _SUBLIMETEXTPATHDEFAULT})

if settings['path'] and exists(as_url(settings['path'])):
	_SUBLIMETEXTPATH = settings['path']

else:
	_SUBLIMETEXTPATH = _SUBLIMETEXTPATHDEFAULT

class SublimeOpenSelected(DirectoryPaneCommand):
	def __call__(self):
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		chosen_files = self.get_chosen_files()
		option=" "
		if len(chosen_files)>1:
			option= " -n "
		if not chosen_files:
			show_alert('No file is selected!')
			return		
		openCommand(option, chosen_files, path)

class SublimeOpenCurrentFolderInNewWindow(DirectoryPaneCommand):
	def __call__(self):
		url = self.pane.get_path()
		scheme, path = splitscheme(url)

		if scheme != 'file://':
			show_alert('{} is not supported'.format(url))
			return

		paths=[]
		paths.append(as_url(path))	
		chosen_files = self.get_chosen_files()
			
		if chosen_files:
			for file in chosen_files:
				if not is_dir(file):
					paths.append(file)
			

		openCommand(" -n -a  ", paths, path)						

class SublimeSetPath(DirectoryPaneCommand):
	def __call__(self):
		if not set_sublime_install_path():
			show_alert('Failed to update Sublime Text path')

def to_path(url):
	return splitscheme(url)[1]

def set_sublime_install_path():
	new_sublime_filepath, ok = show_prompt('Enter full path to Sublime Text program here', default = get_current_sublime_install_path(), selection_start = 0, selection_end = None )

	if not ok:
		return False

	if not exists(as_url(new_sublime_filepath)):
		show_alert('Path to Sublime Text given is invalid')
		return False

	_SUBLIMETEXTPATH = new_sublime_filepath
	save_json(_SUBLIMETEXTCONFIGFILE, {'path': new_sublime_filepath})
	show_alert('Sublime Text path updated')
	return True

def get_current_sublime_install_path():
	settings = load_json(_SUBLIMETEXTCONFIGFILE, default={'path': _SUBLIMETEXTPATHDEFAULT})

	if settings['path'] and exists(as_url(settings['path'])):
		return settings['path']
	else:
		return _SUBLIMETEXTPATHDEFAULT

def openCommand(option, files, path):
	sublime_path = get_current_sublime_install_path()

	if not exists(as_url(sublime_path)):
		show_alert('Invalid Sublime Text path: ' + sublime_path)
		choice = show_alert('Update Path to Sublime Text?', buttons = YES | NO )

		if choice == YES:
			if not set_sublime_install_path():
				# user failed to set sublime install path. bail.
				show_alert('command failed because no valid path to Sublime Text given')
				return

		else:
			# no path to use, user doesnt want to set one now. bail.
			show_alert('command failed because no valid path to Sublime Text given')
			return

	_SUBLIMETEXTPATH = sublime_path

	# TODO: Check if quoting is working for other platforms
	args = [shlex.quote(to_path(x)) for x in files]
	cmd= _SUBLIMETEXTPATH + " " + option + " " + " ".join(args)
	env = create_clean_environment()
	Popen(cmd, shell=False, cwd=path,
		stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, env=env)

def create_clean_environment():
	# Pyinstaller, used by fman to ship on Linux sets LD_LIBRARY_PATH, which
	# prevents starting Qt5 applications. Remove the variable if it is set.
	env = dict(os.environ)
	try:
		del env['LD_LIBRARY_PATH']
	except KeyError:
		pass
	return env