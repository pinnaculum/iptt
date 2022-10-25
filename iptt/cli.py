from ptpython.prompt_style import PromptStyle
from ptpython.layout import CompletionVisualisation
from ptpython import embed
from prompt_toolkit.formatted_text import HTML


def configure(repl):
    class CustomPrompt(PromptStyle):
        def in_prompt(self):
            return HTML("<ansigreen>iptt [%s]</ansigreen>: ") % (
                repl.current_statement_index,
            )

        def in2_prompt(self, width):
            return "...: ".rjust(width)

        def out_prompt(self):
            return HTML("<ansired>Result[%s]</ansired>: ") % (
                repl.current_statement_index,
            )

    repl.all_prompt_styles["custom"] = CustomPrompt()
    repl.prompt_style = "custom"
    repl.show_signature = True
    repl.enable_history_search = True
    repl.enable_auto_suggest = True
    repl.title = 'iptt'
    repl.confirm_exit = False
    repl.vi_keep_last_used_mode = True
    repl.completion_visualisation = CompletionVisualisation.POP_UP
    repl.completion_menu_scroll_offset = 0
    repl.complete_while_typing = False


async def embed_cli(_globals: dict = {},
                    _locals: dict = {}):

    await embed(
        globals=_globals if _globals else globals(),
        locals=_locals if _locals else locals(),
        return_asyncio_coroutine=True,
        patch_stdout=True,
        configure=configure
    )
