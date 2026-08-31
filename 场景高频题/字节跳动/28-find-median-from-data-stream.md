# 28. 数据流的中位数（Find Median from Data Stream）· 困难

设计一个数据结构，支持动态添加整数并随时返回当前所有元素的中位数：

- `addNum(num)`：将整数 num 添加到数据流中。
- `findMedian()`：返回目前所有元素的中位数。

## 示例

```
输入：
["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
[[],[1],[2],[],[3],[]]
输出：[null,null,null,1.5,null,2.0]
```

## 考点

- 大顶堆（较小半部分）+ 小顶堆（较大半部分），O(log n)。
