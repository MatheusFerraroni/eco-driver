import os
import json
import matplotlib.pyplot as plt

files = os.listdir("./")

z_add = 50

files = ['super.extras']

for f in files:
    ext = f.split(".")[-1]

    if ext!="extras":
        continue

    file = open(f,"r")
    infos = json.loads(file.read())
    file.close()

    xs = []
    ys = []
    ys_green_above = []
    ys_green_below = []
    max_x = 0
    fig, ax = plt.subplots(figsize=(200,4))

    min_h = float("Infinity")
    max_h = -float("Infinity")
    for i in range(len(infos)):

        inf = infos[i]
        max_x = max(max_x,inf["x"])
        xs.append(inf["x"])
        ys.append(inf["z"]+z_add)
        ys_green_above.append(inf["z"]+z_add+10)
        ys_green_below.append(inf["z"]+z_add-10)

        min_h = min(min_h, inf["angle"])
        max_h = max(max_h, inf["angle"])

        if i%50==0 and i%100!=0:
            ax.annotate(str(round(inf["angle"],1)),
                        xy=(inf["x"], inf["z"]+z_add+5), xycoords='data',
                        xytext=(5, 40), textcoords='offset points',
                        arrowprops=dict(arrowstyle="->"),
                        horizontalalignment='right', verticalalignment='bottom')

    print(min_h, max_h)
    # ax.set_ylim(0,175)
    # ax.patch.set_facecolor('#87d3e0')
    # ax.set_xlim(-20,max_x+20)
    # ax.stackplot(xs, ys_green_above, color="#269126")
    # ax.stackplot(xs, ys, color="#000000")
    # ax.stackplot(xs, ys_green_below, color="#269126")
    # ax.set_title('Elevation for Map '+f.replace(".extras",""))
    # ax.set_xlabel('Distance (m)')
    # ax.set_ylabel('Height (h)')
    # plt.savefig(f+".pdf", bbox_inches="tight")