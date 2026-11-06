from card_lint import lint
L='<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/aftechnet/claude-card@'+'a'*40+'/card.css">'
GOOD=L+'<div class="f"><div class="u"><b>x</b>y</div><span>→</span></div><button class="o p" onclick="sendPrompt(\'yes\')"><i>A<small>b</small></i></button>'
def test_good(): assert lint(GOOD.replace("'yes'","'yes x'"))==[]
def test_half_filled(): assert any('half-filled' in e for e in lint(GOOD.replace("'yes'","'change: '")))
def test_style(): assert 'has <style> block' in lint(GOOD+'<style></style>')
def test_main_not_first(): assert 'main option (o p) not first' in lint(L+'→<button class="o" onclick="sendPrompt(\'s\')"><i>S<small>x</small></i></button><button class="o p" onclick="sendPrompt(\'y\')"><i>Y<small>x</small></i></button>')
def test_unpinned(): assert 'no pinned card.css link' in lint(GOOD.replace('a'*40,'main'))
def test_long(): assert any('too long' in e for e in lint(GOOD+'x'*1200))
def test_live_needs_scope_line():
    h=GOOD.replace('</i></button>','</i><span class="t g">Changes now · low risk</span></button>')
    assert any('Not touched' in e for e in lint(h))
    assert not any('Not touched' in e for e in lint(h+'<div class="s">Not touched: servers · Undo: old text</div>'))
def test_old_tag_wording(): assert any('old tag wording' in e for e in lint(GOOD+'<div class="s">x</div><span class="t g">Live · low</span>'))
def test_jargon_warn(): assert any('tech words' in e for e in lint(GOOD.replace('<b>x</b>','<b>Merge git</b>')))
def test_fold_not_counted():
    h=GOOD+'<details><summary>How I know</summary>'+'s'*400+'</details>'+'x'*(1100-len(GOOD))
    assert not any('too long' in e for e in lint(h))
def test_fold_too_long(): assert any('fold too long' in e for e in lint(GOOD+'<details>'+'s'*600+'</details>'))
def test_bare_yes_warn(): assert any("bare 'yes'" in e for e in lint(GOOD))
def test_named_yes_ok(): assert not any("bare 'yes'" in e for e in lint(GOOD.replace("'yes'","'yes cut plan'")))
