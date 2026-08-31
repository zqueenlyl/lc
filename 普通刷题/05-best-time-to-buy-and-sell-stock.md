# 05. 买卖股票的最佳时机（Best Time to Buy and Sell Stock）· 简单

给定一个数组 `prices`，其中 `prices[i]` 是第 `i` 天的股票价格。你只能选择某一天买入，并在未来某一天卖出，求能获得的最大利润；若无法获利则返回 0。

## 示例

```
输入：prices = [7,1,5,3,6,4]
输出：5
解释：第 2 天买入（1），第 5 天卖出（6），利润 5。
```

## 考点

- 一次遍历维护历史最低价，O(n)。

## 代码实现

[Go 实现](../solutions/p05_best_time_to_buy_and_sell_stock.go)

[单元测试](../solutions/p05_best_time_to_buy_and_sell_stock_test.go)
