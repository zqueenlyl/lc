#!/usr/bin/env python3
"""vector-db/mvp.py

零依赖演示向量数据库的核心机制（对照 vector-db/README.md）：

1. 稠密向量 + 三种相似度度量（余弦 / 内积 / 欧氏）
2. FLAT 暴力检索（精确）
3. IVF 近似最近邻索引（K-means 聚类分桶 + nprobe 只扫最近桶）
4. 元数据过滤（先过滤后搜 / 先搜后过滤）

说明：真实向量库用 embedding 模型（BGE / text-embedding-3 / text2vec）生成语义向量；
本脚本用「字/词 → 确定性伪随机向量，句子 = 字/词向量平均」模拟，只为演示检索机制，
保持零依赖可运行。共享字的句子会得到相近向量，能体现「语义相近 → 距离近」。
"""

from __future__ import annotations

import hashlib
import math
import random

DIM = 64  # 向量维度


# ---------------------------------------------------------------------------
# 一、向量与相似度
# ---------------------------------------------------------------------------

def _normalize(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0:
        return v[:]
    return [x / norm for x in v]


def _word_vec(word: str) -> list[float]:
    """把一个词映射成确定性伪随机向量（同一词永远同一向量）。"""
    seed = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
    rnd = random.Random(seed)
    return _normalize([rnd.gauss(0, 1) for _ in range(DIM)])


def _tokenize(text: str) -> list[str]:
    """演示用简化分词：中文按单字切，英文/数字按连续字母切。

    真实场景用分词器（jieba 等）或直接上 embedding 模型，这里只为演示检索机制。
    """
    tokens: list[str] = []
    buf = ""
    for ch in text.lower():
        if "\u4e00" <= ch <= "\u9fff":  # CJK 汉字 → 单字 token
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(ch)
        elif ch.isalnum():
            buf += ch
        elif buf:
            tokens.append(buf)
            buf = ""
    if buf:
        tokens.append(buf)
    return tokens


def embed(text: str) -> list[float]:
    """句子 embedding：字/词向量平均 + 归一化（模拟语义向量）。"""
    words = _tokenize(text)
    if not words:
        return [0.0] * DIM
    v = [0.0] * DIM
    for w in words:
        wv = _word_vec(w)
        for i in range(DIM):
            v[i] += wv[i]
    return _normalize(v)


def cosine(a: list[float], b: list[float]) -> float:
    """余弦相似度（向量已归一化时，等价于内积）。"""
    return sum(x * y for x, y in zip(a, b))


def inner_product(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def euclidean(a: list[float], b: list[float]) -> float:
    """欧氏距离（越小越近）。"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ---------------------------------------------------------------------------
# 二、FLAT 暴力检索（精确基线）
# ---------------------------------------------------------------------------

def flat_search(query_vec, records, k=3):
    """全量扫描，取余弦相似度最高的 top-k。"""
    return sorted(records, key=lambda r: -cosine(query_vec, r["vec"]))[:k]


# ---------------------------------------------------------------------------
# 三、IVF 近似索引（聚类分桶 + 只扫最近 nprobe 个桶）
# ---------------------------------------------------------------------------

class IVFIndex:
    def __init__(self, nlist: int = 4, niter: int = 8):
        self.nlist = nlist
        self.centroids: list[list[float]] = []
        self.buckets: list[list[dict]] = [[] for _ in range(nlist)]
        self._niter = niter

    def train(self, vecs: list[list[float]]) -> None:
        """K-means 初始化 + 迭代，得到 nlist 个聚类中心。"""
        rnd = random.Random(42)
        self.centroids = [_normalize([rnd.gauss(0, 1) for _ in range(DIM)])
                          for _ in range(self.nlist)]
        for _ in range(self._niter):
            assign = [self._nearest_centroid(v) for v in vecs]
            for c in range(self.nlist):
                members = [vecs[i] for i in range(len(vecs)) if assign[i] == c]
                if members:
                    summed = [0.0] * DIM
                    for v in members:
                        for d in range(DIM):
                            summed[d] += v[d]
                    self.centroids[c] = _normalize([x / len(members) for x in summed])

    def _nearest_centroid(self, v: list[float]) -> int:
        return max(range(self.nlist), key=lambda c: cosine(v, self.centroids[c]))

    def add(self, record: dict) -> None:
        """写入：按最近中心分桶。"""
        self.buckets[self._nearest_centroid(record["vec"])].append(record)

    def search(self, query_vec, k=3, nprobe=1) -> list[dict]:
        """查询：只扫最近 nprobe 个桶（nprobe=1 最省，nprobe=nlist 退化为 FLAT）。"""
        cids = sorted(range(self.nlist),
                      key=lambda c: -cosine(query_vec, self.centroids[c]))[:nprobe]
        cands = [r for c in cids for r in self.buckets[c]]
        return sorted(cands, key=lambda r: -cosine(query_vec, r["vec"]))[:k]


# ---------------------------------------------------------------------------
# 四、元数据过滤
# ---------------------------------------------------------------------------

def pre_filter(records, predicate):
    """先过滤后搜（Milvus 的 filter-then-search 思路）。"""
    return [r for r in records if predicate(r)]


# ---------------------------------------------------------------------------
# 五、演示
# ---------------------------------------------------------------------------

def main() -> None:
    corpus = [
        ("退款怎么申请", "售后"), ("退款多久到账", "售后"),
        ("退货流程是什么", "售后"),
        ("物流多久能到货", "物流"), ("快递到哪了怎么查", "物流"),
        ("优惠券怎么使用", "营销"), ("会员积分怎么获得", "营销"),
    ]

    records = [
        {"id": i, "text": text, "category": cat, "vec": embed(text)}
        for i, (text, cat) in enumerate(corpus)
    ]

    print("=" * 68)
    print("1. 相似度度量")
    print("=" * 68)
    a, b = embed("退款怎么申请"), embed("退款多久到账")
    c = embed("物流多久能到货")
    print(f"cosine('退款怎么申请','退款多久到账') = {cosine(a, b):.3f}  (共享「退款」，明显更高)")
    print(f"cosine('退款怎么申请','物流多久能到货') = {cosine(a, c):.3f}  (无共享字，明显更低)")

    print()
    print("=" * 68)
    print("2. FLAT 暴力检索（精确 top-3）")
    print("=" * 68)
    q = embed("退款要多久")
    for r in flat_search(q, records, k=3):
        print(f"  [{r['id']}] {r['text']:<14} score={cosine(q, r['vec']):.3f}")

    print()
    print("=" * 68)
    print("3. IVF 近似索引（聚类分桶，只扫最近 nprobe 个桶）")
    print("=" * 68)
    ivf = IVFIndex(nlist=4)
    ivf.train([r["vec"] for r in records])
    for r in records:
        ivf.add(r)
    for nprobe in (1, 4):
        res = ivf.search(q, k=3, nprobe=nprobe)
        hits = ", ".join(f"[{r['id']}]{r['text']}" for r in res)
        print(f"  nprobe={nprobe}: {hits}  (nprobe=nlist 时退化为 FLAT)")

    print()
    print("=" * 68)
    print("4. 元数据过滤：先过滤后搜（只看「售后」类）")
    print("=" * 68)
    filtered = pre_filter(records, lambda r: r["category"] == "售后")
    for r in flat_search(q, filtered, k=3):
        print(f"  [{r['id']}] {r['text']:<14} ({r['category']}) score={cosine(q, r['vec']):.3f}")

    print()
    print("结论：向量库 = embedding 向量 + 相似度 + ANN 索引 + 元数据过滤。")


if __name__ == "__main__":
    main()
