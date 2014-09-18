# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"WikiEditor", pos = wx.DefaultPosition, size = wx.Size( 522,385 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.wiki_items = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_SINGLE )
		bSizer1.Add( self.wiki_items, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.output = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer1.Add( self.output, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.menubar = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.new_project = wx.MenuItem( self.file_menu, wx.ID_ANY, u"New Project"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.new_project )
		
		self.open_file = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Open.."+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.open_file )
		
		self.save_file = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_file )
		
		self.save_file_as = wx.MenuItem( self.file_menu, wx.ID_ANY, u"Save as..."+ u"\t" + u"Ctrl-Shift+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.AppendItem( self.save_file_as )
		
		self.menubar.Append( self.file_menu, u"File" ) 
		
		self.SetMenuBar( self.menubar )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.wiki_items.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.on_wiki_item_activated )
		self.wiki_items.Bind( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_wiki_items_right_click )
		self.wiki_items.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_wiki_item_selection )
		self.Bind( wx.EVT_MENU, self.on_new_project, id = self.new_project.GetId() )
		self.Bind( wx.EVT_MENU, self.on_open_file, id = self.open_file.GetId() )
		self.Bind( wx.EVT_MENU, self.on_save_file, id = self.save_file.GetId() )
		self.Bind( wx.EVT_MENU, self.on_save_file_as, id = self.save_file_as.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_wiki_item_activated( self, event ):
		event.Skip()
	
	def on_wiki_items_right_click( self, event ):
		event.Skip()
	
	def on_wiki_item_selection( self, event ):
		event.Skip()
	
	def on_new_project( self, event ):
		event.Skip()
	
	def on_open_file( self, event ):
		event.Skip()
	
	def on_save_file( self, event ):
		event.Skip()
	
	def on_save_file_as( self, event ):
		event.Skip()
	

###########################################################################
## Class NewProjectDialog
###########################################################################

class NewProjectDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"New Project", pos = wx.DefaultPosition, size = wx.Size( 278,172 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		project_typeChoices = [ u"Package", u"Module" ]
		self.project_type = wx.RadioBox( self, wx.ID_ANY, u"Project Type", wx.DefaultPosition, wx.DefaultSize, project_typeChoices, 1, wx.RA_SPECIFY_COLS )
		self.project_type.SetSelection( 0 )
		bSizer2.Add( self.project_type, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.ok, 0, wx.ALL, 5 )
		
		
		bSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.cancel, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class SingleItemEditDialog
###########################################################################

class SingleItemEditDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit", pos = wx.DefaultPosition, size = wx.Size( 549,266 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.input_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer4.Add( self.input_box, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.ok, 0, wx.ALL, 5 )
		
		
		bSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.cancel, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class ChooseTemplateDialog
###########################################################################

class ChooseTemplateDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Choose a template", pos = wx.DefaultPosition, size = wx.Size( 207,98 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		templateChoices = []
		self.template = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, templateChoices, wx.CB_SORT )
		self.template.SetSelection( 0 )
		bSizer6.Add( self.template, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.ok = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.ok, 0, wx.ALL, 5 )
		
		self.cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.cancel, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

