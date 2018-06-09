import sublime
import sublime_plugin

import os
import re
import json

class LoadProjectFile(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()
        file_name = window.active_view().file_name()

        project_data = None
        settings_file = ''
        current_dir = os.path.dirname(file_name)
        settings_re = re.compile("(\s|\S)*\.sublime-project")

        while current_dir != '/' and settings_file == '':
            parent = os.path.dirname(current_dir)

            for file in os.listdir(current_dir):
                if settings_re.match(file):
                    settings_file = os.path.join(current_dir, file)
                    break

            if settings_file:
                break

            current_dir = parent

        if settings_file != '':
            with open(settings_file) as data:
                try:
                    project_data = json.load(data)
                except ValueError:
                    print('Found a sublime-project file, but it does not appear to contain any project data')
                    project_data = {
                        "folders": [
                            {
                                "path": current_dir
                            }
                        ]
                    }

            if 'folders' in project_data:
                for index, folder in enumerate(project_data['folders']):
                    folder_sq = folder["path"].split(os.sep)

                    if folder_sq[0] == '.':
                        folder_sq[0] = current_dir

                    if folder_sq[0] == '..':
                        folder_sq[0] = os.path.dirname(current_dir)

                    project_data["folders"][index]["path"] = os.sep.join(folder_sq)

            window.set_project_data(project_data)
            print('Project data loaded from ', settings_file)

        else:
            print('No sublime-project could be found in the file tree')
