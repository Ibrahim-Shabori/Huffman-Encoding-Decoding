import sys
import copy
import time
 
# Defining tree nodes properties.
class Tree_node:
    def __init__(self, val):
        self.val = val
        self.right_child = None
        self.left_child = None
        self.parent = None
        self.done = False
        self.counter = 0

    def has_left_child(self):
        return self.left_child != None

    def has_right_child(self):
        return self.right_child != None

    def is_leaf(self):
        return not (self.has_left_child() or self.has_right_child())

# Defining binary trees properties.
class Binary_tree:
    # already_made property is used when rhe tree is already_made
    # but refusing the method that
    # "if it is bigger, go to left, if not go to right"
    def __init__(self, already_made = False):
        self.root = None
        self.num_enteries = 0
        self.nodes = list()
        self.already_made = already_made

    # if the tree is already_made then it put all the nodes in the list,
    # if not, it is only adding the node provided to the tree according to the method,
    # "if it is bigger, go to left, if not go to right", then also add this node in nodes list.
    def add_it(self, node):
        if not self.root:
            self.nodes.append(node)
            self.num_enteries += 1
            self.root = node
            if self.already_made:
                if node.left_child:
                    self.add_it(node.left_child)
                if node.right_child:
                    self.add_it(node.right_child)
        elif self.already_made:
            self.nodes.append(node)
            self.num_enteries += 1
            if node.left_child:
                self.add_it(node.left_child)
            if node.right_child:
                self.add_it(node.right_child)
        else:
            self.nodes.append(node)
            cur_node = self.root
            while cur_node:
                if node.counter > cur_node.counter:
                    if cur_node.left_child:
                        cur_node = cur_node.left_child
                    else:
                        cur_node.left_child = node
                        node.parent = cur_node
                        self.num_enteries += 1
                        break
                else:
                    if cur_node.right_child:
                        cur_node = cur_node.right_child
                    else:
                        cur_node.right_child = node
                        node.parent = cur_node
                        self.num_enteries += 1
                        break

    # it helps to reset "done" property that used to check nodes in (sorting)
    # and (getting_codes) process.
    def reset_dones(self):
        for node in self.nodes:
            node.done = False

    # Sorts the nodes values, from the smallest to the greatest,
    # and returns these values in a list.
    def sort_it(self):
        sorted_l = list()
        cur_node = self.root
        while len(sorted_l) < self.num_enteries:
            if cur_node.has_right_child() and not cur_node.right_child.done:
                cur_node = cur_node.right_child
                continue
            elif not cur_node.done:
                sorted_l.append((cur_node, cur_node.val))
                cur_node.done = True
                if cur_node.has_left_child() and not cur_node.left_child.done:
                    cur_node = cur_node.left_child
                else:
                    cur_node = cur_node.parent
            else:
                cur_node = cur_node.parent

        self.reset_dones()

        return sorted_l

    # Follows (depth first search in order) algorithm, to reach leaves
    # "1" added to the code if we go right, if we go left, "0" provided,
    # if we reched some leaf the code is put in  dictionary as a key,
    # and its value is that leaf we reached.
    def get_codes(self):
        nodes_codes = {}
        cur_node = self.root
        new_code = ""
        while cur_node:
            if cur_node.has_right_child() and not cur_node.right_child.done:
                cur_node = cur_node.right_child
                new_code+="1"
                continue
            else:
                cur_node.done = True
                if cur_node.has_left_child() and not cur_node.left_child.done:
                    cur_node = cur_node.left_child
                    new_code+="0"
                else:
                    if cur_node.is_leaf():
                        nodes_codes[cur_node.val] = copy.deepcopy(new_code)
                    cur_node = cur_node.parent
                    new_code = copy.deepcopy(new_code[:-1])

        self.reset_dones()
        return nodes_codes

    def __repr__(self):
        tex = "root : " + self.root.val
        return tex


