# A custom GPT that reads your traces (GPT Actions)

ChatGPT can call the Pressfront API as a GPT Action. You import the OpenAPI spec once and paste a key.

## 1. Make the GPT

1. In ChatGPT open **Explore GPTs**, then **Create**, then the **Configure** tab.
2. Name: `Pressfront Trace`. Instructions (paste):

   ```
   You explain what happened online around a name or a story, using the Pressfront actions.
   Start with list_samples when the user has no trace id. For a story, call get_case and
   report its four stops in order: who said it first, how it spread, who is passing it on,
   whether it happened before. For the whole picture call get_trace_brief.
   Quote posts with their links. Sides and tone are read by a language model: say so.
   Never decide who is right, never call anyone a bot or a coordinated campaign.
   ```

## 2. Add the action

1. At the bottom of **Configure**, press **Create new action**.
2. Press **Import from URL** and paste:

   ```
   https://pressfront.co/api/v1/openapi.json
   ```

   Every endpoint appears as an operation (`list_samples`, `get_case`, `get_trace_brief`, `instant_check`, ...).

3. **Authentication**: press the gear, pick **API Key**, **Auth Type: Bearer**, and paste a key:
   - to try it: the public demo key `pf_live_DemoKeyForPressfrontTraceSample1` (reads the 3 sample traces only)
   - for your own traces: a key from Settings at https://pressfront.co/account.html#settings (pick **Read only** if the GPT should never start a trace)

   ChatGPT then sends `Authorization: Bearer <key>` on every call.

4. **Privacy policy** (ChatGPT asks for one to share a GPT): `https://pressfront.co/privacy.html`

## 3. Ask it

> Who started the story that Lara went partying after the concert was cancelled?

It calls `list_samples`, then `get_case` on `01M6S180Z4AYZ47ACQT09S4WEX`, and walks through the four stops.

> What are people saying to @nytimes? Quote one post from each side.

It calls `instant_check` with `nytimes`.

## Good to know

- ChatGPT gives an action only a short time to answer. Reading a trace is fast. Starting one takes minutes: the GPT gets an id back and can check on it with `get_trace` (`wait=25`).
- One key, one account: everyone who uses a shared GPT reads the traces of the key's account. Use the demo key or a read-only key for a public GPT.
- Limits: 60 calls a minute per key; the demo key, 20 a minute per person.
