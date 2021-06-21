from src.usecases.cloud_storage_provider_management import CloudStorageProviderManagement


def synchronize_files(user_id, provider, access_token):
    csp = CloudStorageProviderManagement(provider)
    csp.synchronize_files(user_id, access_token)


def extract_and_index_content(user_id, provider, file_id, access_token):
    csp = CloudStorageProviderManagement(provider)
    csp.extract_and_index_content(user_id, provider, file_id, access_token)
