# Alerts in Slack or Discord

When posts about a name you watch jump, Pressfront emails you. Paste one link in Settings and the same alert lands in a Slack or Discord channel too (or on your own server, signed).

This needs your own Pressfront account (Trace). The demo key has no alerts.

## 1. Get a link

**Slack:** make an app with [Incoming Webhooks](https://api.slack.com/messaging/webhooks), pick a channel, copy the link. It looks like `https://hooks.slack.com/services/T000/B000/XXXX`.

**Discord:** channel settings, **Integrations**, **Webhooks**, **New Webhook**, **Copy Webhook URL**. It looks like `https://discord.com/api/webhooks/123/abc`.

**Your own server:** any public `https://` address.

## 2. Paste it in Pressfront

Settings at https://pressfront.co/account.html#settings, paste the link, press **Save**, then **Send a test**. The channel gets:

> Pressfront test: this channel will get your Trace alerts.

## 3. Watch a name

In Settings, or over the API with a full key:

```bash
curl -X POST https://pressfront.co/api/v1/names \
  -H "Authorization: Bearer $PRESSFRONT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "@yourname"}'
```

## What an alert looks like

One plain line: the count, the usual, a link. No mood words.

**A jump** (posts in the last 15 minutes against the usual):

> @yourname: 42 posts in the last 15 min. Usually about 4. https://pressfront.co/trace.html?id=...

**It doubled again** after an alert:

> @yourname: 96 posts in the last 15 min (it doubled again). Usually about 4. https://pressfront.co/trace.html?id=...

**The 6-hour sweep** of a watched name:

> @yourname: first crossing into watch. https://pressfront.co/trace.html?id=...

Slack gets `{"text": "<the line>"}`, Discord gets `{"content": "<the line>"}`.

## Your own server: the JSON event

Your server gets the event itself, signed:

```json
{
  "id": "evt_mhb2k3a1f00d",
  "type": "alert.spike",
  "created_at": "2026-11-06T19:15:00.000Z",
  "data": { "name": "@yourname", "platform": "x", "count": 42, "usual": 4, "window_min": 15, "level": 1, "link": "https://pressfront.co/trace.html?id=...", "reason": "..." }
}
```

Types: `alert.spike`, `alert.sweep`, `alert.watch`, `trace.done` (your own server only, never Slack or Discord) and `test`.

Check the `Pressfront-Signature` header (`t=<unix seconds>,v1=<hex>`): it is HMAC-SHA256 of `<t>.<raw body>` with the `whsec_...` secret shown in Settings, the same scheme as Stripe's.

```python
import hashlib, hmac

def verified(raw_body: bytes, header: str, secret: str) -> bool:
    parts = dict(p.split("=", 1) for p in header.split(","))
    want = hmac.new(secret.encode(), f"{parts['t']}.".encode() + raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(want, parts["v1"])
```

## If a link stops working

We wait 8 seconds for a 2xx and try twice more, after 1 and 5 minutes, with the same `id`. If 3 alerts in a row never land, we pause the link and email you; email alerts keep coming. Fix it and press **Send a test**: a test that lands turns it back on.

Alerts are an early warning, not a guarantee: we do not promise every alert arrives or every post is counted.
