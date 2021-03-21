import cv2
import numpy as np
import json
import os
import time
import multiprocessing

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty as op
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner, SpinnerOption

from kivy.clock import Clock

class MapWindow(TabbedPanelItem):
   pass

class WindowManager(TabbedPanel):
    test_list = []
    for i in range(0, 100):
        test_list.append(i+1)
        
class SpinnerConfig(SpinnerOption):
    pass

kvFile = Builder.load_file('MainFront.kv')

class GuiderApp(App):
    
    def build(self):
        self.WindowMan = WindowManager()
        return self.WindowMan

if __name__ == '__main__':
    # MapImage = cv2.imread('Map.jpg')

    # BlankColor = [0,0,0,0]
    # BlankImg = np.full((MapImage.shape[0], MapImage.shape[1], 4), BlankColor)

    GuiderApp().run()