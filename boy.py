from pico2d import load_image, get_time

from state_machine import StateMachine, space_down, time_out, right_down, left_up, right_up, left_down, start_event, \
    a_down


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0
        boy.frame = 0
        # 시작 시간 기록
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100,
                                          100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100,
                                          100)
        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
            boy.face_dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1
            boy.face_dir = -1

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Autorun:
    @staticmethod
    def enter(boy, e):
        boy.start_time = get_time()
        if boy.face_dir == 1:
            boy.action = 1
            boy.dir = 1
        elif boy.face_dir == -1:
            boy.action = 0
            boy.dir = -1

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.x >= 800:
            boy.dir = -1
            boy.action = 0
            boy.face_dir = -1
        elif boy.x <= 0:
            boy.dir = 1
            boy.action = 1
            boy.face_dir = 1

        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 7

        if get_time() - boy.start_time > 5:
            if boy.face_dir == 1:
                boy.action = 3
            elif boy.face_dir == -1:
                boy.action = 2
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+25, 150, 150)
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 상태머신인지 알려줄 필요
        self.state_machine.start(Idle) # 객체를 생성하지 않고 직접 Idle 클래스 사용
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Sleep, a_down: Autorun},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Autorun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle, a_down: Autorun},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트 종류, 값)
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()


