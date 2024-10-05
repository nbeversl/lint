from .sublime_urtext import refresh_project_text_command
from .sublime_urtext import UrtextTextCommand

class UrtextLint(UrtextTextCommand):
    
    @refresh_project_text_command()
    def run(self):
        self._UrtextProjectList.current_project.run_directive('LINT', self.view.file_name())
