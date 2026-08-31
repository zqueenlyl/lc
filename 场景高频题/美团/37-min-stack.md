# 37. 最小栈（Min Stack）· 简单

设计一个支持 `push`、`pop`、`top` 操作，并能在常数时间内检索到最小元素的栈。

## 示例

```
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
输出：[null,null,null,null,-3,null,0,-2]
```

## 考点

- 辅助栈（同步记录当前最小值）或差值法，O(1)。

## 代码实现

[Go 实现](../../solutions/p37_min_stack.go)

[单元测试](../../solutions/p37_min_stack_test.go)
