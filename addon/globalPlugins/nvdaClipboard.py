# -*- coding: UTF-8 -*-
# NVDA addon: Append selected text to clipboard and clear clipboard

import api
import textInfos
import ui
from scriptHandler import script
import globalPluginHandler
import winUser
import gui


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    @script(
        description="Append current selected text to clipboard",
        gesture="kb:NVDA+windows+c",
    )
    def script_appendSelectionToClipboard(self, gesture):

        obj = api.getFocusObject()

        # Handle browsers and document interceptors
        treeInterceptor = obj.treeInterceptor
        if treeInterceptor and not treeInterceptor.passThrough:
            obj = treeInterceptor

        try:
            info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info = None

        if not info or info.isCollapsed:
            ui.message("No selection")
            return

        selectedText = info.text

        # Get current clipboard text
        try:
            clipboardText = api.getClipData()
        except:
            clipboardText = None

        # Combine clipboard text and new selection
        if clipboardText and isinstance(clipboardText, str) and not clipboardText.isspace():
            newText = clipboardText + "\n" + selectedText
        else:
            newText = selectedText

        api.copyToClip(newText)

        ui.message(f"Appended to clipboard: {selectedText}")


    @script(
        description="Clear clipboard",
        gesture="kb:NVDA+shift+delete",
    )
    def script_clearClipboard(self, gesture):

        try:
            with winUser.openClipboard(gui.mainFrame.Handle):
                winUser.emptyClipboard()
                winUser.setClipboardData(winUser.CF_UNICODETEXT, "")
            ui.message("Clipboard cleared")
        except OSError:
            ui.message("Unable to clear clipboard")