import matplotlib.pyplot as plt

plt.rc('font',**{'family':'Times New Roman', 'size': 16})
plt.rc('axes', axisbelow=True)
plt.rcParams['pdf.fonttype'] = 42

def draw():
    PREV_CW = (-2, 80)
    x = [ 1, 2, 3, 4, 5, 6, 7]
    y_cwv = [ 10, 20, 40, 80, 160, 80, 81]
    y_newcwv = [ 10, 20, 40, 80, 81, 82, 83]

    # Initial window
    plt.scatter(PREV_CW[0], PREV_CW[1], label='Previous CWND size', color='red', marker='*', lw=3)
    
    # No New CWV
    # plt.plot(x, y_cwv, lw=3)

    # New CWV
    plt.plot(x, y_newcwv, lw=3)
    
    # Link Capacity
    plt.plot([-2, 7], [100, 100], linestyle='dotted', label='Link Capacity', lw=3)

    plt.plot([-2, 1], [0, 0], label='Idle Period', lw=3)
    plt.annotate('Idle t(x) > RTO', [-0.79, 0], xytext=(.33, 0.25), textcoords='axes fraction',
            arrowprops=dict(facecolor='black'),
            horizontalalignment='right', verticalalignment='top')

    plt.legend(bbox_to_anchor=(1.07, -.1), ncol=2)
    plt.xlabel("Time")
    plt.ylabel("CWND Size")
    plt.ylim(bottom=-8, top=168)
    plt.xticks([])
    plt.yticks([])

    plt.gcf().set_size_inches(6, 3)
    figure_name = '/vagrant/doc/paper/figures/new_cwv.pdf'
    print(f"Saving {figure_name}")
    plt.savefig(figure_name, bbox_inches='tight')

if __name__ == '__main__':
    draw()