export function isConnectionAllowed(sourceType: string, targetType: string): boolean {
  if (sourceType === 'textNode' && ['imageNode', 'videoNode', 'audioNode', 'imageEditorNode'].includes(targetType)) return true;
  if (sourceType === 'imageNode' && ['videoNode', 'imageEditorNode'].includes(targetType)) return true;
  if (sourceType === 'audioNode' && ['videoNode'].includes(targetType)) return true;
  if (sourceType === 'uploadNode' && ['imageNode', 'videoNode', 'audioNode', 'imageEditorNode'].includes(targetType)) return true;
  return false;
}
