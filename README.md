# Pressfront examples

**Pressfront Trace** finds who started a story online, who spread it, and what they are saying, on X, Bluesky and other sites (Reddit, forums, news). It shows who said what and when; it never decides who is right.

Five small examples, each one runs in under a minute with the public demo key. No sign-up.

| | Example | What it does |
|---|---|---|
| 1 | [`python/who_started_it.py`](python/who_started_it.py) | The answer to "who started it?" in four stops: who said it first, how it spread, who is passing it on, whether it happened before. |
| 2 | [`javascript/instant_check.mjs`](javascript/instant_check.mjs) | Who is posting about a name right now, on which side, with a quote from each side. One call. |
| 3 | [`claude/mcp.md`](claude/mcp.md) | Ask Claude "what happened?" and it reads the trace for you (Claude Code in one line, or claude.ai as a connector). |
| 4 | [`slack/alerts.md`](slack/alerts.md) | Alerts in a Slack or Discord channel when posts about a name jump. What they look like. |
| 5 | [`chatgpt/actions.md`](chatgpt/actions.md) | A custom GPT that reads your traces, from the OpenAPI spec. |

## Try it now: the demo key and 3 real traces

The demo key is public. It only reads: it never starts a trace or a search.

```
pf_live_DemoKeyForPressfrontTraceSample1
```

It reads three real finished traces:

| Kind | Trace | Id |
|---|---|---|
| A story going around | "Lara went partying after concert cancelled" | `01M6S180Z4AYZ47ACQT09S4WEX` |
| A very big name | @nytimes, 17,383 accounts | `01M6S483JT47MPY51RV3XTQ6BD` |
| The instant check | @spacex | `01M6PX06C05X1TV8V1NYZNTKJ3` |

```bash
curl https://pressfront.co/api/v1/samples \
  -H "Authorization: Bearer pf_live_DemoKeyForPressfrontTraceSample1"

curl https://pressfront.co/api/v1/traces/01M6S180Z4AYZ47ACQT09S4WEX/case \
  -H "Authorization: Bearer pf_live_DemoKeyForPressfrontTraceSample1"
```

Every trace has `/case` (the four stops as data) and `/brief` (the whole situation as Markdown, ready to paste into any AI). A name trace also has `/story`, `/accounts`, `/posts`, `/timeline`, `/groups`, `/who`, `/sites` and `/evidence`.

The demo key also reads one invented trace (made-up accounts), `01JDEM0SAMP1E000000000000T`.

## Run the examples

```bash
# Python 3.8+
pip install requests
python python/who_started_it.py

# Node 18+, no packages
node javascript/instant_check.mjs
node javascript/instant_check.mjs @nytimes
```

## With your own key

Make a key in Settings at <https://pressfront.co/account.html#settings> (it comes with Trace) and set it once:

```bash
export PRESSFRONT_API_KEY=pf_live_...
python python/who_started_it.py "the story in the few words people post about it"
node javascript/instant_check.mjs @anyname
```

With your own key the examples start real traces and search any name. A name nobody traced today takes about a minute; a story trace takes a few minutes.

## Good to know

- Sides and tone (critical, mocking, supportive, ...) are read by a language model, and the answers say so.
- We report posts and counts. We do not call anyone a bot, and accounts that posted at the same time are a timing match, not proof anyone coordinated.
- Rate limits: the demo key allows 20 calls a minute per person. Your own key allows 60 a minute.

## Links

- Docs: <https://pressfront.co/developers>
- OpenAPI spec: <https://pressfront.co/api/v1/openapi.json>
- MCP server (Claude, Cursor, any MCP client): `https://pressfront.co/api/mcp`
- Questions: support@pressfront.co

MIT licensed. See [LICENSE](LICENSE).

## No key? Pay per call

Run it from the [Apify Store](https://apify.com/pressfront/pressfront-trace): pay per call, no subscription.
