#!/usr/local/bin/python2
import wxversion
wxversion.select('3.0')
import wx
from wx.html import HtmlEasyPrinting


class MyPrintout(wxPrintout):
    
    def OnPrintPage(self, page):
        dc = self.GetDC()
        dc.BeginDrawing()
        text = 'Hello World'
        xPos = 150
        yPos = 300
        dc.DrawText(text, xPos, yPos)
        dc.EndDrawing()
        return true

class MyFrame(wxFrame):
    
    def __init__(self, parent=None, id=-1, title='Print01'):
        panel = wxPanel(self, -1)
        b1 = wxButton(panel, 10, 'Print')
        EVT_BUTTON(self, 10, self.OnPrint)
    
    
    def OnPrint(self, event):
        printer = wxPrinter()
        printout = MyPrintout()
        printer.Print(self, printout)  # self is the parent window
        printout.Destroy()

if __name__ == '__main__':
    ex = wx.App()
    MyFrame(None, 'Poetic Interpreter')
    ex.MainLoop ()

