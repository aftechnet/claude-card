# claude-card

Shared style for AFTECH decision cards in Claude chat visuals (colors and layout only, no data).
Uses the claude.ai theme variables, so it works in light and dark mode.

Load it pinned to a commit (never @main in cards, it is cached and can change):

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aftechnet/claude-card@<commit>/card.css">

Classes: `.f` flow row (boxes `.g` green done, `.u` blue this yes, `.a` amber open, `.n` gray later, `.r` red broken), `.o` option row (`.o.p` main), `.t` tag, `.bar` bar row (fill width is a true share of the track since v1.4.0), `.tb` small table, `<details>` "How I know" fold. `.f.x` = flow with no role words (report card). `.dbt` one amber "Doubt:" line (v1.5). The first visible element after the `h2.sr-only` summary keeps the top-right corner free for the app's expand button (v1.5).
Change it with a new commit, then update the commit in the card skill. Old commits keep working.

Rules checker: `python3 card_lint.py card.html` (tests: `pytest test_card_lint.py`). It checks structure only, not clarity.
