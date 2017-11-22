import numpy as np
import matplotlib.pyplot as plt


def plot_line_shaded_std(x, y, std_y, horizontal=True,
                         ax=None,
                         line_kwargs=dict(),
                         fill_kwargs=dict()):
    """Plot wrapper to draw line for y and shaded patch according to std_y """
    line_defaults = {}

    # Set plot defaults into the kwargs
    if not ax:
        ax = plt.gca()

    # Apply defaults but respect input
    line_defaults.update(line_kwargs)

    if horizontal:
        p = ax.plot(x, y, **line_defaults)
    else:
        p = ax.plot(y, x, **line_defaults)

    fill_defaults = {'color': p[-1].get_color(),
                     'alpha': 0.35}

    # Apply defaults but respect input
    fill_defaults.update(fill_kwargs)

    if horizontal:
        ax.fill_between(x, y-std_y, y+std_y, **fill_defaults)
    else:
        ax.fill_betweenx(x, y-std_y, y+std_y, **fill_defaults)


def box_plot(box, **kwargs):
    """plots box despite coordinate discontinuities.
    INPUT
    -----
    box: np.array
        Defines the box in the coordinates of the current axis.
        Describing the box corners [x1, x2, y1, y2]
    kwargs: optional
        anything that can be passed to plot can be put as kwarg
    """

    if len(box) != 4:
        raise RuntimeError("'box' must be a 4 element np.array, \
            describing the box corners [x1, x2, y1, y2]")
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()
    x_split = False
    y_split = False

    if np.diff([box[0], box[1]]) < 0:
        x_split = True

    if np.diff([box[2], box[3]]) < 0:
        y_split = True

    if y_split and not x_split:
        plt.plot([box[0], box[0], box[1], box[1], box[0]],
                 [ylim[1], box[2], box[2], ylim[1], ylim[1]], **kwargs)

        plt.plot([box[0], box[0], box[1], box[1], box[0]],
                 [ylim[0], box[3], box[3], ylim[0], ylim[0]], **kwargs)

    elif x_split and not y_split:
        plt.plot([xlim[1], box[0], box[0], xlim[1], xlim[1]],
                 [box[2], box[2], box[3], box[3], box[2]], **kwargs)

        plt.plot([xlim[0], box[1], box[1], xlim[0], xlim[0]],
                 [box[2], box[2], box[3], box[3], box[2]], **kwargs)

    elif x_split and y_split:
        plt.plot([xlim[1], box[0], box[0]], [box[2], box[2], ylim[1]],
                 **kwargs)

        plt.plot([xlim[0], box[1], box[1]], [box[2], box[2], ylim[1]],
                 **kwargs)

        plt.plot([xlim[1], box[0], box[0]], [box[3], box[3], ylim[0]],
                 **kwargs)

        plt.plot([xlim[0], box[1], box[1]], [box[3], box[3], ylim[0]],
                 **kwargs)

    elif not x_split and not y_split:
        plt.plot([box[0], box[0], box[1], box[1], box[0]],
                 [box[2], box[3], box[3], box[2], box[2]], **kwargs)
