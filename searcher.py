# This code is written by Goutamkumar Tulajappa Kalburgi. NAU Email ID: gk325@nau.edu
__author__ = "Goutamkumar Tulajappa Kalburgi (gk325@nau.edu)"

import graphmaker
import graphviz
import searchnode
import node
import stats


class Searcher:
    """A class to create Search Objects.
    ...
    Attributes
    ----------
    traversal : list
        list of each visited node
    goal_node : str
        goal node in the graph
    graph_visualizer : GraphViz
        visualizing searches in a given search
    map_file : .txt
        text file with each line of the file describing one edge in the graph
    nodes : a dictionary of SearchNode objects
        Dictionary of SearchNode objects with node_label as the key
    open_list : list of SearchNode objects
        consists of nodes that have been visited but not expanded
    path : list
        Nodes that are visited to reach the goal_node
    search_algo : str
        Name of the search algorithm to be run on the map
    goal_found : bool
        Marks if the goal_node is found(True) or not found (False)
    """

    def __init__(self, search_algo, map_file, verbose):
        """
        Constructs all the necessary attributes for the Searcher object
        :param search_algo:
            Name of the search algorithm to be run on the map
        :param map_file:
            text file with each line of the file describing one edge in the graph
        """
        self.traversal = []
        self.start_node = None
        self.goal_node = None
        self.goal_found = False
        self.graph_visualizer = graphviz.GraphViz()
        self.graph_visualizer.loadGraphFromFile(map_file)
        self.map_file = map_file
        self.nodes = {}
        self.open_list = []
        self.path = []
        self.search_algo = search_algo
        self.stats = stats.Stats()
        self.adjacentEdges()
        self.verbose = verbose
        self.goal_nodes = []
        self.paths = []
        self.start_label = None
        print('z=Searcher(\'' + search_algo + '\',\'' + map_file + '\', hSLD,' + str(verbose) + ')')
        print('Loaded search type', '\'' + search_algo + '\'', 'with map in file:', '\'' + map_file + '\'')

    def adjacentEdges(self):
        """
        Reads each line of the map_file, and discovers adjacent edges of each node
        Creates the nodes dictionary with node_label as the key and SearchNode object as the value
        """
        with open(self.map_file) as f:
            lines = f.readlines()
        clean_lines = [x.strip() for x in lines]
        for line in clean_lines:
            line = line.replace('\'', '').replace('[', '').replace(']', '').replace(' ', '').strip('()')
            raw_edge = line.split(',')
            [node1, node2, edge_value, x1, y1, x2, y2] = raw_edge
            if node1 not in self.nodes.keys():
                s = searchnode.SearchNode(node1, x1, y1)
                self.nodes[node1] = s
            self.nodes[node1].addAdjacentEdge([node2, edge_value])
            if node2 not in self.nodes.keys():
                s = searchnode.SearchNode(node2, x2, y2)
                self.nodes[node2] = s
            self.nodes[node2].addAdjacentEdge([node1, edge_value])
        self.stats.total_nodes = len(self.nodes)
        f.close()

    def breadthFirstSearch(self):
        """
        Traverses the nodes of the graph layer by layer, starting at a given vertex
        """
        while len(self.open_list) != 0:
            current_node = self.open_list.pop(0)
            if self.verbose:
                print('Exploring node \'' + current_node.label + '\'')
            self.stats.addFrontierSize(len(self.open_list))
            self.stats.addDepthSize(current_node.level)
            self.traversal.append(current_node.label)
            if current_node.label == self.goal_node.label:
                break
            adj_nodes = self.getChildren(current_node.label)
            if self.verbose:
                print('Inserting new children ', end='')
                print_adj_list = [x[0] for x in adj_nodes]
                print(print_adj_list[:])
            self.stats.addBranchSize(len(adj_nodes))
            for n in adj_nodes:
                self.nodes[n[0]].cost = float(n[1]) + current_node.value
                self.insertToOpenList(n, 'end', current_node)
            if self.verbose:
                print_open_list = [ol.toString() for ol in self.open_list]
                print('Open list:', print_open_list)

    def depthFirstSearch(self):
        """
        Traverses the nodes of the graph as far as possible along each branch
        """
        while len(self.open_list) != 0 and not self.goal_found:
            current_node = self.open_list.pop(0)
            if self.verbose:
                print('Exploring node \'' + current_node.label + '\'')
            self.stats.addFrontierSize(len(self.open_list))
            self.stats.addDepthSize(current_node.level)
            self.traversal.append(current_node.label)
            if current_node.label == self.goal_node.label:
                self.goal_found = True
                break
            adj_nodes = self.getChildren(current_node.label)
            if self.verbose:
                print('Inserting new children ', end='')
                print_adj_list = [x[0] for x in adj_nodes]
                print(print_adj_list[:])
            adj_nodes.reverse()
            self.stats.addBranchSize(len(adj_nodes))
            for n in adj_nodes:
                self.nodes[n[0]].cost = float(n[1]) + current_node.value
                self.insertToOpenList(n, 'front', current_node)
            for o in range(len(self.open_list)):
                self.depthFirstSearch()
            if self.verbose:
                print_open_list = [ol.toString() for ol in self.open_list]
                print('Open list:', print_open_list)

    def bestFirstSearch(self):
        """
        Traverses the nodes of the graph by expanding the node with the least path value
        """
        while len(self.open_list) != 0:
            self.open_list.sort(key=lambda x: x.cost)
            current_node = self.open_list.pop(0)
            if self.verbose:
                print('Exploring node \'' + current_node.label + '\'')
            self.stats.addFrontierSize(len(self.open_list))
            self.stats.addDepthSize(current_node.level)
            self.traversal.append(current_node.label)
            if current_node.label == self.goal_node.label:
                break
            adj_nodes = self.getChildren(current_node.label)
            if self.verbose:
                print('Inserting new children ', end='')
                print_adj_list = [x[0] for x in adj_nodes]
                print(print_adj_list[:])
            self.stats.addBranchSize(len(adj_nodes))
            for n in adj_nodes:
                cost = float(n[1]) + current_node.cost
                self.insertToOpenList(n, 'end', current_node, cost)
            if self.verbose:
                print_open_list = [ol.toString() for ol in self.open_list]
                print('Open list:', print_open_list)

    def aStarSearch(self):
        """
        Traverses the nodes of the graph by expanding the node with the least cost (path_value + hSLD)
        """
        while len(self.open_list) != 0:
            self.open_list.sort(key=lambda x: x.cost)
            current_node = self.open_list.pop(0)
            if self.verbose:
                print('Exploring node \'' + current_node.label + '\'')
            self.stats.addFrontierSize(len(self.open_list))
            self.stats.addDepthSize(current_node.level)
            self.traversal.append(current_node.label)
            if current_node.label == self.goal_node.label:
                break
            adj_nodes = self.getChildren(current_node.label)
            if self.verbose:
                print('Inserting new children ', end='')
                print_adj_list = [x[0] for x in adj_nodes]
                print(print_adj_list[:])
            self.stats.addBranchSize(len(adj_nodes))
            for n in adj_nodes:
                self.nodes[n[0]].hSLD = self.hSLD(n[0])
                self.nodes[n[0]].cum_value = float(n[1]) + current_node.cum_value
                cost = float(n[1]) + current_node.cum_value + self.nodes[n[0]].hSLD
                self.insertToOpenList(n, 'end', current_node, cost)
            if self.verbose:
                print_open_list = [ol.toString() for ol in self.open_list]
                print('Open list:', print_open_list)

    def getChildren(self, node_label):
        """
        Returns the children nodes for a given parent_node label
        :param node_label:
            node_label of the parent node
        :return:
            list of children nodes for the input node
        """
        return sorted(self.nodes[node_label].adjacent_edges, key=lambda x: x[0])

    def go(self):
        """
        Selection Control method. Controls the program flow based on the search algorithm selected
        """
        print('z.go()')
        print(self.search_algo, 'search: from \'' + self.start_node.label + '\' to \'', self.goal_nodes[:], '\'')
        path_costs = []
        min_index = 0
        for x in self.goal_nodes:
            self.goal_found = False
            self.nodes = {}
            self.open_list = []
            self.traversal = []
            self.path = []
            self.adjacentEdges()
            self.goal_node = self.nodes[x]
            self.start_node = self.nodes[self.start_label]
            self.start_node.level = 0
            self.start_node.value = 0
            self.start_node.parent = None
            self.start_node.visited = True

            self.open_list.append(self.start_node)


            if self.search_algo == 'breadth':
                print(
                    '\'' + self.search_algo + '\' search from: \'' + self.start_node.label + '\' to \'' + self.goal_node.label + '\'')
                self.breadthFirstSearch()
            if self.search_algo == 'depth':
                self.depthFirstSearch()
            if self.search_algo == 'best':
                self.bestFirstSearch()
            if self.search_algo == 'a_star':
                self.aStarSearch()
            p = self.getPath()
            self.printStats()
            self.paths.append(p)
            path_costs.append(self.stats.totalPathCost())
        if self.search_algo == 'best' or self.search_algo == 'a_star':
            min_index = path_costs.index(min(path_costs))
        else:
            min_index = self.paths.index(min(self.paths, key=len))
        print()
        print('The optimal route(lowest path cost/ shortest distance) is', self.paths[min_index])



    def insertToOpenList(self, adj_node, insert_at, current_node=None, cost=None):
        """
        Adds a node to the open_list (consists of nodes that have been visited but not expanded)
        :param cost:
        :param adj_node:
            Node to be added
        :param insert_at:
            front/end/at_order of the list
        :param current_node:
            parent_node of the given node to be added
        """
        n = self.nodes[adj_node[0]]
        if not n.visited or (self.search_algo != 'breadth' and n in self.open_list):
            if self.search_algo == 'depth' and n in self.open_list:
                self.open_list.remove(n)
            elif self.search_algo == 'best':
                if n in self.open_list:
                    if n.cost > cost:
                        self.open_list.remove(n)
                    else:
                        return
                n.cost = float(cost)
                n.value = float(adj_node[1])
            elif self.search_algo == 'a_star':
                if n in self.open_list:
                    if n.cost > cost:
                        self.open_list.remove(n)
                    else:
                        return
                n.cost = float(cost)
                n.value = float(adj_node[1])
            if self.search_algo == 'breadth' or self.search_algo == 'depth':
                n.value = float(adj_node[1])
            n.visited = True
            if current_node is not None:
                n.parent = current_node.label
                n.level = current_node.level + 1
            if insert_at == 'front':
                self.open_list.insert(0, n)
            elif insert_at == 'end':
                self.open_list.append(n)
            elif insert_at == 'order':
                self.open_list.append(n)
                self.open_list.sort(key=lambda x: x.value)

    def setStartGoal(self, start_label, goal_label):
        """
        Sets and initializes the start and goal_node
        :param start_label:
            label(name) of the start_node
        :param goal_label:
            label(name) of the goal_node
        """
        self.start_label = start_label
        self.start_node = self.nodes[start_label]
        self.start_node.level = 0
        self.start_node.value = 0
        self.start_node.parent = None
        self.start_node.visited = True
        self.open_list.append(self.start_node)
        if type(goal_label) is not list:
            self.goal_nodes.append(goal_label)
        else:
            for i in goal_label:
                self.goal_nodes.append(i)

        print('z.setStartGoal(\'' + start_label + '\',\'' + str(self.goal_nodes[:]) + '\')')

    def showOpen(self):
        """
        Prints tuples of (label, value) from the open_list
        """
        for o in self.open_list:
            t = (o.label, o.value)
            print(t, end='')
        print()

    def plotGraph(self):
        """
        Function to ask a loaded graph to plot itself
        """
        self.graph_visualizer.plot()

    def hSLD(self, node_label):
        """
        Returns the cartesian distance between the goal node some other node that is passed in
        """
        current_node = self.nodes[node_label]
        node1 = node.Node(current_node.x, current_node.y)
        node2 = node.Node(self.goal_node.x, self.goal_node.y)
        return node2.distance(node1)

    def getPath(self):
        """
        Prints the nodes that are visited to reach the goal_node
        """
        self.stats.searched_nodes = len(self.traversal)
        p = self.goal_node.label
        while p is not None:
            self.stats.addPathCost(self.nodes[p].value)
            self.path.append(p)
            p = self.nodes[p].parent
        self.path.reverse()
        print('Success! reached goal node \'' + self.goal_node.label + '\' with path:', self.path)
        return self.path

    def printStats(self):
        """
        Prints the stats summary for the search
        """
        print('------------------------')
        print('SEARCH SUMMARY STATS:')
        print('Search Type: \'' + self.search_algo + '\'. Map file: \'' + self.map_file + '\'')
        print('Total Nodes in Graph:', self.stats.total_nodes)
        print('Start Node:', '\'' + self.start_node.label + '\',', 'Goal Node(s):', '\'' + self.goal_node.label + '\'')
        print('Searched total of', self.stats.searched_nodes, 'nodes out of total of', self.stats.total_nodes,
              'nodes in the graph')
        print('Ended at \'' + self.goal_node.label + '\' with path cost:', self.stats.totalPathCost())
        print('Path (' + str(len(self.path)) + '):', self.path)
        print('Frontier Size: Average=', self.stats.averageFrontierSize(), '; Max size=', self.stats.maxFrontierSize())
        print('Depth of Search: Average=', self.stats.averageDepthSize(), '; Max depth=', self.stats.maxDepthSize())
        print('Average branching factor=', self.stats.averageBranchingFactor())
        print('Order of Node Expansion:', self.traversal)
