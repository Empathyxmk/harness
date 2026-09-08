import os
import shutil
import modelfiles

def default_filename(repo_id):
    # Just like before, handle proper model naming
    if not isinstance(repo_id, str) or "/" not in repo_id:
        return ""
    ext = getattr(modelfiles, "DEFAULT_FILE_EXT", "gguf")
    pieces = repo_id.strip().split("/")
    basename = pieces[-1]
    # Try to parse possible quant, else fallback
    if "-gguf" in basename or "-GGUF" in basename:
        return basename.split("-")[0] + ".Q4_K_M." + ext
    if basename.endswith(ext):
        return basename
    if basename.count("-") >= 1 and ext in basename:
        return basename
    return ""

def download(repo_id, filename):
    from huggingface_hub import hf_hub_download
    # Download and return path
    return hf_hub_download(repo_id, filename)

def remove(repo_id, filename):
    """Removes models from disk

    Either removes entire repo_id or just filename within that repo.
    Does nothing if the file or repo does not exist on disk.
    """
    path = ""
    if filename:
        # Corrected bug: should use repo_id, not undefined variable
        path = modelfiles.path_from_model(repo_id, filename)
        if path:
            path = os.path.realpath(path)
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    os.remove(os.path.realpath(path))
                except FileNotFoundError:
                    pass
            return path
        return None
    else:
        dir_path = modelfiles.path_from_repo(repo_id)
        if dir_path:
            try:
                shutil.rmtree(dir_path)
            except Exception:
                pass
            return dir_path
        return ""