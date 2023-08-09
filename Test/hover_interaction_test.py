import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)

x = np.random.rand(15)
y = np.random.rand(15)
names = np.array(list("ABCDEFGHIJKLMNO"))
c = np.random.randint(1, 5, size=15)

norm = plt.Normalize(1, 4)
cmap = plt.cm.RdYlGn

fig, ax = plt.subplots()
sc = plt.scatter(x, y, c=c, s=100, cmap=cmap, norm=norm)

annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str, ind["ind"]))),
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()

fig = plt.figure()
plot = fig.add_subplot(111)

# create some curves
for i in range(4):
    # Giving unique ids to each Graphs member
    plot.plot(
        [i * 1, i * 2, i * 3, i * 4],
        gid=i)


def on_plot_hover(event):
    # Iterating over each Graphs member plotted
    for curve in plot.get_lines():
        # Searching which Graphs member corresponds to current mouse position
        if curve.contains(event)[0]:
            print("over %s" % curve.get_gid())


fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)
plt.show()