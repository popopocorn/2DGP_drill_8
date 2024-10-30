from math import radians
from pico2d import *
from state_machine import *

class Idle:
    @staticmethod # @ - decorator, 함수의 기능 변경 멤버함수의 개념 X
    def enter(obj, e):
        obj.dx=0
        if obj.dir >= 0:
            obj.action = 3
        else:
            obj.action = 2
        obj.frame = 0
        obj.start_time = get_time()
    @staticmethod
    def exit(obj):
        pass
    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 8
        if get_time() - obj.start_time > 3:
            obj.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(obj.frame * 100, obj.action * 100, 100, 100, obj.x, obj.y)

class Sleep:
    @staticmethod  # @ - decorator, 함수의 기능 변경 멤버함수의 개념 X
    def enter(obj, e):
        obj.frame = 0

    @staticmethod
    def exit(obj):
        pass

    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 8

    @staticmethod
    def draw(obj):
        if obj.dir >= 0:
            obj.image.clip_composite_draw(obj.frame * 100, 3 * 100, 100, 100, radians(90), '',obj.x - 25, obj.y - 25, 100, 100)
        else:
            obj.image.clip_composite_draw(obj.frame * 100, 2 * 100, 100, 100, radians(-90), '', obj.x + 25,
                                          obj.y - 25, 100, 100)
class Run:
    @staticmethod
    def enter(obj, e):
        if right_down(e) or left_up(e):
            obj.dir = 1
            obj.dx = 1
            obj.action = 1
            obj.frame = 0
        elif left_down(e) or right_up(e):
            obj.dx = -1
            obj.dir = -1
            obj.action = 0
            obj.frame = 0

    @staticmethod
    def exit(obj):

        pass
    @staticmethod
    def do(obj):
        obj.x += obj.dx * 5
        obj.frame = (obj.frame + 1) % 8
        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw(obj.frame * 100, obj.action * 100, 100, 100, obj.x, obj.y)
        pass
class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.dx = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Run : {right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle},
                Idle : {right_down: Run, left_down : Run, left_up : Run, right_up : Run,time_out : Sleep},
                Sleep : {right_down : Run, left_down: Run, right_up: Run, left_up : Run, space_down : Idle},

            }
        )
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #이건 key, mouse 입력
        #하지만 tuple형식으로 넘겨줘야함
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
