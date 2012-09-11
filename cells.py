# -*- coding: utf-8 -*-
import os, pygame, random, thread, time, signal, deamonize
from pygame.color import THECOLORS

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    cwd_save = os.getcwd()
    os.chdir("/")
    os.umask(0)
    os.setsid( )
    # Perform second fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush( )
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))
    os.chdir(cwd_save)



SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
MAX_SPEED = 20
RUNNING = True

class MyObject(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.xadd = 5
        self.yadd = 5
        self.rect = pygame.rect.Rect(self.x, self.y, 25, 25)
              
    def update(self):
        self.x += self.xadd
        self.y += self.yadd
        
        if (self.x >= SCREEN_WIDTH - self.rect.width):
            self.xadd = -random.randint(1, MAX_SPEED)
        
        if (self.x <= 0):
            self.xadd = random.randint(1, MAX_SPEED)
            
        if (self.y >= SCREEN_HEIGHT - self.rect.height):
            self.yadd = -random.randint(1, MAX_SPEED)
            
        if (self.y <= 0):
            self.yadd = random.randint(1, MAX_SPEED)
        
        self.rect.topleft = (self.x, self.y)

def display_worm_forever():
    x = random.randint(0, 1024 - SCREEN_WIDTH)
    y = random.randint(0, 800 - SCREEN_HEIGHT)
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(x) + ',' + str(y)
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

    clock = pygame.time.Clock()
    myObject = MyObject()        
    while RUNNING:
        clock.tick(100)
        myObject.update()    
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.color.THECOLORS['blue'], myObject.rect)
        pygame.display.update()
    print 'display thread terminated'

def signal_handler(signal, frame):
    global RUNNING
    RUNNING = False	

if __name__ == "__main__":
    # Uncomment to turn worm into a daemon
    deamonize.daemonize()

    os.putenv('DISPLAY', ':0') # Attach to local display
    signal.signal(signal.SIGINT, signal_handler) # CTRL+C
    signal.signal(signal.SIGTERM, signal_handler) # pkill
    thread.start_new_thread(display_worm_forever, ())
    
    while RUNNING:
        # TODO: Start implementing your worm here
        print 'running...'
        time.sleep(1)
    time.sleep(0.1); # Give display thread some time to terminate