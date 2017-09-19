from uptimism.graph_object import GraphObject
from uptimism.colors import Colors
from uptimism.images import Images
import os

class Padding():
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

class SocialPadding():
    RIGHT_COLUMN = Padding(300.0, 0.0, 0.0, 400.0)
    LEFT_COLUMN = Padding(300.0, 0.0, 0.0, -50.0)

class DataSet():
    def __init__(self, team, volume):
        self.team = team
        self.volume = volume
        self.img = None
        self.img_width = 0.0
        self.img_height = 0.0
        self.is_leader = False
        self.padding = SocialPadding.LEFT_COLUMN
    
    def set_img(self, img):
        self.img = img
        self.img_width = self.img.get_width()
        self.img_height = self.img.get_height()

class BarGraph(GraphObject):
    def __init__(self, data):
        super(BarGraph, self).__init__(data)
        self.yMax = None
        self.fCount = 10
        self.dataSets = self.process(data)
        self.initialize()
    
    def process(self, data):
        dataSets = {}
        leader = None

        for e in self.data:
            name, volume = e["team"], float(e["volume"])
            dataSets[name] = DataSet(name, volume)
            
            if volume > self.yMax or self.yMax is None:
                self.yMax = volume
                leader = name
        
        # do a series of padding sets for each bar graph I suppose? ehh
        dataSets[leader].is_leader = True
        dataSets[leader].padding = SocialPadding.RIGHT_COLUMN
        return dataSets

    def initialize(self):
        self.set_surface_as_img(Images.BG)
        # self.set_pen(0.005, Colors.BLACK)
        self.create()
    
    def reset(self):
        self.reset_bg(Images.BG)    

    def create(self):
        # for testing - need to come up with a plan for actual assigning
        images = [Images.SOCIAL_RED, Images.SOCIAL_BLUE]
        i = 0
        for dataSet in self.dataSets.values():
            dataSet.set_img(self.load_png(images[i]))
            i += 1
        
        # convert to list so that the image overlap has the right z-index=1
        dataSets = [d for d in self.dataSets.values()]
        dataSets.sort(key=lambda dataPoint: dataPoint.volume)
        
        #forward frames
        time_points = self.get_ease_out_curve(self.fCount)
        text_list = ["SWANS FANS WERE", "PUMPED ON SOCIAL", "MEDIA"]
        self.draw_frames(dataSets, time_points, text_list, True)

        # hover at peak
        for i in range(self.fCount):
            self.create_frame()    

        # reverse frames
        time_points.reverse()
        self.draw_frames(dataSets, time_points, text_list, False)
        
        # # make a test gif
        self.create_gif(self.fCount*2)

    def draw_frames(self, dataSets, time_points, text_list, forward):
        leftColumn = dataSets[0]
        rightColumn = dataSets[1]
        textLen = len(text_list)

        # i = 0
        # while i < 4:
            
        for i in range(self.fCount):
            t = time_points[i]
            for dataSet in dataSets:
                yOffset = dataSet.img_height * (1 - t) + dataSet.padding.top
                yOffset = yOffset + dataSet.img_height * (1 - dataSet.volume / self.yMax)
                xOffset = dataSet.img_width * (1 - t) + dataSet.padding.left
                xOffset = xOffset + dataSet.img_width * (1 - dataSet.volume / self.yMax)
                self.draw_img(dataSet.img, xOffset, yOffset)

            remaining = self.fCount - i
            
            if forward:
                if remaining <= textLen:
                    idx = textLen-remaining+1
                    print_list = text_list[:idx]
                    self.write_text(print_list)
                


            self.create_frame()

            if i < self.fCount-1:
                self.reset()