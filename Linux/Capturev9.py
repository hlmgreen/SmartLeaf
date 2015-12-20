__author__ = 'mark greenwood'
import wx
import time
import pygame
import pygame.camera
import os

# initialises connected devices
pygame.camera.init()
camList = pygame.camera.list_cameras()


class MyApp(wx.App):
    """Builds the main GUI application"""
    def OnInit(self):
        self.frame = MyFrame()
        self.SetTopWindow(self.frame)
        self.frame.CenterOnScreen()
        self.frame.Show()
        return True


class StreamWindow(wx.Frame):
    """Builds a window for displaying a camera test stream upon selection of test button"""
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title="Test", size=(1280, 720), style=wx.DEFAULT_FRAME_STYLE)
        wx.Frame.CenterOnScreen(self)
        self.panel = wx.Panel(self)

    def draw(self, selection):
        """Blits images to the window and draws grid lines on top of each one. Grid lines correspond to area for
        cropping in tracking so plants must fit within."""
        cam = pygame.camera.Camera(selection, (1280, 720))  # gets selected camera
        self.Bind(wx.EVT_CLOSE, self.close_stream)  # binds close event to X button
        try:
            cam.start()
            self.run = True
            while self.run == True:
                    img = cam.get_image()
                    pygame.draw.lines(img, (0, 0, 0), False, [[130, 20], [1150, 20], [1150, 700], [130, 700], [130, 20]], 2)
                    pygame.draw.lines(img, (0, 0, 0), False, [[334, 20], [334, 700], [538, 700], [538, 20], [742, 20],
                                                              [742, 700], [946, 700], [946, 20]], 2)
                    pygame.draw.lines(img, (0, 0, 0), False, [[130, 247], [1150, 247], [1150, 474], [130, 474]], 2)
                    img = pygame.image.tostring(img, "RGB", False) #converts to cross package format
                    bitmap = wx.BitmapFromBuffer(1280, 720, img)  #convert to bitmap for display
                    self.bitmap = wx.StaticBitmap(self.panel, bitmap=bitmap)
                    self.Update()
                    self.Show()
                    wx.Yield()

            cam.stop()
            self.Destroy()  # stop cam and then close window

        except SystemError:
            print "Please select a camera"
            self.Destroy()

    def close_stream(self, event):
        """Close stream event- breaks the loop on click of X button"""
        self.run = False


