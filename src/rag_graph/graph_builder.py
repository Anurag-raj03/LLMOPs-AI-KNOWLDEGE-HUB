from langgraph.graph import StateGraph, END
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag_graph.nodes.retriever_node import RetrieverNode
from rag_graph.nodes.generator_node import GeneratorNode
from rag_graph.nodes.summarizer_node import SummarizerNode
from rag_graph.nodes.evaluator_node import EvaluatorNode
from rag_graph.nodes.feedback_node import FeedbackNode

def build_rag_graph():
    graph = StateGraph(dict)
    graph.add_node("retriever", RetrieverNode())
    graph.add_node("generator", GeneratorNode())
    graph.add_node("summarizer", SummarizerNode())
    graph.add_node("evaluator", EvaluatorNode())
    graph.add_node("feedback", FeedbackNode())
    graph.add_edge("retriever", "generator")
    graph.add_edge("generator", "summarizer")
    graph.add_edge("summarizer", "evaluator")
    graph.add_edge("evaluator", "feedback")
    graph.set_entry_point("retriever")
    graph.set_finish_point("feedback")

    return graph.compile()
