#!/usr/bin/env python3
"""对 trade.ttl 做 OWL 2 RL 物化，只打印本例个体上新出现的类型和关系。

依赖：rdflib、owlrl。不需要 Java，也不跑 OWL 2 DL。

    python3 reason.py
    python3 reason.py --contradict
"""

from __future__ import annotations

import sys
from pathlib import Path

from owlrl import OWLRL_Semantics, DeductiveClosure
from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.term import Node

TR = Namespace("https://example.com/onto/trade#")
ERR = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
HERE = Path(__file__).resolve().parent

RELATIONS = (TR.subsidiaryOf, TR.listedOn, TR.consignedTo, TR.employs, TR.employedBy)
TYPES = (
    TR.Party,
    TR.Person,
    TR.Organization,
    TR.SanctionList,
    TR.SanctionedParty,
    TR.Shipment,
    TR.BlockedShipment,
)

EXPECTED = (
    (TR.globex, RDF.type, TR.Organization),
    (TR.globex, RDF.type, TR.SanctionedParty),
    (TR.acme, RDF.type, TR.SanctionedParty),
    (TR.harbor, RDF.type, TR.Organization),
    (TR.harbor, RDF.type, TR.SanctionedParty),
    (TR.harbor, TR.subsidiaryOf, TR.globex),
    (TR.alice, RDF.type, TR.Person),
    (TR.alice, TR.employedBy, TR.harbor),
    (TR.A1042, RDF.type, TR.BlockedShipment),
)


def local(node: Node) -> str | None:
    text = str(node)
    if text.startswith(str(TR)):
        return text[len(str(TR)) :]
    return None


def show(triple: tuple[Node, Node, Node]) -> str | None:
    s, p, o = triple
    subj = local(s)
    if subj is None:
        return None
    if p == RDF.type:
        obj = local(o)
        if obj is None or URIRef(str(TR) + obj) not in TYPES:
            return None
        return f"{subj}  a  {obj}"
    if p in RELATIONS:
        obj = local(o)
        if obj is None:
            return None
        return f"{subj}  {local(p)}  {obj}"
    return None


def facts(triples) -> list[str]:
    lines = []
    for triple in triples:
        line = show(triple)
        if line is not None:
            lines.append(line)
    return sorted(set(lines))


def errors(graph: Graph) -> list[str]:
    found = []
    for message in graph.objects(None, ERR.error):
        found.append(str(message))
    return sorted(set(found))


def expand(contradict: bool) -> tuple[list[str], list[str], list[str]]:
    graph = Graph()
    graph.parse(HERE / "trade.ttl", format="turtle")
    if contradict:
        graph.add((TR.harbor, RDF.type, TR.Person))
    before = set(graph)
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    asserted = facts(before)
    inferred = sorted(set(facts(graph)) - set(asserted))
    return asserted, inferred, errors(graph)


def main() -> int:
    contradict = "--contradict" in sys.argv
    asserted, inferred, found_errors = expand(contradict)

    print("断言（trade.ttl 里写了的）")
    for line in asserted:
        print(f"  {line}")
    print("推出（物化后新出现的）")
    for line in inferred:
        print(f"  {line}")
    if found_errors:
        print("不一致")
        for message in found_errors:
            print(f"  {message}")

    if contradict:
        if not any("harbor" in message and "Disjoint" in message for message in found_errors):
            print("未捕获 Person 与 Organization 的冲突", file=sys.stderr)
            return 1
        return 0

    missing = [show(triple) for triple in EXPECTED if show(triple) not in inferred]
    if missing or found_errors:
        print("缺少预期推断:", ", ".join(m or "?" for m in missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
