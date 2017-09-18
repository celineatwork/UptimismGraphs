import sys, json
from uptimism.bar_graph import BarGraph

class Graph():
    LINEGRAPH = u"lineGraph"
    BARGRAPH = u"barGraph"
    GAUGEGRAPH = u"gaugeGraph"

def main():
    if len(sys.argv) > 1:
        
        with open(sys.argv[1]) as f:
            data = json.load(f)
            make_graph(data)
            f.close()

def make_graph(data):
    # graph = LineGraph(data)
    graph = BarGraph(data)
    # print test
        
main()
