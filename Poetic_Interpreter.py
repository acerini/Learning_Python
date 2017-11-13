#!/usr/bin/python
import wx
from wx.html import HtmlEasyPrinting

FONTSIZE = 10

class TextDocPrintout(wx.Printout):
    """
        A printout class that is able to print simple text documents.
        Does not handle page numbers or titles, and it assumes that no
        lines are longer than what will fit within the page width.  Those
        features are left as an exercise for the reader. ;-)
        """
    def __init__(self, text, title, margins):
        wx.Printout.__init__(self, title)
        self.lines = text.split('\n')
        self.margins = margins
    
    
    def HasPage(self, page):
        return page <= self.numPages
    
    def GetPageInfo(self):
        return (1, self.numPages, 1, self.numPages)
    
    
    def CalculateScale(self, dc):
        # Scale the DC such that the printout is roughly the same as
        # the screen scaling.
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX)/float(ppiScreenX)
        
        # Now adjust if the real page size is reduced (such as when
        # drawing on a scaled wx.MemoryDC in the Print Preview.)  If
        # page width == DC width then nothing changes, otherwise we
        # scale down for the DC.
        pw, ph = self.GetPageSizePixels()
        dw, dh = dc.GetSize()
        scale = logScale * float(dw)/float(pw)
        
        # Set the DC's scale.
        dc.SetUserScale(scale, scale)
        
        # Find the logical units per millimeter (for calculating the
        # margins)
        self.logUnitsMM = float(ppiPrinterX)/(logScale*25.4)
    
    
    def CalculateLayout(self, dc):
        # Determine the position of the margins and the
        # page/line height
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM
        self.y1 = topLeft.y * self.logUnitsMM
        self.x2 = dc.DeviceToLogicalXRel(dw) - bottomRight.x * self.logUnitsMM
        self.y2 = dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM
        
        # use a 1mm buffer around the inside of the box, and a few
        # pixels between each line
        self.pageHeight = self.y2 - self.y1 - 2*self.logUnitsMM
        font = wx.Font(FONTSIZE, wx.TELETYPE, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        self.lineHeight = dc.GetCharHeight()
        self.linesPerPage = int(self.pageHeight/self.lineHeight)
    
    
    def OnPreparePrinting(self):
        # calculate the number of pages
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        self.numPages = len(self.lines) / self.linesPerPage
        if len(self.lines) % self.linesPerPage != 0:
            self.numPages += 1


    def OnPrintPage(self, page):
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
    
        # draw a page outline at the margin points
        dc.SetPen(wx.Pen("black", 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        r = wx.RectPP((self.x1, self.y1),
                      (self.x2, self.y2))
        dc.DrawRectangleRect(r)
        dc.SetClippingRect(r)
                      
        # Draw the text lines for this page
        line = (page-1) * self.linesPerPage
        x = self.x1 + self.logUnitsMM
        y = self.y1 + self.logUnitsMM
        while line < (page * self.linesPerPage):
            dc.DrawText(self.lines[line], x, y)
            y += self.lineHeight
            line += 1
            if line >= len(self.lines):
                break
        return True




class Interpret(wx.Frame):
    
    def __init__(self, parent, title):
        super(Interpret, self).__init__(parent, title=title,
                                      size=(460, 470))
    
        self.InitUI()
        self.Centre()
        self.Show()
    
    
    def InitUI(self):
        panel = wx.Panel(self)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        background = wx.StaticText(panel, style=wx.TE_MULTILINE, label='#!/usr/bin/python\n# -*- coding: utf-8 -*-\n# absolute.py\nimport wx \nclass Example(wx.Frame): \ndef __init__(self, parent, title):\nsuper(Example, self).__init__(parent, title=title,\nsize=(390, 350))\n self.InitUI()\nself.Centre()\nself.Show()\ndef InitUI(self):\n\npanel = wx.Panel(self)\n\n\nvbox = wx.BoxSizer(wx.VERTICAL)\n\
                              hbox1 = wx.BoxSizer(wx.HORIZONTAL)\nst1 = wx.StaticText(panel, label=Author Name)\n\nhbox1.Add(st1, flag=wx.RIGHT, border=8)\ntc = wx.TextCtrl(panel)\nhbox1.Add(tc, proportion=1)\nvbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)\n\
                              \nvbox.Add((-1, 10))\n\nhbox2 = wx.BoxSizer(wx.HORIZONTAL)\nst2 = wx.StaticText(panel, label=Poem)\nhbox2.Add(st2)\nvbox.Add(hbox2, flag=wx.LEFT|wx.TOP, border=10)\n\nvbox.Add((-1, 10))\n\nhbox3 = wx.BoxSizer(wx.HORIZONTAL)\ntc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)\nhbox3.Add(tc2, proportion=1, flag=wx.EXPAND)\nvbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)\n\nvbox.Add((-1,25))\n\n hbox4 = wx.BoxSizer(wx.HORIZONTAL)\ncb1 = wx.CheckBox(panel, label=Visual_Encode)\n\n hbox4.Add(cb1)\ncb2 = wx.CheckBox(panel, label=Translate)\n\nhbox4.Add(cb2, flag=wx.LEFT, border=10)\n\
                              cb3 = wx.CheckBox(panel, label = Input)\n\nhbox4.Add(cb3, flag=wx.LEFT, border=10)\nvbox.Add(hbox4, flag=wx.LEFT, border=10)\n\nvbox.Add((-1, 25))\n\nhbox5 = wx.BoxSizer(wx.HORIZONTAL)\nbtn1 = wx.Button(panel, label=Interpret, size=(70, 30))\n\
                              hbox5.Add(btn1)\nbtn2 = wx.Button(panel, label=Close, size=(70,30))\nhbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)\nvbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)\n\npanel.SetSizer(vbox)\n\n\nif __name__ == __main__:\n \napp = wx.App()\n Example(None, title=Poetic Interpreter)\napp.MainLoop()')
       
        background.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        background.SetForegroundColour(wx.Colour(255,255,255,100))
        
        
        vbox.Add((-1, 0))
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        titletxt = wx.StaticText(panel, label='POETIC INTERPRETER...')
        
        hbox2.Add(titletxt)
        vbox.Add(hbox2, flag=wx.LEFT|wx.TOP,  border=35)
        
        titletxt.SetFont(wx.Font(36, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        
        
        
        vbox.Add((-1, 35))
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        poet = wx.StaticText(panel, label='Poet:  ')
        self.author = wx.TextCtrl(panel)
        
        hbox3.Add(poet, flag=wx.RIGHT, border=8)
        hbox3.Add(self.author, proportion=1)
    
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=35)
        self.author.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        self.author.SetForegroundColour(wx.Colour(0,142,117))
        poet.SetFont(wx.Font(17, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))

        vbox.Add((-1, 15))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        ptitle = wx.StaticText(panel, label='Title:')
        self.filename = wx.TextCtrl(panel)
        
        hbox4.Add(ptitle, flag=wx.RIGHT, border=8)
        hbox4.Add(self.filename, proportion=1)
        
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=35)
        self.filename.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        self.filename.SetForegroundColour(wx.Colour(0,142,117))
        ptitle.SetFont(wx.Font(17, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        
        vbox.Add((-1, 30))
        
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.TextCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox6.Add(self.TextCtrl, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox6, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=35)
        self.TextCtrl.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        
        vbox.Add((-1, 0))
        
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Interpret', size=(100, 80))
        hbox5.Add(btn1)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=35)
        btn1.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'MONO-RGO MODULAR'))
        btn1.SetForegroundColour('blue')

        btn1.Bind( wx.EVT_BUTTON, self.onPrint)
     
        panel.SetSizer(vbox)
        panel.SetBackgroundColour(wx.Colour(0,142,117))

        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_LETTER)
        self.pdata.SetOrientation(wx.PORTRAIT)
        self.margins = (wx.Point(15,15), wx.Point(15,15))
        self.numPage = (1)
    
    def onGetData(self, evt=None):
        print("get data button pressed")
        author = self.author.Value
        ptitle = self.filename.Value
        contents = self.TextCtrl.Value
        print(author)
        print(ptitle)
        print(contents)
    
    
    def onPrint(self, evt=None):
        data = wx.PrintDialogData(self.pdata)
        printer = wx.Printer(data)
        text = self.TextCtrl.GetValue()
        printout = TextDocPrintout(text, "title", self.margins)
        useSetupDialog = True
        if not printer.Print(self, printout, useSetupDialog) \
            and printer.GetLastError() == wx.PRINTER_ERROR:
                wx.MessageBox(
                              "There was a problem printing.\n"
                              "Perhaps your current printer is not set correctly?",
                              "Printing Error", wx.OK)
        else:
            data = printer.GetPrintDialogData()
            self.pdata = wx.PrintData(data.GetPrintData()) # force a copy
        printout.Destroy()



if __name__ == '__main__':
    ex = wx.App()
    Interpret(None, 'Poetic Interpreter')
    ex.MainLoop ()
