'''
TODO:
- Implement Open
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import os

# wxPython
import wx

# gui
import gui

# templates
from templates import TemplateContainer
from templates import NonTemplate
from templates import Template
from templates import TemplateManager

# mwparserfromhell
import mwparserfromhell


# =============================================================================
# >> CONSTANTS
# =============================================================================
LABEL_EDIT = 'Edit'
LABEL_ADD = 'Add'
LABEL_REMOVE = 'Remove'

TEMPLATES_PATH = 'templates.ini'


# =============================================================================
# >> GUI
# =============================================================================
class WikiEditorFrame(gui.MainFrame):
    '''
    The GUI class.
    '''

    def __init__(self, parent):
        '''
        Initialzes the object.

        @param <parent>:
        The parent frame of this frame or None:
        '''

        super(WikiEditorFrame, self).__init__(parent)

        if not os.path.isfile(TEMPLATES_PATH):
            wx.MessageBox('Unable to find "{0}".'.format(TEMPLATES_PATH),
                'File not found', wx.OK | wx.ICON_ERROR)
            self.Close()
        else:
            self.template_mngr = TemplateManager(TEMPLATES_PATH)
            self.save_path = None

            # Contains the item ID of the item that was right clicked
            self.selected_item_id = None

            # Build the popup menu that appears on a right click
            self.popup_menu = wx.Menu()

            item = self.popup_menu.Append(-1, LABEL_ADD)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)

            item = self.popup_menu.Append(-1, LABEL_REMOVE)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)

            self.popup_menu.AppendSeparator()

            item = self.popup_menu.Append(-1, LABEL_EDIT)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)

            # After initialization ask for a new project
            self.ask_for_new_project()

    def on_popup_item_selected(self, event):
        '''
        Called when an item has been selected from the popup menu.
        '''

        action = self.popup_menu.FindItemById(event.GetId()).GetText()
        tree_part = self.wiki_items.GetItemData(self.selected_item_id).GetData()

        # Handle edit action
        if action == LABEL_EDIT:
            self.send_edit_dialog(tree_part)

        # Handle add action
        elif action == LABEL_ADD:
            # Ask the user which template should be used if there are more
            # than one
            if len(tree_part.templates) > 1:
                # Create a new dialog...
                dialog = gui.ChooseTemplateDialog(self)

                # ... and add all possible templates
                dialog.template.AppendItems(tree_part.templates)

                # Did the user chose a valid template?
                if dialog.ShowModal() == wx.ID_OK and dialog.template.Selection != wx.NOT_FOUND:
                    template_name = dialog.template.GetString(dialog.template.Selection)
                    dialog.Destroy()
                else:
                    dialog.Destroy()
                    return
            else:
                # If there is just one template, just use it without asking
                template_name = tree_part.templates[0]

            # Get the template which is hold by the container
            template = self.template_mngr.get_template(template_name)

            # Add the template as a child to the container
            new_node = self.wiki_items.AppendItem(self.selected_item_id, template.name)
            self.wiki_items.SetItemData(new_node, wx.TreeItemData(template))
            for tree_part in template.values():
                item = self.wiki_items.AppendItem(new_node, tree_part.name)
                self.wiki_items.SetItemData(item, wx.TreeItemData(tree_part))

        # Handle remove action
        elif action == LABEL_REMOVE:
            # Remove the node from the tree. All children are also removed.
            self.wiki_items.Delete(self.selected_item_id)

        # Handle all other actions. This should not happen.
        else:
            raise NotImplementedError('Should not happen!')

        # Finally, update the current data box
        self.display_current_data()

    def on_wiki_item_activated(self, event):
        '''
        Called when an item has been activated by hitting enter or
        double-clicking it.
        '''

        tree_part = self.wiki_items.GetItemData(event.GetItem()).GetData()

        # Only NonTemplate objects are editable!
        if isinstance(tree_part, NonTemplate):
            self.send_edit_dialog(tree_part)

    def on_wiki_items_right_click(self, event):
        '''
        Called when a wiki item has been right-clicked.
        '''

        item_id = event.GetItem()
        self.selected_item_id = item_id
        tree_part = self.wiki_items.GetItemData(item_id).GetData()

        enabled = None

        # Find the action that should be enabled
        if isinstance(tree_part, Template):
            enabled = LABEL_REMOVE
        elif isinstance(tree_part, NonTemplate):
            enabled = LABEL_EDIT
        elif isinstance(tree_part, TemplateContainer):
            enabled = LABEL_ADD
        else:
            raise NotImplementedError('Should not happen')

        # Enable the found action and disable all other actions
        for item in self.popup_menu.GetMenuItems():
            item.Enable(item.GetLabel() == enabled)

        self.PopupMenu(self.popup_menu, event.GetPoint())

    def on_wiki_item_selection(self, event):
        '''
        Called when the selection of a wiki item has been changed.
        '''

        # Update the output box
        self.display_current_data()

    def on_new_project(self, event):
        '''
        Called when a new project should be started.
        '''

        self.ask_for_new_project()

    def on_open_file(self, event):
        '''
        Called when a file should be opened.
        '''

        open_file_dialog = wx.FileDialog(self, 'Open', style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if open_file_dialog.ShowModal() == wx.ID_CANCEL:
            return

        with open(open_file_dialog.GetPath(), 'r') as f:
            wikicode = mwparserfromhell.parse(f.read())

        # Get the base template
        templates = wikicode.filter_templates(recursive=False)
        if len(templates) != 1:
            raise ValueError('Number of base templates does not equal 1.')

        wiki_template = templates[0]

        # Get the new template
        template = self.template_mngr.get_template(wiki_template.name.strip())

        # Reset the tree
        self.wiki_items.DeleteAllItems()
        self.save_path = open_file_dialog.GetPath()

        def add_parameters(parent, template, wiki_template):
            '''
            Adds the parameters and its values to the tree.

            @param <parent>:
            A TreeItemId object that defines the root of the template.

            @param <template>:
            A Template object whose parameters should be added.

            @param <wiki_template>:
            A Wikicode object.
            '''

            # We want to know if the file defines an unknown parameter
            params = map(lambda tree_part: tree_part.name, template.values())
            for param in map(lambda param: param.name.strip(), wiki_template.params):
                if param not in params:
                    raise NameError('Unknown paramter "{0}".'.format(param))

            # Add all the parameters of the template
            for tree_part in template.values():
                item = self.wiki_items.AppendItem(parent, tree_part.name)
                self.wiki_items.SetItemData(item, wx.TreeItemData(tree_part))

                # If the template did not define this parameter, just continue
                if not wiki_template.has(tree_part.name):
                    continue

                # Get the value of the parameters
                param = wiki_template.get(tree_part.name).value

                if isinstance(tree_part, NonTemplate):
                    tree_part.value = str(param)

                elif isinstance(tree_part, TemplateContainer):
                    # Loop through all templates the current parameter defined
                    for child_wiki_template in param.filter_templates(recursive=False):
                        child_template_name = child_wiki_template.name.strip()
                        child_template = self.template_mngr.get_template(child_template_name)

                        child = self.wiki_items.AppendItem(item, child_template_name)
                        self.wiki_items.SetItemData(child, wx.TreeItemData(child_template))

                        # Add its parameters recursively
                        add_parameters(child, child_template, child_wiki_template)
                else:
                    raise ValueError('Unexpected tree part object.')

        # Save it as the root item
        root = self.wiki_items.AddRoot(template.name)
        self.wiki_items.SetItemData(root, wx.TreeItemData(template))

        # Add the parameters recursively
        add_parameters(root, template, wiki_template)

        # Show every node
        self.wiki_items.ExpandAll()

        # Update the output box
        self.display_current_data()
        
        # Force the scrollbar to be on the top
        self.wiki_items.SetScrollPos(wx.VERTICAL, 0)

    def on_save_file(self, event):
        '''
        Called when the project should be saved to a file.
        '''

        # Get the root item ID
        root_item_id = self.wiki_items.GetRootItem()

        # Do not save there is no root item
        if not root_item_id.IsOk():
            return

        # Wasn't saved before?
        if self.save_path is None:
            self.on_save_file_as(event)
            return

        with open(self.save_path, 'w') as f:
            f.write(self.wiki_items.GetItemData(root_item_id).GetData(
                ).generate_data(self.wiki_items, root_item_id))

    def on_save_file_as(self, event):
        '''
        Called when the project should be saved to a specific file.
        '''

        # Get the root item ID
        root_item_id = self.wiki_items.GetRootItem()

        # Do not save there is no root item
        if not root_item_id.IsOk():
            return

        save_file_dialog = wx.FileDialog(self, 'Save', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save_file_dialog.ShowModal() == wx.ID_CANCEL:
            return

        self.save_path = save_file_dialog.GetPath()
        self.on_save_file(event)

    def on_copy_all_to_clipboard(self, event):
        '''
        Generates the data by using the root item and copies it to the
        clipboard.
        '''

        self.set_clipboard_data(self.wiki_items.GetRootItem())

    def on_copy_to_clipboard(self, event):
        '''
        Generates the data by using the focused item and copies it to the
        clipboard.
        '''
        
        self.set_clipboard_data(self.wiki_items.GetFocusedItem())

    def set_clipboard_data(self, item_id):
        '''
        Generates the data by using the given item and copies it to the
        clipboard.
        '''

        if not item_id.IsOk():
            return
            
        data = self.wiki_items.GetItemData(
            item_id).GetData().generate_data(self.wiki_items, item_id)
            
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()

    def init_new_project(self, template_name):
        '''
        Initializes a new project.

        @param <template_name>:
        The name of the template that should be used as the base.
        '''

        # Delete all items from the tree
        self.wiki_items.DeleteAllItems()

        # Set the save to None, so the save as dialog will be displayed again
        self.save_path = None

        # Get the new template
        template = self.template_mngr.get_template(template_name)

        # Save it as the root item
        root = self.wiki_items.AddRoot(template.name)
        self.wiki_items.SetItemData(root, wx.TreeItemData(template))

        # Add its children
        for tree_part in template.values():
            item = self.wiki_items.AppendItem(root, tree_part.name)
            self.wiki_items.SetItemData(item, wx.TreeItemData(tree_part))

        # Show every node
        self.wiki_items.ExpandAll()

    def send_edit_dialog(self, tree_part):
        '''
        Sends the edit dialog to the user.

        @param <tree_part>:
        The tree part that should be edited.
        '''

        dialog = gui.SingleItemEditDialog(self)
        dialog.input_box.Value = tree_part.value
        if dialog.ShowModal() == wx.ID_OK:
            tree_part.value = dialog.input_box.Value

            # Update the output box
            self.display_current_data()

        dialog.Destroy()

    def ask_for_new_project(self):
        '''
        Send the dialog that ask for a project type. If a new project type
        has been choosen, it will be initialized.
        '''

        dialog = gui.NewProjectDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            project_type = dialog.project_type.GetString(
                dialog.project_type.Selection)
        else:
            project_type = ''

        dialog.Destroy()

        if project_type:
            self.init_new_project(project_type)

    def display_current_data(self):
        '''
        Updates the text box on the right side with the current data.
        '''

        item_id = self.wiki_items.GetFocusedItem()
        if not item_id.IsOk():
            item_id = self.wiki_items.GetRootItem()
            if not item_id.IsOk():
                return

        self.output.Value = self.wiki_items.GetItemData(
            item_id).GetData().generate_data(self.wiki_items, item_id)


# =============================================================================
# >> MAIN ROUTINE
# =============================================================================
def main():
    '''
    Starts the GUI.
    '''

    app = wx.App(False)
    frame = WikiEditorFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()