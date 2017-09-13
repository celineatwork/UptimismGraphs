import sys, json
import linegraph, bargraph, gaugegraph


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
    # if data["type"] == Graph.LINEGRAPH:
    #     linegraph.create(data)
    # elif data["type"] == Graph.BARGRAPH:
    #     bargraph.create(data)
    # elif data["type"] == Graph.GAUGEGRAPH:
    #     gaugegraph.create(data)
    linegraph.create(data)
        
main()
