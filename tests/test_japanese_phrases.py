from src.japanese_phrases import pick_three_phrases


def test_pick_three_phrases():
    phrases = [{"jp": str(i)} for i in range(6)]
    out = pick_three_phrases(phrases, "2026-01-01")
    assert len(out) == 3
    assert len({x['jp'] for x in out}) == 3
