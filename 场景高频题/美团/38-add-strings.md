# 38. 字符串相加（Add Strings）· 简单

给定两个字符串形式的非负整数 `num1` 和 `num2`，计算它们的和并以字符串形式返回，不能使用任何大整数库或直接转换为整数。

## 示例

```
输入：num1 = "11", num2 = "123"
输出："134"
```

## 考点

- 从末位逐位相加 + 进位处理，O(max(n,m))。

## 代码实现

[Go 实现](../../solutions/p38_add_strings.go)

[单元测试](../../solutions/p38_add_strings_test.go)
