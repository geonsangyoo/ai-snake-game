import matplotlib.pyplot as pplot
from IPython import display

pplot.ion()


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(pplot.gcf())

    pplot.clf()
    pplot.title("Gaming by AI-Bot")
    pplot.xlabel("Number of Game")
    pplot.ylabel("SCORE")

    pplot.plot(scores)
    pplot.plot(mean_scores)

    pplot.ylim(ymin=0)

    pplot.text(len(scores) - 1, scores[-1], str(scores[-1]))
    pplot.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))

    pplot.show(block=False)
    pplot.pause(0.1)
