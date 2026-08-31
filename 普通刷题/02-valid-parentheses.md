# 02. 有效的括号（Valid Parentheses）· 简单

给定一个只包括 `'('`、`')'`、`'{'`、`'}'`、`'['`、`']'` 的字符串 `s`，判断字符串是否有效。

有效字符串需满足：
1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。

## 示例

```
输入：s = "()[]{}"
输出：true

输入：s = "(]"
输出：false
```

## 考点

- 栈的匹配，O(n)。

## 代码实现

[Go 实现](../solutions/p02_valid_parentheses.go)

[单元测试](../solutions/p02_valid_parentheses_test.go)
