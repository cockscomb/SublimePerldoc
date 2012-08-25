import sublime, sublime_plugin
import commands, os


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
    self.command('perldoc -T {0}'.format(str))

  def change(self, str):
    pass

  def cancel(self):
    pass

  def command(self, command):
    output = commands.getoutput(command).decode('utf-8')
    self.show_result(output)

  def show_result(self, result):
    if self.show_in_panel:
      self.show_panel(result)
    else:
      self.show_window(result)

  def update_view(self, view, text):
    edit = view.begin_edit()
    view.insert(edit, 0, text)
    view.end_edit(edit)

  def show_panel(self, text):
    output_panel = self.window.get_output_panel('perldoc_panel')
    self.update_view(output_panel, text)
    self.window.run_command('show_panel', {'panel': 'output.perldoc_panel'})

  def show_window(self, text):
    output_view = self.window.new_file()
    self.update_view(output_view, text)
    output_view.run('')


class PerldocsourceCommand(PerldocCommand):

  def caption(self):
    return 'perldoc -lm'

  def done(self, str):
    self.command('perldoc -lm {0}'.format(str))

  def show_result(self, result):
    self.window.open_file(result)
