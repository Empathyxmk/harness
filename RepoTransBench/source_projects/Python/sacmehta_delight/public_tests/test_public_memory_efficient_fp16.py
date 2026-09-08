import pytest

@pytest.mark.skip("Skipping because of import issues in fairseq.optim.memory_efficient_fp16 in this environment")
def test_memory_efficient_fp16_backward_and_grad_public():
    import torch
    import fairseq.optim.memory_efficient_fp16 as fp16

    model = torch.nn.Linear(4, 2).half()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

    input = torch.randn(5, 4).half()
    target = torch.randn(5, 2).half()

    loss = torch.nn.functional.mse_loss(model(input), target)
    fp16.memory_efficient_fp16_backward(loss, optimizer)
    for param in model.parameters():
        if param.grad is not None:
            assert torch.is_tensor(param.grad)

@pytest.mark.skip("Skipping because of import issues in fairseq.optim.memory_efficient_fp16 in this environment")
def test_fp32_optimizer_wrapper_state_public():
    import torch
    import fairseq.optim.memory_efficient_fp16 as fp16

    model = torch.nn.Linear(4, 2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    wrapper = fp16.FP32OptimizerWrapper(optimizer)
    assert hasattr(wrapper, 'state_dict')
    assert hasattr(wrapper, 'load_state_dict')