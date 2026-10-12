#!/usr/bin/env python3
"""对 order.ttl 做 OWL 2 RL 物化。

    python3 reason.py
    python3 reason.py --contradict
"""

from __future__ import annotations

import sys
from pathlib import Path

from owlrl import OWLRL_Semantics, DeductiveClosure
from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.term import Node

OD = Namespace("https://example.com/onto/order#")
ERR = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
HERE = Path(__file__).resolve().parent

RELATIONS = (OD.hasStatus, OD.mayProceedTo)
TYPES = (
    OD.Status,
    OD.BeforePay,
    OD.Funded,
    OD.Fulfilled,
    OD.Terminal,
    OD.Order,
    OD.BeforePayOrder,
    OD.FundedOrder,
    OD.FulfilledOrder,
    OD.TerminalOrder,
)

EXPECTED = (
    (OD.A1042, RDF.type, OD.FulfilledOrder),
    (OD.B7, RDF.type, OD.BeforePayOrder),
    (OD.shipped, RDF.type, OD.Status),
    (OD.closed, RDF.type, OD.Status),
)


def local(node: Node) -> str | None:
    text = str(node)
    if text.startswith(str(OD)):
        return text[len(str(OD)) :]
    return None


def show(triple: tuple[Node, Node, Node]) -> str | None:
    subject, pred, obj = triple
    subj = local(subject)
    if subj is None:
        return None
    if pred == RDF.type:
        name = local(obj)
        if name is None or URIRef(str(OD) + name) not in TYPES:
            return None
        return f"{subj}  a  {name}"
    if pred in RELATIONS:
        name = local(obj)
        if name is None:
            return None
        return f"{subj}  {local(pred)}  {name}"
    return None


def facts(triples) -> list[str]:
    lines = []
    for triple in triples:
        line = show(triple)
        if line is not None:
            lines.append(line)
    return sorted(set(lines))


def errors(graph: Graph) -> list[str]:
    return sorted({str(message) for message in graph.objects(None, ERR.error)})


def expand(contradict: bool) -> tuple[list[str], list[str], list[str]]:
    graph = Graph()
    graph.parse(HERE / "order.ttl", format="turtle")
    if contradict:
        graph.add((OD.A1042, OD.hasStatus, OD.draft))
    before = set(graph)
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    asserted = facts(before)
    inferred = sorted(set(facts(graph)) - set(asserted))
    return asserted, inferred, errors(graph)


def main() -> int:
    contradict = "--contradict" in sys.argv
    asserted, inferred, found = expand(contradict)
    print("断言（order.ttl 里写了的）")
    for line in asserted:
        print(f"  {line}")
    print("推出（物化后新出现的）")
    for line in inferred:
        print(f"  {line}")
    if found:
        print("不一致")
        for message in found:
            print(f"  {message}")
    if contradict:
        if not any("sameAs" in message or "Disjoint" in message for message in found):
            print("未捕获「同时处于草稿和已发货」", file=sys.stderr)
            return 1
        return 0
    missing = [show(triple) for triple in EXPECTED if show(triple) not in inferred]
    if missing or found:
        print("缺少预期推断:", ", ".join(m or "?" for m in missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
