import re
import sys
import os
from os import path
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand
import sublime_plugin
import sublime
import functools
import locale
import tempfile


def settings_get(name, default=None):
    # load up the plugin settings
    plugin_settings = sublime.load_settings('Stylus.sublime-settings')
    # project plugin settings? sweet! no project plugin settings? ok, well promote plugin_settings up then
    if sublime.active_window() and sublime.active_window().active_view():
        project_settings = sublime.active_window().active_view().settings().get("Stylus")
    else:
        project_settings = {}

    # what if this isn't a project?
    # the project_settings would return None (?)
    if project_settings is None:
        project_settings = {}

    setting = project_settings.get(name, plugin_settings.get(name, default))
    return setting


def run(cmd, args=[], source="", cwd=None, env=None, callback=None):
    """
    Run command. "coffee", "cake", etc.
    Will run on thread if callback function is passed.
    """
    if callback:
        threading.Thread(target=lambda cb: cb(_run(cmd, args=args, source=source, cwd=cwd, env=env)), args=(callback,)).start()
    else:
        res = _run(cmd, args=args, source=source, cwd=cwd, env=env)
        return res


def _run(cmd, args=[], source="", cwd=None, env=None):
    if not type(args) is list:
        args = [args]
    if sys.platform == "win32":
        args = [cmd] + args
        if sys.version_info[0] == 2:
            for i in range(len(args)):
                args[i] = args[i].encode(locale.getdefaultlocale()[1])
        proc = Popen(args, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        try:
            stat = proc.communicate(input=source)
        except:
            stat = proc.communicate(input=source.encode("utf8"))
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode(locale.getdefaultlocale()[1]), "err": stat[1].decode(locale.getdefaultlocale()[1])}
    else:
        if env is None:
            env = {"PATH": settings_get('binDir', '/usr/local/bin')}

        # adding custom PATHs from settings
        customEnv = settings_get('envPATH', "")
        if customEnv:
            env["PATH"] = env["PATH"]+":"+customEnv
        if source == "":
            command = [cmd] + args
        else:
            command = [cmd] + args + [source]
        proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode('utf-8'), "err": stat[1].decode('utf-8')}


def isStylus(view=None):
    if view is None:
        view = sublime.active_window().active_view()
    correct_scope = False
    for region in view.sel():
        correct_scope = correct_scope or ('source.stylus' in view.scope_name(region.b))
    return correct_scope



class StyluscompileCommand(TextCommand):
    def is_enabled(self):
        return isStylus(self.view)

    def run(self, *args, **kwargs):
        compile_dir = settings_get('compileDir')
        source_file = self.view.file_name()
        source_dir = os.path.normcase(os.path.dirname(source_file))
        try:
            project_file = self.view.window().project_file_name()
        except AttributeError:
            project_file = ''
        if project_file:
            project_dir = os.path.normcase(os.path.dirname(project_file))
        compile_paths = settings_get('compilePaths')
        compress = settings_get('compress', False)

        args = [source_file]
        if compress:
            args = ['-c'] + args

        use_autoprefixer = settings_get('useAutoPrefixer', False)
        if use_autoprefixer is True:
            print("Using autoprefixer...")
            args = ['--use', 'autoprefixer-stylus'] + args

        # check instance of compile_paths
        if isinstance(compile_paths, dict):
            appendix_len = None
            for key_path in compile_paths:
                norm_path = os.path.normcase(key_path)
                if not os.path.isabs(norm_path) and project_file:
                    norm_path = os.path.join(project_dir, norm_path)
                appendix = os.path.relpath(source_dir, norm_path)
                if not appendix.startswith('..') and (appendix_len is None or len(appendix) < appendix_len):
                    appendix_len = len(appendix)
                    compile_dir = compile_paths[key_path]
                    if not os.path.isabs(compile_dir):
                        compile_dir = os.path.join(norm_path, compile_dir)
                    compile_dir = os.path.join(compile_dir, appendix)

        if compile_dir and (isinstance(compile_dir, str)):
            # Check for absolute path or relative path for compile_dir
            if not os.path.isabs(compile_dir):
                compile_dir = os.path.join(source_dir, compile_dir)
            print("Compile to:" + compile_dir)
            # create folder if not exist
            if not os.path.exists(compile_dir):
                os.makedirs(compile_dir)
                print("Compile dir did not exist, created folder: " + compile_dir)
            folder, file_nm = os.path.split(source_file)
            args = ['--out', compile_dir] + args
        else:
            compile_dir = source_dir
            print("Compile to same directory")

        cwd = None
        result = run("stylus", args=args, cwd=cwd)

        if result['okay'] is True:
            status = 'Compilation Succeeded'
        else:
            lines = result['err'].splitlines()
            if len(lines) >= 3:
                line = lines[2]
                if re.search("throw err;$", line):
                    # Remove useless lines
                    lines = lines[4:]
                    index = 0
                    linenb = 0
                    for line in lines:
                        if re.search("^    at ", line):
                            linenb = index
                            break
                        index += 1
                    if linenb > 0:
                        # remove useless lines
                        lines = lines[:linenb - 1]

            status = 'Compilation FAILED ' + lines[0]
            sublime.error_message("\n".join(lines))

        later = lambda: sublime.status_message(status)
        sublime.set_timeout(later, 300)

class StylusIndentCommand(TextCommand):
    def is_enabled(self):
        return isStylus(self.view)

    def is_visible(self):
        return False

    def is_scope(self, offset, scope):
        return self.view.score_selector(offset, scope) > 0

    def is_selector_scope(self, offset):
        return self.is_scope(offset, 'meta.selector.stylus')

    def is_interpolation_scope(self, offset):
        return self.is_scope(offset, 'stylus.embedded.source')

    def run(self, *args, **kwargs):
        is_selector = True
        for region in self.view.sel():
            left_offset = min(region.a, region.b)
            line_region = self.view.line(region)
            line_text = self.view.substr(line_region)
            is_selector = is_selector and (
                (not self.is_interpolation_scope(left_offset)) and
                (self.is_selector_scope(left_offset) or (
                    self.view.size() == left_offset and
                    self.is_selector_scope(left_offset - 1)
                ) or (
                    re.search('\\{\\s*$', line_text)
                ) or (
                    re.search('^\\s*(if|else|for)\\b', line_text)
                ))
            )
        snippet = "\n"
        if is_selector:
            snippet = "\n\t"
        self.view.run_command('insert_snippet', { 'contents': snippet })



class CaptureEditing(sublime_plugin.EventListener):
    def is_enabled(self, view):
        return isStylus(view)

    def on_post_save(self, view):
        if not self.is_enabled(view):
            return
        compile_on_save = settings_get('compileOnSave', False)
        if compile_on_save is True:
            print("Compiling on save...")
            view.run_command("styluscompile")
