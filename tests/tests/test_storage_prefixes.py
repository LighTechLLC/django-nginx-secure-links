def test_hashing_called_when_path_in_private_prefixes(
    storage_params_partially_private,
    partially_private_storage,
    mock_utils_obj,
    mocked_utils_gen_hash,
):
    prefix = storage_params_partially_private['private_prefixes'][0]
    sample_path = '{}/sample1.pdf'.format(prefix)
    partially_private_storage.url(sample_path)
    assert mock_utils_obj.call_count == 1


def test_hashing_not_called_when_path_not_in_private_prefixes(
    storage_params_partially_private,
    partially_private_storage,
    mock_utils_obj,
    mocked_utils_gen_hash,
):
    prefix = storage_params_partially_private['private_prefixes'][0]
    sample_path = 'not_{}/sample1.pdf'.format(prefix)
    partially_private_storage.url(sample_path)
    assert mock_utils_obj.call_count == 0


def test_hashing_not_called_when_path_in_public_prefixes(
    storage_params_partially_public,
    partially_public_storage,
    mock_utils_obj,
    mocked_utils_gen_hash,
):
    prefix = storage_params_partially_public['public_prefixes'][0]
    sample_path = '{}/sample1.pdf'.format(prefix)
    partially_public_storage.url(sample_path)
    assert mock_utils_obj.call_count == 0


def test_hashing_called_when_path_not_in_public_prefixes(
    storage_params_partially_public,
    partially_public_storage,
    mock_utils_obj,
    mocked_utils_gen_hash,
):
    prefix = storage_params_partially_public['public_prefixes'][0]
    sample_path = 'not_{}/sample1.pdf'.format(prefix)
    partially_public_storage.url(sample_path)
    assert mock_utils_obj.call_count == 1


def test_hashing_called_on_all_paths_for_private_storage(
    private_storage, mock_utils_obj, mocked_utils_gen_hash
):
    prefixes = [str(i) for i in range(100)]
    for prefix in prefixes:
        sample_path = '{0}/sample{0}.pdf'.format(prefix)
        private_storage.url(sample_path)
    assert mock_utils_obj.call_count == len(prefixes)