def huffman_encoding(data):

    if not data:
        return "0", 0

    # Defining a char dictionary where keys are chars, and each key value
    # is its repetition in the data.
    # Also defining two b_trees, one of them is already_made :
    # means next we will make a tree by connecting nodes then
    # add the first one to the "already_made tree" because it didnt't follow the method.
    char_dict = {}
    b_tree = Binary_tree()
    f_tree = Binary_tree(True)

    # adding chars and their repetition to the char_dict.

    for i in data:
        try:
            if char_dict[i]:
                char_dict[i][1] += 1
        except KeyError:
            char_dict[i] = [i]
            char_dict[i].append(1)

    # adding chars to the tree implemented.
    for i in char_dict:
        new_node = Tree_node(char_dict[i][0])
        new_node.counter = char_dict[i][1]
        b_tree.add_it(new_node)

    if len(char_dict) == 1:
        f_code = "1" * len(data)
        head = Tree_node(data[0])
        node1= Tree_node(data[0])
        head.right_child = node1
        f_tree.add_it(head)
        return f_code, f_tree

    # elements_used will help later, f__dict will get ony new nodes.
    elements_used = 0
    f__dict = {}

    # this while loop sorts the tree that has the characters
    # then put the values(nodes) in order in a list.
    # next, we determine the last part that we didn't use before by starting at
    # elements_used which will be increase up every time by two.
    # the way to get out of this loop, is when there is just one item we didn't use
    # we add it then get out.
    while True:
        sorted_l, sorted__l = zip(*b_tree.sort_it())

        sorted_l = sorted_l[elements_used:]

        if len(sorted_l) == 1:
            break

        # every time we take the least two nodes with repetition, and merge them
        # in a new node, and add a copy of this node to the same tree to be compared,
        # with other nodes again.
        # the origin node we connect it with the nodes that its made of them.
        # then put the origin node in the dict that only takes new nodes.
        new_node = Tree_node(sorted_l[0].val + sorted_l[1].val)
        new_node.counter = sorted_l[0].counter + sorted_l[1].counter
        b_tree.add_it(copy.deepcopy(new_node))
        new_node.left_child = copy.deepcopy(sorted_l[0])
        new_node.right_child = copy.deepcopy(sorted_l[1])
        f__dict[new_node.val] = new_node
        elements_used += 2

    # we need root to be the last element in the new nodes
    # as it will be the root we need for the already_made tree.
    root = None
    for i in f__dict:
        root = f__dict[i]
        # set the children of all new nodes (non chars nodes)
        try:
            f__dict[i].right_child = f__dict[f__dict[i].right_child.val]
            f__dict[i].right_child.parent = f__dict[i]
        except KeyError:
            f__dict[i].right_child = Tree_node(f__dict[i].right_child.val)
            f__dict[i].right_child.parent = f__dict[i]
        try:
            f__dict[i].left_child = f__dict[f__dict[i].left_child.val]
            f__dict[i].left_child.parent = f__dict[i]
        except KeyError:
            f__dict[i].left_child = Tree_node(f__dict[i].left_child.val)
            f__dict[i].left_child.parent = f__dict[i]

    if root == None:
        f_tree.add_it(Tree_node(data))
        return "0", f_tree
    # set the already_made tree, and get codes.
    f_tree.add_it(root)
    node_codes = f_tree.get_codes()

    # get the code for the data provided.
    f_code = ""
    for i in data:
        f_code += node_codes[i]

    return f_code, f_tree

def huffman_decoding(data,tree):

    if tree == 0:
        return "No data provided"

    # get the first int from the code,
    # while there is not a char with this code take another int from the code
    # when it finds a char with the (code so far), add this char to the sentence
    # and renew the code.
    sentence = ""
    char = ""
    node_codes = tree.get_codes()
    code_nodes = {v: k for k, v in node_codes.items()}
    counter = 0
    while counter < len(data):
        char += data[counter]
        try:
            sentence += code_nodes[char]
            char = ""
            counter += 1
        except KeyError:
            counter += 1

    return sentence

# test cases
if __name__ == "__main__":
    codes = {}

    sen = []
    for i in range(3):
        sen.append(input(f"Put a sen {i+1}: "))

    for sentence in sen:

        a_great_sentence = sentence

        print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
        print ("The content of the data is: {}\n".format(a_great_sentence))

        encoded_data, tree = huffman_encoding(a_great_sentence)

        print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
        print ("The content of the encoded data is: {}\n".format(encoded_data))

        decoded_data = huffman_decoding(encoded_data, tree)

        print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
        print ("The content of the encoded data is: {}\n".format(decoded_data))
