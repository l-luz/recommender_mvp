"""Tests for the LinUCB model persistence."""

import json
import numpy as np

from app.core.recommender.linucb import LinUCBRecommender
from app.core.training import OnlineTrainer
from app.utils.config import RECOMMENDER_CONFIG


def _build_simple_model(d: int = 3):
    """
    Helper for building a "non-trivial" LinUCB:
    applies some updates on different arms.
    """
    rec = LinUCBRecommender(n_arms=0, d=d, alpha=1.0)

    arms = [10, 20]
    ctxs = [
        np.array([1.0, 0.0, 0.5], dtype=float),
        np.array([0.0, 1.0, 0.5], dtype=float),
        np.array([0.5, 0.5, 1.0], dtype=float),
    ]
    rewards = [1.0, 0.0, 1.0]

    for i, ctx in enumerate(ctxs):
        arm = arms[i % len(arms)]
        r = rewards[i]
        rec.update(ctx, arm, r)

    return rec, arms


def test_linucb_save_and_load_preserves_parameters(tmp_path):
    """
    Ensures that saving and loading a model preserves its internal state.

    Verify that:
    - save_state() saves A and b to file
    - load_state() reconstructs the model consistently
    - before/after recommendations are identical
    """
    d = 4
    rec = LinUCBRecommender(n_arms=0, d=d, alpha=1.0)

    arms = [10, 20]

    ctx1 = np.ones(d)
    ctx2 = np.array([0.5, 0.2, 0.1, 0.9])

    rec.update(ctx1, arm=10, reward=1.0)
    rec.update(ctx2, arm=20, reward=0.5)
    rec.update(ctx1, arm=10, reward=0.2)

    contexts = np.stack([ctx1, ctx2], axis=0)

    rec_before = rec.recommend(arms, contexts, n_recommendations=2)

    model_path = tmp_path / "linucb.json"
    rec.save_state(str(model_path))
    assert model_path.exists()

    rec2 = LinUCBRecommender(n_arms=0, d=d, alpha=1.0)
    rec2.load_state(str(model_path), valid_arms=arms, d_expected=d)

    for arm in arms:
        assert np.allclose(rec.A_inv[arm], rec2.A_inv[arm])
        assert np.allclose(rec.b[arm], rec2.b[arm])

    rec_after = rec2.recommend(arms, contexts, n_recommendations=2)
    assert rec_before == rec_after


def test_linucb_state_ignored_if_dimension_mismatch(tmp_path):
    """Tests that loading a state with a different feature dimension is ignored."""
    # original model with d=3
    rec_orig, arms = _build_simple_model(d=3)
    model_path = tmp_path / "linucb_state.json"
    rec_orig.save_state(str(model_path))

    d_new = 4
    rec_new = LinUCBRecommender(n_arms=0, d=d_new, alpha=1.0)
    rec_new.load_state(path=str(model_path), valid_arms=arms, d_expected=d_new)

    # status should be the default (A=I, b=0) for each arm
    I = np.eye(d_new)
    zero = np.zeros((d_new, 1))

    for arm in arms:
        if arm not in rec_new.A_inv:
            rec_new.update(np.zeros(d_new), arm, 0.0)

        assert np.allclose(rec_new.A_inv[arm], I)
        assert np.allclose(rec_new.b[arm], zero)


def test_online_trainer_flush_saves_model(tmp_path, monkeypatch):
    """Verifies that OnlineTrainer.flush() triggers a model save."""
    model_path = tmp_path / "linucb_state_trainer.json"

    RECOMMENDER_CONFIG["model_path"] = str(model_path)

    d = 3
    rec = LinUCBRecommender(n_arms=0, d=d, alpha=1.0)
    trainer = OnlineTrainer(recommender=rec, batch_size=2)

    ctx1 = np.array([1.0, 0.0, 0.0], dtype=float)
    ctx2 = np.array([0.0, 1.0, 0.0], dtype=float)

    # will automatically flush when adding the second feedback
    trainer.add_feedback(ctx1, arm=10, reward=1.0)
    trainer.add_feedback(ctx2, arm=20, reward=0.0)

    assert model_path.exists(), "OnlineTrainer.flush não salvou o estado do modelo."

    # sanity check
    with open(model_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "d" in data and data["d"] == d
    assert "arms" in data and isinstance(data["arms"], dict)
    assert "10" in data["arms"] or 10 in data["arms"]
