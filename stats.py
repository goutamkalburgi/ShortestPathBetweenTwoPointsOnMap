# This code is written by Goutamkumar Tulajappa Kalburgi. NAU Email ID: gk325@nau.edu
__author__ = "Goutamkumar Tulajappa Kalburgi (gk325@nau.edu)"


class Stats:
    """A class to represent the Stats.
    ...
    Attributes
    ----------
    list_of_frontier_size : list
        list of the open_list length when a new node is taken out for exploration
    total_nodes : str
        total number of nodes in the map
    searched_nodes : int
        number of nodes that are traversed from a point
    list_of_path_cost : str
        list of path cost
    list_of_depth_size : int
        list of level for every traversal node
    list_of_branch_size : float
        list of no of children for every node traversed
    """

    def __init__(self):
        self.list_of_frontier_size = []
        self.total_nodes = 0
        self.searched_nodes = 0
        self.list_of_path_cost = []
        self.list_of_depth_size = []
        self.list_of_branch_size = []

    def addFrontierSize(self, size):
        """
        Add the len of open list at a given instance to the list
        :param size:
        """
        self.list_of_frontier_size.append(size)

    def averageFrontierSize(self):
        """
        :return: the average frontier size
        """
        return sum(self.list_of_frontier_size) / len(self.list_of_frontier_size)

    def maxFrontierSize(self):
        """
        :return: maximum frontier size
        """
        return max(self.list_of_frontier_size)

    def addPathCost(self, cost):
        """
        Add the path cost of a node at a given instance to the list
        :param size:
        """
        self.list_of_path_cost.append(cost)

    def totalPathCost(self):
        """
        :return: total path cost
        """
        return sum(self.list_of_path_cost)

    def addDepthSize(self, size):
        """
        Adds the level no of the node to the list
        :param size:
        """
        self.list_of_depth_size.append(size)

    def maxDepthSize(self):
        """
        :return: maximum depth size
        """
        return max(self.list_of_depth_size)

    def averageDepthSize(self):
        """
        :return: average depth size
        """
        return sum(self.list_of_depth_size) / len(self.list_of_depth_size)

    def addBranchSize(self, size):
        """
        Adds the branch size to the list
        :param size:
        :return:
        """
        self.list_of_branch_size.append(size)

    def averageBranchingFactor(self):
        """
        :return: average branching factor
        """
        return sum(self.list_of_branch_size) / (len(self.list_of_branch_size) + 1)




