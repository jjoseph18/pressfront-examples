// Who is posting about a name right now? Pressfront's instant check, in one call.
//
//   node instant_check.mjs                 # @spacex, a real sample, with the public demo key
//   node instant_check.mjs @nytimes        # the other name sample the demo key answers
//   PRESSFRONT_API_KEY=pf_live_... node instant_check.mjs @anyname
//                                          # your own key: any X or Bluesky name, about a minute
//                                          # if nobody traced it today
//
// Node 18+ (built-in fetch), no packages. Sides and tone are read by a language model; Pressfront
// reports what people posted and never decides who is right.

const API = process.env.PRESSFRONT_API_BASE || "https://pressfront.co/api/v1";
const DEMO_KEY = "pf_live_DemoKeyForPressfrontTraceSample1";
const KEY = process.env.PRESSFRONT_API_KEY || DEMO_KEY;
// the demo key's invented name (made-up accounts), used if the real samples are not there
const INVENTED = "quillandclaw.bsky.social";

const handle = (process.argv[2] || "@spacex").replace(/^@+/, "");

async function instant(h) {
  for (let i = 0; i < 12; i++) {
    const r = await fetch(`${API}/instant/${encodeURIComponent(h)}?wait=50`, { headers: { Authorization: `Bearer ${KEY}` } });
    const body = await r.json();
    // 202 = Pressfront is searching this name now (free until it answers): ask again
    if (r.status === 202) {
      console.log(`searching @${h}... ${body.secondsLeft ?? "?"} s left`);
      await new Promise((ok) => setTimeout(ok, (body.retryAfterSec || 10) * 1000));
      continue;
    }
    return { status: r.status, body };
  }
  return { status: 504, body: { error: "timeout", message: "Still searching. Run it again in a minute." } };
}

let { status, body } = await instant(handle);
if (status === 404 && KEY === DEMO_KEY && handle !== INVENTED) {
  console.log(`(The demo key does not answer @${handle} yet; showing its invented sample @${INVENTED}.)\n`);
  ({ status, body } = await instant(INVENTED));
}
if (status !== 200) {
  console.error(`${status} ${body.error}: ${body.message}`);
  process.exit(1);
}

const n = (x) => (x == null ? "?" : Number(x).toLocaleString("en-US"));
console.log(`${body.handle}  (as of ${String(body.asOf).slice(0, 16).replace("T", " ")} UTC)\n`);
console.log(body.headline);
if (body.subline) console.log(body.subline);
console.log("");
for (const s of body.sides || []) {
  const q = s.quote ? `  "${s.quote.text.slice(0, 110)}${s.quote.text.length > 110 ? "..." : ""}" (${s.quote.account})` : "";
  console.log(`  ${String(s.label).padEnd(17)} ${n(s.count).padStart(7)}${q}`);
}
if (body.started && body.started.url) console.log(`\nStarted: ${body.started.url}`);
if ((body.carriers || []).length) {
  console.log("\nWho carried it (their posts brought the most others in):");
  for (const c of body.carriers) console.log(`  ${c.handle}  ${n(c.followers)} followers${c.brought != null ? `, brought ${n(c.brought)}` : ""}`);
}
if (body.note) console.log(`\n${body.note}`);