class MyFrame(wx.Frame):
    """Builds the main GUI frame containing all the input selections and events"""
    def __init__(self):
        super(MyFrame, self).__init__(None, id=wx.ID_ANY, title="Image Capture", size=(1000, 600),
                                      name="MyFrame")

        #Creates the panel to sit inside the main window
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.WHITE)

        #Camera 1 inputs
        text_box1 = wx.StaticText(self.panel, label="Plate 1", pos=(5, 30))
        self.combo_box1 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 25))
        test_button1 = wx.Button(self.panel, label="Test camera", pos=(285, 25), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click, test_button1)

        #Camera 2
        text_box2 = wx.StaticText(self.panel, label="Plate 2", pos=(5, 65))
        self.combo_box2 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 60))
        test_button2 = wx.Button(self.panel, label="Test camera", pos=(285, 60), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click2, test_button2)

        #cam 3
        text_box3 = wx.StaticText(self.panel, label="Plate 3", pos=(5, 100))
        self.combo_box3 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 95))
        test_button3 = wx.Button(self.panel, label="Test camera", pos=(285, 95), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click3, test_button3)

        #cam 4
        text_box4 = wx.StaticText(self.panel, label="Plate 4", pos=(5, 135))
        self.combo_box4 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 130))
        test_button4 = wx.Button(self.panel, label="Test camera", pos=(285, 130), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click4, test_button4)

        #cam 5
        text_box5 = wx.StaticText(self.panel, label="Plate 5", pos=(5, 170))
        self.combo_box5 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 165))
        test_button5 = wx.Button(self.panel, label="Test camera", pos=(285, 165), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click5, test_button5)

        #cam 6
        text_box6 = wx.StaticText(self.panel, label="Plate 6", pos=(5, 205))
        self.combo_box6 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 200))
        test_button6 = wx.Button(self.panel, label="Test camera", pos=(285, 200), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click6, test_button6)

        #cam 7
        text_box7 = wx.StaticText(self.panel, label="Plate 7", pos=(5, 240))
        self.combo_box7 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 235))
        test_button7 = wx.Button(self.panel, label="Test camera", pos=(285, 235), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click7, test_button7)

        #cam 8
        text_box8 = wx.StaticText(self.panel, label="Plate 8", pos=(5, 275))
        self.combo_box8 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos=(80, 270))
        test_button8 = wx.Button(self.panel, label="Test camera", pos=(285, 270), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click8, test_button8)

        #cam 9
        text_box9 = wx.StaticText(self.panel, label="Plate 9", pos=(500, 30))
        self.combo_box9 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                      style=wx.CB_DROPDOWN, pos= (575, 25))
        test_button9 = wx.Button(self.panel, label="Test camera", pos=(780, 25), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click9, test_button9)

        #cam 10
        text_box10 = wx.StaticText(self.panel, label="Plate 10", pos=(500, 65))
        self.combo_box10 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 60))
        test_button10 = wx.Button(self.panel, label="Test camera", pos=(780, 60), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click10, test_button10)

        #cam 11
        text_box11 = wx.StaticText(self.panel, label="Plate 11", pos=(500, 100))
        self.combo_box11 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 95))
        test_button11 = wx.Button(self.panel, label="Test camera", pos=(780, 95), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click11, test_button11)

        #cam 12
        text_box12 = wx.StaticText(self.panel, label="Plate 12", pos=(500, 135))
        self.combo_box12 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 130))
        test_button12 = wx.Button(self.panel, label="Test camera", pos=(780, 130), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click12, test_button12)

        #cam 13
        text_box13 = wx.StaticText(self.panel, label="Plate 13", pos=(500, 170))
        self.combo_box13 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 165))
        test_button13 = wx.Button(self.panel, label="Test camera", pos=(780, 165), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click13, test_button13)

        #cam 14
        text_box14 = wx.StaticText(self.panel, label="Plate 14", pos=(500, 205))
        self.combo_box14 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 200))
        test_button14 = wx.Button(self.panel, label="Test camera", pos=(780, 200), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click14, test_button14)

        #cam 15
        text_box15 = wx.StaticText(self.panel, label="Plate 15", pos=(500, 240))
        self.combo_box15 = wx.ComboBox(self.panel, value='Select camera', choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 235))
        test_button15 = wx.Button(self.panel, label="Test camera", pos=(780, 235), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click15, test_button15)

        #cam 16
        text_box16 = wx.StaticText(self.panel, label="Plate 16", pos=(500, 275))
        self.combo_box16 = wx.ComboBox(self.panel,value='Select camera',  choices=['Select camera'] + camList,
                                       style=wx.CB_DROPDOWN, pos=(575, 270))
        test_button16 = wx.Button(self.panel, label="Test camera", pos=(780, 270), size=(150, 28))
        self.Bind(wx.EVT_BUTTON, self.on_click16, test_button16)

        #Time data, run button and save path
        save_dialog = wx.StaticText(self.panel, label='Save directory', pos=(400, 325))
        save_button = wx.Button(self.panel, label='....', pos=(510, 320), size=(80,28))
        self.Bind(wx.EVT_BUTTON, self.on_click18, save_button)

        time_text = wx.StaticText(self.panel, label="Time Interval (s)", pos=(400, 352))
        self.time_input = wx.TextCtrl(self.panel, pos=(510, 350))

        cycle_text = wx.StaticText(self.panel, label="Cycles", pos=(400, 382))
        self.cycle_input = wx.TextCtrl(self.panel, pos=(510, 380))

        run_button = wx.Button(self.panel, -1, size=(190, 30), pos=(400, 415), label='Run Program')
        self.Bind(wx.EVT_BUTTON, self.on_click17, run_button)

        #error/progress text box
        self.error_box_text = wx.TextCtrl(self.panel, value='', size=(990, 120), pos=(5, 475),
                                          style = wx.TE_READONLY + wx.TE_MULTILINE)

        self.gauge = wx.Gauge(self.panel, size=(990, 20), pos=(5, 450))

    #events - converts drop down camera selection to string which is passed to the stream window.
    def on_click(self, event):
        selection = self.combo_box1.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click2(self, event):
        selection = self.combo_box2.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click3(self, event):
        selection = self.combo_box3.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click4(self, event):
        selection = self.combo_box4.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click5(self, event):
        selection = self.combo_box5.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click6(self, event):
        selection = self.combo_box6.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click7(self, event):
        selection = self.combo_box7.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click8(self, event):
        selection = self.combo_box8.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click9(self, event):
        selection = self.combo_box9.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click10(self, event):
        selection = self.combo_box10.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click11(self, event):
        selection = self.combo_box11.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click12(self, event):
        selection = self.combo_box12.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click13(self, event):
        selection = self.combo_box13.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click14(self, event):
        selection = self.combo_box14.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click15(self, event):
        selection = self.combo_box15.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click16(self, event):
        selection = self.combo_box16.GetStringSelection()
        stream_w = StreamWindow(parent=None, id=-1)
        stream_w.draw(selection)

    def on_click18(self, event):
        self.save_dlg = wx.DirDialog(self, 'Choose or create a directory for your test', defaultPath=os.getcwd(),
                                     style=wx.DD_CHANGE_DIR)
        self.save_dlg.ShowModal()

    def camerasnp(self, cam, save_as):
        """This capture an image and saves it, cam is the name of the device, saveas is the name to save document as"""
        pygame.camera.init()
        cam = pygame.camera.Camera(cam, (1920, 1080))  # change to cam resolution
        cam.start()
        img = cam.get_image()
        pygame.image.save(img, save_as)  # saves image
        cam.stop()

    def timelapser(self, time_sec, loops, matrix, save_dlg):
        """Runs time-lapse with measured time between each cycle"""
        print 'Time interval = %s' % time_sec
        print 'Number of intervals = %s' % loops
        counter = 0

        keys = matrix.keys()
        keys.sort()
        self.error_box_text.WriteText('Running %s loops at %s seconds intervals' % (str(loops), time_sec))
        wx.Yield()  # pauses the process momentarily to update text box

        while counter < loops:
            old_time = time.time()
            text = 'Running loop %s' % counter
            print text
            self.error_box_text.WriteText('\n%s' % text)  # updates with loop number
            self.gauge.SetValue(counter)  # updates progress bar
            wx.Yield()
            counter += 1

            for cam_shoot in keys:
                if matrix[cam_shoot] == "":
                    continue
                else:
                    for snap in range(0, 3):  # takes 3 images at each time point 
                        self.camerasnp(matrix[cam_shoot], '%s/Plate%s-%s-c%s.png' % (save_dlg, cam_shoot, counter, snap))

            new_time = time.time()
            time.sleep(time_sec-(new_time-old_time))

    def on_click17(self, event):
        """Main run event - gets selected inputs and then return error messages if invalid else runs program"""
        try:
            all_selected_cameras = {1: (self.combo_box1.GetStringSelection()),
                                    2: (self.combo_box2.GetStringSelection()),
                                    3: (self.combo_box3.GetStringSelection()),
                                    4: (self.combo_box4.GetStringSelection()),
                                    5: (self.combo_box5.GetStringSelection()),
                                    6: (self.combo_box6.GetStringSelection()),
                                    7: (self.combo_box7.GetStringSelection()),
                                    8: (self.combo_box8.GetStringSelection()),
                                    9: (self.combo_box9.GetStringSelection()),
                                    10: (self.combo_box10.GetStringSelection()),
                                    11: (self.combo_box11.GetStringSelection()),
                                    12: (self.combo_box12.GetStringSelection()),
                                    13: (self.combo_box13.GetStringSelection()),
                                    14: (self.combo_box14.GetStringSelection()),
                                    15: (self.combo_box15.GetStringSelection()),
                                    16: (self.combo_box16.GetStringSelection())}

            run_time = float(self.time_input.GetValue())
            loops = float(self.cycle_input.GetValue())
            save_dlg = self.save_dlg.GetPath()

            self.gauge.SetRange(loops-1)  # sets progress gauge max

            #error handling - checks if inputs are valid
            for key, value in all_selected_cameras.items():  # if somebody clicks 'sel camera' it changes to empty string
                if value == 'Select camera':
                    all_selected_cameras[key] = ''

            if all(val == '' for val in all_selected_cameras.values()):  # prints an error if no cam is selected
                self.error_box_text.WriteText('Please select a camera\n')

            if run_time < 60:  # this prevents errors where time taken for images is longer than interval
                self.error_box_text.WriteText('Error - please select a longer interval')

            #if inputs are valid program is run
            else:
                self.error_box_text.WriteText('Saving to %s\n' % save_dlg)
                self.timelapser(run_time, loops, all_selected_cameras, save_dlg)
                complete_dialog = wx.MessageDialog(None, message="Image capture complete",
                                                   style=wx.OK + wx.ID_JUSTIFY_CENTER + wx.ICON_INFORMATION)
                complete_dialog.ShowModal()

        except(ValueError, AttributeError):
            self.error_box_text.WriteText('Error: please select all parameters\n')


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
