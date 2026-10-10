Problem to solve
A support ticket arrives as plain text. Your program must classify it and return a structured result.
Input:
My order #4821 has not arrived.


Expected output:
{
  "category": "order_status",
  "order_id": "4821",
  "needs_order_lookup": true
}
