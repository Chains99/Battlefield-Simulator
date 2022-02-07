class node_heap:
    def __init__(self, number, position, value):
        self.id = number
        self.position = position
        self.value = value


def heapify_up(heap, node):
    if (node.position == 0):
        return
    if (node.position % 2 == 0):
        temp = int(node.position / 2 - 1)
        if (temp >= 0):
            node_p = heap[temp]
            if (node_p.value > node.value):
                node_p.position = node.position
                heap[node.position] = node_p
                node.position = temp
                heap[temp] = node
                heapify_up(heap, node)
        return
    else:
        temp = int(node.position / 2)
        if (temp >= 0):
            node_p = heap[temp]
            if (node_p.value > node.value):
                node_p.position = node.position
                heap[node_p.position] = node_p
                node.position = temp
                heap[temp] = node
                heapify_up(heap, node)
        return


def heapify_down(heap, node):
    left = None
    right = None
    if (node.position * 2 + 1 < len(heap)):
        left = heap[node.position * 2 + 1]
    else:
        return
    if (node.position * 2 + 2 < len(heap)):
        right = heap[node.position * 2 + 2]

    if (left == None):
        return
    if (right != None):
        min = None
        temp = 0
        if (left.value > right.value):
            temp = node.position * 2 + 1
            min = right
        else:
            temp = node.position * 2 + 2
            min = left
        if (min != None and min.value > node.value):
            min.position = node.position
            heap[min.position] = min
            node.position = temp
            heap[temp] = node
            heapify_down(heap, node)
    elif (left.value < node.value):
        left.position = node.position
        heap[left.position] = left
        node.position = node.position * 2 + 1
        heap[node.position] = node
        heapify_down(heap, node)
    return


def extract_min(heap):
    temp = heap[0]
    # heap[0] = heap[len(heap)-1]
    heap.pop(0)

    if len(heap) > 1:
        if heap[0].value > heap[1].value:
            # Then swap elements
            heap[0].position = heap[1].position
            heap[1].position = heap[0].position
            temp2 = heap[0]
            heap[0] = heap[1]
            heap[1] = temp2
    for item in heap:
        item.position -= 1
    return temp


def append_node(heap, node):
    node.position = len(heap)
    heap.append(node)
    heapify_up(heap, node)
