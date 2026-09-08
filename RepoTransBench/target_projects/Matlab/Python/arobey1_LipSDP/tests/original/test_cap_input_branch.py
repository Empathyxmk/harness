from src.lipsdp.error_messages import cap_input

def test_cap_input_branch_cases():
    N = 3
    input_num = 2  # nchoosek(3,2) = 3
    result = cap_input(input_num, N, 'random neurons')
    assert result == 2
    input_num = 100
    limit = N * (N - 1) // 2
    result = cap_input(input_num, N, 'random neurons')
    assert result == limit