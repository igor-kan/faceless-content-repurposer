# faceless-content-repurposer

Generate clip and republishing plans for faceless YouTube/social workflows.

## What it does
- Reads source content inventory from CSV
- Generates short-form hook/title plan
- Produces a simple publishing calendar

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/build_repurpose_plan.py --input examples/sources.csv --output out
```

## References
- YouTube Data API docs: https://developers.google.com/youtube/v3/docs
- Reddit API docs: https://developers.reddit.com/docs/capabilities/server/reddit-api
- Kit sequences API: https://developers.kit.com/api-reference/v3/sequences
- beehiiv API: https://developers.beehiiv.com/
