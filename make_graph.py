import sys, json
# import linegraph, bargraph, gaugegraph
from linegraph_filled import LineGraph
from bargraph import BarGraph


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
        
main()
