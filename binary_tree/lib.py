class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def bst_from_arr(arr: list, l: int, r: int):
    if r - l < 1:
        return None

    if r - l == 1:
        return TreeNode(arr[l].val)

    m = (r - l) // 2 + l
    return TreeNode(arr[m].val, bst_from_arr(arr, l, m), bst_from_arr(arr, m + 1, r))


def bst_from_list(head: ListNode):
    arr = []

    cur = head
    while cur:
        arr.append(cur)
        cur = cur.next

    return bst_from_arr(arr, 0, len(arr))


ls = ListNode(-3, ListNode(-1, ListNode(0, ListNode(5, ListNode(10, ListNode(11))))))
bst = bst_from_list(ls)
