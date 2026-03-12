import type { NodeKind } from './node.types';

export function createDefaultNodeData(kind: NodeKind) {
  switch (kind) {
    case 'textNode':
      return { title: 'Text', type: 'textNode', prompt: '', model: 'Gemini 2.5 Flash Lite', status: 'idle' };
    case 'imageNode':
      return { title: 'Image', type: 'imageNode', model: 'gpt-image-1', size: '1024', ratio: '16:9', status: 'idle' };
    case 'videoNode':
      return { title: 'Video', type: 'videoNode', model: 'veo-2', duration: '16s', ratio: '16:9', status: 'idle' };
    case 'audioNode':
      return { title: 'Audio', type: 'audioNode', model: 'elevenlabs-v3', voice: 'default', status: 'idle' };
    case 'imageEditorNode':
      return { title: 'Image Editor', type: 'imageEditorNode', editPrompt: '', model: 'gpt-image-1', status: 'idle' };
    case 'uploadNode':
      return { title: 'Upload', type: 'uploadNode', accept: 'any', status: 'idle' };
  }
}
