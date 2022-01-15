# This code is written by Goutamkumar Tulajappa Kalburgi. NAU Email ID: gk325@nau.edu
__author__ = "Goutamkumar Tulajappa Kalburgi (gk325@nau.edu)"


class SearchNode:
    """A class to represent the Node.
    ...
    Attributes
    ----------
    adjacent_edges : list
        adjacent edges of the node
    label : str
        name(label) of the node
    level : int
        level of the node in the tree
    parent : str
        parent of the node
    value : int
        path cost from the start node to the node
    hSLD : float
        Straight line distance from the node to the goal
    cost : float
        Sum of its path cost(value) and estimated cost(hSLD)
    visited : bool
        Marks the node as visited(True) or no visited(False)
    x : int
        The x-coordinate of the node
    y : int
        The y-coordinate of the node

    Methods
    ----------
    addAdjacentEdge(adjacent_edge)
        Adds the adjacent_edge to the list of adjacent_edges
    """

    def __init__(self, label, x, y):
        """
        Constructs all the necessary attributes for the SearchNode object
        :param label:
            Name(label) of the node
        :param x:
            The x-coordinate of the node
        :param y:
            The y-coordinate of the node
        """
        self.adjacent_edges = []
        self.label = label
        self.level = -1
        self.parent = None
        self.value = 0
        self.hSLD = 0
        self.cost = 0
        self.visited = False
        self.x = int(x)
        self.y = int(y)
        self.cum_value = 0

    def addAdjacentEdge(self, adjacent_edge):
        """
        Adds the adjacent_edge to the list of adjacent_edges
        :param adjacent_edge:
            adjacent_edge to be added to the list of adjacent_edges.
            adjacent_edge is an array of [label, value]
        """
        self.adjacent_edges.append(adjacent_edge)

    def toString(self):
        """
        Returns the key attributes values in a string format.
        """
        return '' + self.label + ';' + str(self.level) + ';' + str(self.value) + ';' + str(self.hSLD) + ';' + str(self.cost)
