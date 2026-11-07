"""Who started it? The answer card of a Pressfront trace, in four stops.

    pip install requests

    python who_started_it.py                      # a real sample story, with the public demo key
    python who_started_it.py --trace TRACE_ID     # any trace your key can read
    PRESSFRONT_API_KEY=pf_live_... python who_started_it.py "Lara went partying after the concert was cancelled"
                                                  # start a new story trace (your own key), wait, print

The four stops: 1 who said it first, 2 how it spread, 3 who is passing it on, 4 whether it
happened before. Pressfront reports what it found; it never decides who is right.
"""
import os
import sys
import time

import requests

API = os.environ.get("PRESSFRONT_API_BASE", "https://pressfront.co/api/v1")
DEMO_KEY = "pf_live_DemoKeyForPressfrontTraceSample1"
KEY = os.environ.get("PRESSFRONT_API_KEY") or DEMO_KEY

# a real story trace anyone can read (GET /v1/samples lists all three)
SAMPLE_STORY = "01M6S180Z4AYZ47ACQT09S4WEX"
# the demo key's invented trace (made-up accounts), used if the samples are not there
INVENTED = "01JDEM0SAMP1E000000000000T"


def get(path, **params):
    r = requests.get(API + path, headers={"Authorization": "Bearer " + KEY}, params=params, timeout=60)
    return r.status_code, r.json()


def start_story(claim):
    if KEY == DEMO_KEY:
        sys.exit("Starting a trace needs your own key: set PRESSFRONT_API_KEY (make one at https://pressfront.co/account.html#settings).")
    r = requests.post(API + "/traces", json={"claim": claim}, headers={"Authorization": "Bearer " + KEY}, timeout=60)
    body = r.json()
    if r.status_code >= 400:
        sys.exit(f"{r.status_code} {body.get('error')}: {body.get('message')}")
    tid = body["id"]
    print(f"Trace {tid} {'(already running)' if body.get('reused') else 'started'}. A story trace takes a few minutes.")
    while True:
        status, t = get(f"/traces/{tid}", wait=25)   # holds up to 25 s until it finishes
        if status != 200:
            sys.exit(f"{status} {t.get('error')}: {t.get('message')}")
        if t["status"] in ("done", "thin"):
            return tid
        if t["status"] == "failed":
            sys.exit("The trace did not finish. Nothing to read; try again.")
        left = t.get("secondsLeft")
        print(f"  still {t['status']}" + (f", about {left} s left" if left else ""))
        time.sleep(1)


def read_case(tid):
    status, card = get(f"/traces/{tid}/case")
    if status == 404 and KEY == DEMO_KEY and tid == SAMPLE_STORY:
        print("(The real samples are not live yet; reading the demo key's invented trace instead.)\n")
        tid = INVENTED
        status, card = get(f"/traces/{tid}/case")
    if status != 200:
        sys.exit(f"{status} {card.get('error')}: {card.get('message')}")
    return card


def show(card):
    t = card.get("trace", {})
    print(f"Trace {t.get('id')}  ({'a story going around' if t.get('kind') == 'origin' else 'a name'}: {t.get('query')})\n")
    print(card["headline"], "\n")
    for s in card["stops"]:
        print(f"  {s['n']}  {s['label']:<8} {s['text']}")
        for extra in (s.get("sub"), s.get("url"), s.get("note")):
            if extra:
                print(f"     {'':<8} {extra}")
    if card.get("huh"):
        print(f"\n  Huh: {card['huh'].get('big')}  {card['huh'].get('line')}")
    print("\n" + card.get("note", ""))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # the cards use a middle dot; Windows consoles need this
    except Exception:
        pass
    if len(argv) >= 2 and argv[0] == "--trace":
        tid = argv[1]
    elif argv:
        tid = start_story(" ".join(argv))
    else:
        tid = SAMPLE_STORY
    show(read_case(tid))


if __name__ == "__main__":
    main(sys.argv[1:])
