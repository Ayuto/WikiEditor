# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import copy

from configobj import ConfigObj

from collections import OrderedDict


# =============================================================================
# >> CLASSES
# =============================================================================
class TreePart(object):
    '''
    Base class for everything in a tree.

    Treat this as an abstract class!
    '''

    def __init__(self, name):
        '''
        Initializes the class.

        @param <name>:
        The name of the node in the tree.
        '''

        self.name = name

    def generate_data(self, wiki_items, item_id):
        '''
        Generates the data for a tree node.

        @param <wiki_items>:
        A wx.TreeCtrl object.

        @param <item_id>:
        The item ID of thise node.

        A subclass needs to implement this!
        '''

        raise NotImplementedError


class TemplateContainer(TreePart):
    '''
    Represents a node in the tree that can store an unlimited number of
    children.
    '''

    def __init__(self, name, templates):
        '''
        Initialzes the object.

        @param <name>:
        The name of the node.

        @param <templates>:
        A tuple of possible template (names).
        '''

        super(TemplateContainer, self).__init__(name)
        self.templates = templates

    def generate_data(self, wiki_items, item_id):
        data = []

        # Loop through all valid children and generate the data for each
        # child.
        child_id, cookie = wiki_items.GetFirstChild(item_id)
        while child_id.IsOk():
            data.append(wiki_items.GetItemData(
                child_id).GetData().generate_data(wiki_items, child_id))
            child_id, cookie = wiki_items.GetNextChild(item_id, cookie)

        # Finally, join the result
        return '\n'.join(data)


class NonTemplate(TreePart):
    '''
    Represents a node that is not a container or template.
    '''

    def __init__(self, name):
        '''
        Initializes the object.

        @param <name>:
        The name of the node in the tree.
        '''

        super(NonTemplate, self).__init__(name)
        self.value = ''

    def generate_data(self, wiki_items, item_id):
        return self.value.strip()


class Template(OrderedDict, TreePart):
    '''
    Represents a full template in a tree.
    '''

    # NOTE:
    # Do not override __init__. It will break things (e.g copy module) even if
    # you use super().

    def generate_data(self, wiki_items, item_id):
        data = []

        # Loop through all valid children and generate the data for each
        # child.
        child_id, cookie = wiki_items.GetFirstChild(item_id)
        while child_id.IsOk():
            child = wiki_items.GetItemData(child_id).GetData()
            data.append('| {0}={1}'.format(child.name, child.generate_data(wiki_items, child_id)))
            child_id, cookie = wiki_items.GetNextChild(item_id, cookie)

        # Finally, join the result
        return '{{%s\n%s}}'% (self.name, '\n'.join(data))


class TemplateManager(dict):
    '''
    Manages all templates that where found in a given file.
    '''

    def __init__(self, file_path):
        '''
        Initialzes the object.

        @param <file_path>:
        The path to a file that contains the template data.
        '''

        for name, data in ConfigObj(file_path, file_error=True).items():
            template = Template()
            template.name = name
            for key, value in data.items():
                if value == 'str':
                    template[key] = NonTemplate(key)
                elif isinstance(value, list):
                    template[key] = TemplateContainer(key, tuple(value))
                else:
                    template[key] = TemplateContainer(key, (value,))

            self[name] = template

    def get_template(self, name):
        '''
        Returns the new template object for the given template name. If no
        template was found with the given name, a KeyError will be raised.

        @param <name>:
        The name of the template.
        '''

        return copy.deepcopy(self[name])