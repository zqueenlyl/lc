package solution

// ListNode 单链表节点定义。
type ListNode struct {
	Val  int
	Next *ListNode
}

// TreeNode 二叉树节点定义。
type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// RandomNode 带随机指针的链表节点定义。
type RandomNode struct {
	Val    int
	Next   *RandomNode
	Random *RandomNode
}
