# 20. 正则表达式匹配（Regular Expression Matching）· 困难

给定字符串 `s` 和字符模式 `p`，实现支持 `'.'` 和 `'*'` 的正则匹配：

- `'.'` 匹配任意单个字符。
- `'*'` 匹配零个或多个它前面的那个元素。

匹配须覆盖整个字符串 `s`，而不是部分匹配。

## 示例

```
输入：s = "aab", p = "c*a*b"
输出：true

输入：s = "mississippi", p = "mis*is*p*."
输出：false
```

## 考点

- 动态规划，O(mn)。

## 代码实现

[Go 实现](../solutions/p20_regular_expression_matching.go)

[单元测试](../solutions/p20_regular_expression_matching_test.go)
