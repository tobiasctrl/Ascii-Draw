import pygame
import pygame.freetype

def CreateIMGList(widht, height):
    IMGList = [[0 for y in range(widht)] for x in range(height)]      
    return IMGList


class MainHandler:
    def __init__(self, width, height, surface):
        self.surface = surface
        self.height = height
        self.width = width
        self.Fields = CreateIMGList(width, height -2)
    def OnLeftClick(self,clickPosX, clickPosY):
        clickPosX = round(clickPosX/10 - 0.49)
        clickPosY = round(clickPosY/20 - 0.49)
        try:
            self.Fields[clickPosY][clickPosX] = 1
        except:
            pass
    def DrawSquares(self, Preview_Window):
        if Preview_Window == False:
            for y in range(self.height -2):
                for x in range(self.width):
                    val = self.Fields[y][x]
                    if val == 1:
                        pygame.draw.rect(self.surface,(0,0,0),(x*10, y*20, 10, 20))

    def OnRightClick(self, clickPosX, clickPosY):
        clickPosX = round(clickPosX/10 - 0.49)
        clickPosY = round(clickPosY/20 - 0.49)
        try:
            self.Fields[clickPosY][clickPosX] = 0
        except:
            pass
    def MakeToolbar(self):
        pygame.draw.rect(self.surface,(150,150,150),(0,self.height *20- 40 , self.width * 10, self.height*20))
    def Reset(self):
        self.Fields = CreateIMGList(self.width, self.height -2)
    def Preview(self):
        font = pygame.freetype.Font(None,20)
        for y in range(self.height -2):
            for x in range(self.width):
                val = self.Fields[y][x]
                if val == 1:
                    font.render_to(self.surface,(x * 10,y * 20),"#")
                else:
                    font.render_to(self.surface,(x * 10,y * 20),"/")
    def Save(self, FileName):
        file = open(FileName, "w")
        LineString = ""
        for y in range(self.height -2):
            for x in range(self.width):
                val = self.Fields[y][x]
                if val == 1:
                    LineString += "#"
                else:
                    LineString += "/"
            file.write(LineString + "\n")
            LineString = ""
        file.close()
            
class Button:
    def __init__(self, surface, color, pos):
        self.surface = surface
        self.color = color #the current button color
        self.btnColor = color #generally Button color
        self.pos = pos
        self.MouseUp = False
    def OnClick(self, ClickColor):
        Hover = False
        Mpos = pygame.mouse.get_pos()
        if Mpos[0] >= self.pos[0] and Mpos[0] <= self.pos[0] + self.pos[2] and Mpos[1] >= self.pos[1] and Mpos[1] <= self.pos[1] + self.pos[3]:
            Hover = True
        LeftMouseState = pygame.mouse.get_pressed()[0]
        if LeftMouseState == True and Hover == False:
            self.MouseUp = False
        if LeftMouseState == False and Hover == True:
            self.MouseUp = True
        if Hover == True and LeftMouseState == True:
            self.color = ClickColor
        else:
            self.color = self.btnColor
        if Hover == True and LeftMouseState == True and self.MouseUp == True:
            self.MouseUp = False
            return True
        else:
            return False
    def Text(self, text, TextSize, TposX):
        self.font = pygame.freetype.Font(None,TextSize)
        self.text = text
        self.TposX = self.pos[0] + TposX
        self.TposY = self.pos[1] + round((self.pos[3] - TextSize) / 2)
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.pos)
        self.font.render_to(self.surface,(self.TposX,self.TposY),self.text)
        pygame.draw.rect(self.surface, (0,0,0), self.pos, 1)

def InputWH_to_pixel(width, height):
    return width * 10 ,height * 20


def Create(width, height, FileName):
    width1, height1 = InputWH_to_pixel(width, height)
    pygame.init()
    pygame.display.set_caption('Ascii Draw')
    screen = pygame.display.set_mode((width1, height1))
    c = MainHandler(width, height, screen)
    done = False
    pos = (0,0)
    LeftMousedown = False
    RightMousedown = False
    Reset = Button(screen,(170, 30, 30), (0,height1 -40, 120, 40))
    Reset.Text("Reset", 22, 10)
    b2 = Button(screen,(30,30,170),(width1 - 180, height1 - 40 , 120 ,40))
    b2.Text("Preview", 22, 5)
    b = Button(screen,(30,170,30),(width1 - 60, height1 - 40, 60, 40))
    b.Text("Save", 22, 5)
    Preview_Window = False
    while not done:
        Reset_state = Reset.OnClick((255,0,0))
        if Reset_state == True:
            c.Reset()
        Preview_State = b2.OnClick((0,0,255))
        Save_State = b.OnClick((0,255,0))
        screen.fill((255,255,255))
        if Save_State == True:
            c.Save(FileName)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LeftMousedown = True
                elif event.button == 3:
                    RightMousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LeftMousedown = False
                elif event.button == 3:
                    RightMousedown = False
        if LeftMousedown:
            pos = pygame.mouse.get_pos()
            c.OnLeftClick(pos[0], pos[1])
        if RightMousedown:
            pos = pygame.mouse.get_pos()
            c.OnRightClick(pos[0], pos[1])
        if Preview_State == True:
            if Preview_Window:
                Preview_Window = False
            else:
                Preview_Window = True
        if Preview_Window == True:
            c.Preview()
        c.MakeToolbar()
        c.DrawSquares(Preview_Window)
        b2.draw()
        b.draw()
        Reset.draw()
        
        pygame.display.flip()

width = int(input("width: "))
height = int(input("height: "))
FileName = input("Filename: ")
Create(width, height, FileName)