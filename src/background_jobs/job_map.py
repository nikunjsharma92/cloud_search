from src.background_jobs.background_jobs import synchronize_files, extract_and_index_content

background_jobs = {
    'SYNCHRONIZE_FILES': 'synchronize_files',
    'EXTRACT_AND_INDEX_CONTENT': 'extract_and_index_content',
}

background_jobs_map = {
    background_jobs['SYNCHRONIZE_FILES']: synchronize_files,
    background_jobs['EXTRACT_AND_INDEX_CONTENT']: extract_and_index_content,
}