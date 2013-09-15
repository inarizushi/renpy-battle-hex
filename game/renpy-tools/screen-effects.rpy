# Store effects to be used on the screen

init python:
    
        import math
        
        #The Pheonix Wright style screen shake!
        class Shaker(object):
        
            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
        
            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child
                
            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.                
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor
                
                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)
        
        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)
        
            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)
        
    #

#

init python:
    sshake = Shake((0, 0, 0, 0), 0.5, dist=10)
    mshake = Shake((0, 0, 0, 0), 1.0, dist=15)
    bshake = Shake((0, 0, 0, 0), 2.0, dist=20)
    
    def bop_time_warp(x):
      return -23.0 * x**5 + 57.5 * x**4 - 55 * x**3 + 25 * x**2 - 3.5 * x
      
    ballMove = Move((0.25, 0.5), (0.75, 0.5), 1.0, time_warp=bop_time_warp, xanchor="center", yanchor="center")
#