import sublime, sublime_plugin
import subprocess, os


class PerldocCommand(sublime_plugin.WindowCommand):

    def run(self):
        settings = self.window.active_view().settings()

        self.show_in_panel = settings.get('show_perldoc_in_panel', False)

        build_env = settings.get('build_env')
        if build_env and build_env.get('PATH'):
            os.environ['PATH'] = build_env['PATH']

        self.show_document()

    def show_document(self):
        view = self.window.active_view()
        selection = view.substr(view.sel()[0])

        if selection:
            self.done(selection)
        else:
            self.window.show_input_panel(self.caption(), self.initial_text(), self.done, self.change, self.cancel)

    def caption(self):
        return 'perldoc'

    def initial_text(self):
        return ''

    def done(self, str):
        self.title = 'perldoc — {}'.format(str)
        self.command(['perldoc', '-T', str])

    def change(self, str):
        pass

    def cancel(self):
        pass

    def command(self, command):
        output = subprocess.check_output(command).decode('utf-8')
        self.show_result(output)

    def show_result(self, result):
        if self.show_in_panel:
            self.show_panel(result)
        else:
            self.show_window(result)

    def show_panel(self, text):
        output_panel = self.window.create_output_panel('perldoc_panel')
        output_panel.run_command('append', {'characters': text})
        self.window.run_command('show_panel', {'panel': 'output.perldoc_panel'})

    def show_window(self, text):
        output_view = self.window.new_file(flags=0)
        output_view.assign_syntax('Packages/SublimePerldoc/man-pages.tmbundle/Syntaxes/Man.tmLanguage')
        output_view.set_name(self.title)
        output_view.set_scratch(True)
        output_view.run_command('append', {'characters': text})


class PerldocsourceCommand(PerldocCommand):

    def caption(self):
        return 'perldoc -lm'

    def done(self, str):
        self.command(['perldoc', '-lm', str])

    def show_result(self, result):
        self.window.open_file(result)
