import crypto from "node:crypto";

export function verifyKieWebhookSignature(params: {
  taskId: string;
  timestamp: string;
  signature: string;
  webhookHmacKey: string;
}) {
  const { taskId, timestamp, signature, webhookHmacKey } = params;
  const dataToSign = `${taskId}.${timestamp}`;
  const expected = crypto
    .createHmac("sha256", webhookHmacKey)
    .update(dataToSign)
    .digest("base64");

  const a = Buffer.from(expected, "utf8");
  const b = Buffer.from(signature, "utf8");
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}
