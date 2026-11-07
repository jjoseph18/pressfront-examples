# Claude reads your traces (MCP)

Pressfront is an MCP server at `https://pressfront.co/api/mcp`. Connect it once, then ask in plain words: "what happened with my last trace?", "who started the Lara story?", "who carried it?".

## Claude Code: one line

Try it first with the public demo key (reads the 3 sample traces, never starts anything):

```bash
claude mcp add --transport http pressfront https://pressfront.co/api/mcp \
  --header "Authorization: Bearer pf_live_DemoKeyForPressfrontTraceSample1"
```

Then ask Claude Code:

> List the Pressfront samples, then tell me who started the Lara story and how it spread.

It calls `list_samples`, then `get_case` on `01M6S180Z4AYZ47ACQT09S4WEX`, and answers from the four stops.

With your own key (Settings at https://pressfront.co/account.html#settings), swap the key:

```bash
claude mcp remove pressfront
claude mcp add --transport http pressfront https://pressfront.co/api/mcp \
  --header "Authorization: Bearer $PRESSFRONT_API_KEY"
```

## claude.ai (or the Claude app): a custom connector

No key needed: you sign in to Pressfront instead.

1. In claude.ai open **Settings**, then **Connectors**.
2. Press **Add custom connector**.
3. Name: `Pressfront`. URL: `https://pressfront.co/api/mcp`. Press **Add**.
4. Press **Connect**. Sign in to Pressfront and press **Allow**.
   It reads only, unless you tick the box that lets it start traces too.
5. In a chat, turn the Pressfront connector on and ask.

## The tools it gets

| Tool | What it does |
|---|---|
| `list_samples` | The 3 real traces anyone can read |
| `get_case` | The answer in four stops: started, spread, who, before? |
| `get_trace_brief` | The whole situation as plain facts |
| `instant_check` | Who is posting about a name right now |
| `list_trace_posts`, `list_trace_accounts` | Every post and account, filtered and sorted |
| `trace_situation`, `start_trace` | Start a trace (your own full key only) |

The full list is in the OpenAPI spec: https://pressfront.co/api/v1/openapi.json

Claude is told to report what the stops say and quote posts, never to decide who is right or call anyone a bot.
