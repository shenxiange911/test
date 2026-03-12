import type { Edge, Node } from "@xyflow/react";
import type { FlowNodeData, NormalizedKieResult } from "./kie.types";

export function updateNodeData(
  nodes: Node<FlowNodeData>[],
  nodeId: string,
  patch: Partial<FlowNodeData>,
): Node<FlowNodeData>[] {
  return nodes.map((node) =>
    node.id === nodeId
      ? {
          ...node,
          data: {
            ...node.data,
            ...patch,
          },
        }
      : node,
  );
}

export function applyTaskQueued(
  nodes: Node<FlowNodeData>[],
  nodeId: string,
  taskId: string,
): Node<FlowNodeData>[] {
  return updateNodeData(nodes, nodeId, {
    runState: "generating",
    taskId,
    error: null,
  });
}

export function applyTaskSuccess(
  nodes: Node<FlowNodeData>[],
  nodeId: string,
  result: NormalizedKieResult,
): Node<FlowNodeData>[] {
  return updateNodeData(nodes, nodeId, {
    runState: "success",
    result,
    error: null,
  });
}

export function applyTaskError(
  nodes: Node<FlowNodeData>[],
  nodeId: string,
  error: string,
): Node<FlowNodeData>[] {
  return updateNodeData(nodes, nodeId, {
    runState: "error",
    error,
  });
}

export function extractUpstreamText(nodes: Node<FlowNodeData>[], edges: Edge[], nodeId: string) {
  return edges
    .filter((edge) => edge.target === nodeId)
    .map((edge) => nodes.find((n) => n.id === edge.source))
    .filter(Boolean)
    .map((node) => node?.data?.prompt || "")
    .filter(Boolean)
    .join("\n\n");
}
