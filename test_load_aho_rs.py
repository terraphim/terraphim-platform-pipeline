data, patterns=None, None
url = "https://terraphim-automata.s3.eu-west-2.amazonaws.com/project_manager.csv.gz"
role = "project manager"

import httpimport
with httpimport.remote_repo(['terraphim_utils2'], "https://raw.githubusercontent.com/terraphim/terraphim-platform-automata/main/"):
    import terraphim_utils2
from terraphim_utils2 import load_automata

data, patterns = load_automata(url)
print(data)