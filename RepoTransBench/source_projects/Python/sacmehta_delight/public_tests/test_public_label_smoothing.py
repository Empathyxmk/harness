import pytest

@pytest.mark.skip("Skipping because of import issues in fairseq.criterions.label_smoothed_cross_entropy in this environment")
def test_label_smoothed_cross_entropy_loss_public():
    import torch
    from fairseq.criterions.label_smoothed_cross_entropy import label_smoothed_nll_loss

    lprobs = torch.log_softmax(torch.tensor([[0.1, 0.6, 0.3], [0.3, 0.4, 0.3]]), dim=-1)
    target = torch.tensor([1, 2])
    epsilon = 0.2

    loss, nll_loss = label_smoothed_nll_loss(lprobs, target, epsilon, ignore_index=None, reduce=True)
    assert loss > 0
    assert nll_loss > 0
    assert loss > nll_loss

@pytest.mark.skip("Skipping because of import issues in fairseq.criterions.label_smoothed_cross_entropy in this environment")
def test_label_smoothed_nll_loss_ignore_index_public():
    import torch
    from fairseq.criterions.label_smoothed_cross_entropy import label_smoothed_nll_loss

    lprobs = torch.log_softmax(torch.tensor([[0.9, 0.05, 0.05]]), dim=-1)
    target = torch.tensor([0])
    epsilon = 0.15
    ignore_index = 2

    loss, nll_loss = label_smoothed_nll_loss(lprobs, target, epsilon, ignore_index=ignore_index, reduce=True)
    assert loss >= 0
    assert nll_loss >= 0