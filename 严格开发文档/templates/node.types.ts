export type NodeKind =
  | 'textNode'
  | 'imageNode'
  | 'videoNode'
  | 'audioNode'
  | 'imageEditorNode'
  | 'uploadNode';

export type MediaResult =
  | { kind: 'text'; text: string }
  | { kind: 'image'; url: string }
  | { kind: 'video'; url: string }
  | { kind: 'audio'; url: string };

export interface UploadedAsset {
  id?: string;
  kind: 'image' | 'video' | 'audio';
  url: string;
  name?: string;
}
