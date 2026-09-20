"""
Execute Python code in code blocks and construct a interactive Python console output.

This allows you to write code examples, but then execute them, showing the results.
"""
from functools import partial
import ast
import re
from io import StringIO
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import find_formatter_class
import code

PY310 = (3, 10) <= sys.version_info
PY311 = (3, 11) <= sys.version_info

RE_INIT = re.compile(r'^\s*#\s*pragma:\s*init\n(.*?)#\s*pragma:\s*init\n', re.DOTALL | re.I)

AST_BLOCKS = (
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
    ast.FunctionDef,
    ast.ClassDef,
    ast.AsyncFor,
    ast.AsyncWith,
    ast.AsyncFunctionDef
)

if PY310:
    AST_BLOCKS = AST_BLOCKS + (ast.Match,)

if PY311:
    AST_BLOCKS = AST_BLOCKS + (ast.TryStar,)


if 'SESSIONS' not in globals() or not globals()["SESSIONS"]:
    SESSIONS = {}


def reset():
    """Reset hook."""

    SESSIONS.clear()


class IPY(code.InteractiveInterpreter):
    """Handle code."""

    def __init__(self, show_except=True, locals=None):  # noqa: A002
        """Initialize."""

        super().__init__(locals=locals)

        self.show_except = show_except

    def set_exceptions(self, enable):
        """Set exceptions handling."""

        self.show_except = enable

    def write(self, data):
        """Write."""

        if not self.show_except:
            raise RuntimeError(data)

        sys.stdout.write(data)


class StreamOut:
    """Override the standard out."""

    def __init__(self):
        """Initialize."""
        self.old = sys.stdout
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def read(self):
        """Read the `stringIO` buffer."""

        value = ''
        if self.stdout is not None:
            self.stdout.flush()
            value = self.stdout.getvalue()
            self.stdout = StringIO()
            sys.stdout = self.stdout
        return value

    def __enter__(self):
        """Enter."""
        return self

    def __exit__(self, type, value, traceback):  # noqa: A002
        """Exit."""

        sys.stdout = self.old
        self.old = None
        self.stdout = None


def execute(cmd, no_except=True, init='', ipy=None, g=None):
    """Execute color commands."""

    # Setup global initialization
    if g is None:
        g = {}

    # Setup global initialization
    if ipy is None:
        ipy = IPY(show_except=not no_except, locals=g)
    if init:
        ipy.set_exceptions(False)
        execute(init.strip(), ipy=ipy, g=g)
        ipy.set_exceptions(not no_except)

    console = ''

    # Build `AST` tree
    m = RE_INIT.match(cmd)
    if m:
        block_init = m.group(1)
        src = cmd[m.end():]
        ipy.set_exceptions(False)
        execute(block_init, ipy=ipy, g=g)
        ipy.set_exceptions(not no_except)
    else:
        src = cmd
    lines = src.split('\n')
    try:
        tree = ast.parse(src)
    except Exception as e:
        if no_except:
            from pymdownx.superfences import SuperFencesException
            raise SuperFencesException from e
        import traceback
        return '{}'.format(traceback.format_exc())

    for node in tree.body:
        result = []

        # Format source as Python console statements
        start = node.lineno
        end = node.end_lineno
        stmt = lines[start - 1: end]
        command = ''
        payload = '\n'.join(stmt)
        for i, line in enumerate(stmt, 0):
            if i == 0:
                stmt[i] = '>>> ' + line
            else:
                stmt[i] = '... ' + line
        if stmt:
            command += '\n'.join(stmt)
        if isinstance(node, AST_BLOCKS):
            command += '\n... '

        try:
            # Capture anything sent to standard out
            with StreamOut() as s:
                # Execute code
                ipy.runsource(payload)

                # Output captured standard out after statements
                text = s.read()
                if text:
                    result.append(text)

                # Execution went well, so append command
                console += command

        except Exception as e:
            if no_except:
                from pymdownx.superfences import SuperFencesException
                raise SuperFencesException from e
            import traceback
            console += '{}\n{}'.format(command, traceback.format_exc())
            # Failed for some reason, so quit
            break

        # If we got a result, output it as well
        console += '\n{}'.format(''.join(result))

    return console


def colorize(src, lang, **options):
    """Colorize."""

    HtmlFormatter = find_formatter_class('html')
    lexer = get_lexer_by_name(lang, **options)
    formatter = HtmlFormatter(cssclass="highlight", wrapcode=True)
    return highlight(src, lexer, formatter).strip()


def py_command_validator(language, inputs, options, attrs, md):
    """Python validator."""

    valid_inputs = {'exceptions', 'play'}

    if not hasattr(md, 'pycon_sessions'):
        md.pycon_sessions = {}

    for k, v in inputs.items():
        if k == 'session':
            if v not in md.pycon_sessions:
                md.pycon_sessions[v] = {}
            options['session_name'] = v
            options['session'] = md.pycon_sessions[v]
            continue
        if k in valid_inputs:
            options[k] = True
            continue
        attrs[k] = v
    return True


def py_command_reset(md):
    """Reset."""

    if hasattr(md, 'pycon_sessions'):
        md.pycon_sessions.clear()


def _py_command_formatter(
    src="",
    language="",
    class_name=None,
    options=None,
    md="",
    init='',
    **kwargs
):
    """Formatter wrapper."""

    from pymdownx.superfences import SuperFencesException

    try:
        # Check if we should allow exceptions
        exceptions = options.get('exceptions', False) if options is not None else False
        run = options.get('play', False) if options is not None else False
        session = options.get('session') if options is not None else None

        if run:
            console = execute(src.strip(), not exceptions, init=init, g=session)
            language = 'pycon'
        else:
            console = src
            language = 'py'

        el = md.preprocessors['fenced_code_block'].extension.superfences[0]['formatter'](
            src=console,
            class_name="class_name",
            language=language,
            md=md,
            options=options,
            **kwargs
        )
    except SuperFencesException:
        import traceback
        print(src)
        print(traceback.format_exc())
        raise
    except Exception:
        from pymdownx import superfences
        import traceback
        print(src)
        print(traceback.format_exc())
        return superfences.fence_code_format(src, 'text', class_name, options, md, **kwargs)
    return el


def py_command_formatter(init=''):
    """Return a Python command formatter with the provided imports."""

    return partial(_py_command_formatter, init=init)
