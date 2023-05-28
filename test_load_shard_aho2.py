

def process_item(x):
    log(f"Shard ID {x}")
    log('shard id %s' % hashtag())
    data, patterns=None, None
    url = "https://terraphim-automata.s3.eu-west-2.amazonaws.com/project_manager.csv.gz"
    role = "project manager"

    import httpimport
    with httpimport.remote_repo(['terraphim_utils2'], "https://raw.githubusercontent.com/terraphim/terraphim-platform-automata/main/"):
        import terraphim_utils2
    from terraphim_utils2 import load_automata,find_matches
    data, patterns = load_automata(url)
    log(f"Loading automata from url {url} with and patterns {patterns}")
    haystack = "I am a text with the word Organization strategic plan and bar and project calendar"
    matches = find_matches(haystack, data, patterns)
    log(f"{matches}")
    # execute('set','debug{%s}'% hashtag(),1)

bg = GearsBuilder('ShardsIDReader')
bg.foreach(process_item)
bg.count()
bg.run()
