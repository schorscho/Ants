import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from ants import World

#------------------------------------------------------------
# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-250, 250), ylim=(-250, 250))

# anties holds the locations of the anties
anties, = ax.plot([], [], 'bo', ms=6)

world = World()
world.place_food(0.5)

# rect is the box edge
rect = plt.Rectangle((-200 , -200),
                     400,
                     400,
                     ec='none', lw=2, fc='none')
ax.add_patch(rect)

def init():
    """initialize animation"""
    global rect
    anties.set_data([], [])
    rect.set_edgecolor('none')
    return anties, rect

def animate(i):
    """perform animation step"""
    global world, rect, ax, fig
    
    world.add_ants(1)
    world.move_ants()

    ms = int(fig.dpi * 2 * 0.04 * fig.get_figwidth() / np.diff(ax.get_xbound())[0])
    ms = 1
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    positions = []
    
    for key in world.get_ant_dict().keys():
        positions.append([key[0], key[1]])

    positions = np.asarray(positions)
    
    anties.set_data(positions[:, 0], positions[:, 1])
    anties.set_markersize(ms)
    
    return anties, rect

ani = animation.FuncAnimation(fig, animate, frames=2000,
                              interval=10, blit=True, init_func=init)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

#HTML(ani.to_html5_video())