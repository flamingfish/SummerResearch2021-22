def panFactory(ax):
    cur_xlim = None
    cur_ylim = None
    xpress = None
    ypress = None
    pressed = False
    def onPress(event):
        nonlocal cur_xlim, cur_ylim, xpress, ypress, pressed
        if event.inaxes != ax: return
        #print('pressed')
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xpress = event.xdata
        ypress = event.ydata
        pressed = True

    def onRelease(event):
        nonlocal pressed
        #print('released')
        pressed = False
        ax.figure.canvas.draw()

    def onMotion(event):
        nonlocal cur_xlim, cur_ylim
        if not pressed: return
        if event.inaxes != ax: return
        #print('moving')
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        cur_xlim -= dx
        cur_ylim -= dy
        ax.set_ylim(cur_ylim)
        ax.set_xlim(cur_xlim)

        ax.figure.canvas.draw()

    fig = ax.get_figure() # get the figure of interest

    # attach the call back
    fig.canvas.mpl_connect('button_press_event', onPress)
    fig.canvas.mpl_connect('button_release_event', onRelease)
    fig.canvas.mpl_connect('motion_notify_event', onMotion)

    #return the function
    return onMotion