Automata=None 
url = "https://terraphim-automata.s3.eu-west-2.amazonaws.com/automata_project_manager.csv.gz.lzma"
role = "project-manager"
rconn=None 
def enable_debug():
    debug=execute('GET','debug{%s}'% hashtag())
    if debug=='1':
        debug=True
    else:
        debug=False
    return debug

def connecttoRedis():
    import redis 
    redis_client=redis.Redis(host='redisgraph',port=6379,charset="utf-8", decode_responses=True)
    return redis_client


def OnRegisteredAutomata():
    global Automata
    global url
    import httpimport
    with httpimport.remote_repo(['terraphim_utils'], "https://raw.githubusercontent.com/terraphim/terraphim-platform-automata/main/"):
        import terraphim_utils
    from terraphim_utils import loadAutomata
    # debug=enable_debug()
    debug = False
    if debug:
        log(f"Loading automata from url {url}")
    Automata=loadAutomata(url)
    return Automata



def process_item(record):
    import httpimport
    with httpimport.remote_repo(['stop_words'], "https://raw.githubusercontent.com/explosion/spaCy/master/spacy/lang/en/"):
        import stop_words
    from stop_words import STOP_WORDS
    with httpimport.remote_repo(['terraphim_utils'], "https://raw.githubusercontent.com/terraphim/terraphim-platform-automata/main/"):
        import terraphim_utils
    from terraphim_utils import loadAutomata, find_matches

    from string import punctuation
    import itertools
    import re
    debug=enable_debug()

    global Automata
    global url
    global role
    if not Automata:
        if debug:
            log(f"Loading automata from url {url}")
        Automata=loadAutomata(url)

    global rconn
    if not rconn:
        rconn=connecttoRedis()

    
    shard_id=hashtag()
    article_id=record['key'].split(':')[1]
    if debug:
        log(f"Matcher received {record['key']} and my {shard_id}")
    for each_key in record['value']:
        sentence_key=record['key']+f':{each_key}'
        # tokens=set(record['value'][each_key].split(' '))
        processed=execute('SISMEMBER','processed_docs_stage3_%s_{%s}' % (role,shard_id),sentence_key)
        # processed = False
        if not processed:
            # if debug:
            #     log("Matcher: tokens " + str(tokens))
            #     log("Matcher: length of tokens " + str(len(tokens)))
            
            # tokens.difference_update(set(punctuation))
            # tokens.difference_update(STOP_WORDS) 
            token_str=record['value'][each_key]
            if debug:
                log(f"Matcher: tokens after removing stop words {token_str}")
            matched_ents = find_matches(" ".join(token_str).lower(), Automata)
            if debug:
                log("Matcher: length of matched_ents " + str(len(matched_ents)))
                log("Matcher: url " + str(url))
            if len(matched_ents)<1:
                if debug:
                    log("Error matching sentence "+sentence_key)
            else:
                if debug: 
                    log("Matcher: Matching sentence "+sentence_key)
                for pair in itertools.combinations(matched_ents, 2):
                    source_entity_id=pair[0][0]
                    destination_entity_id=pair[1][0]
                    label_source=pair[0][1]
                    label_destination=pair[1][1]
                    source_canonical_name=re.sub('[^A-Za-z0-9]+', ' ', str(label_source))
                    destination_canonical_name=re.sub('[^A-Za-z0-9]+', ' ', str(label_destination))
                    year=rconn.hget(f"article_id:{article_id}",'year')
                    if not year:
                        year='2021'
                    execute('XADD', 'edges_matched_%s_{%s}' % (role,shard_id), '*','source',f'{source_entity_id}','destination',f'{destination_entity_id}','source_name',source_canonical_name,'destination_name',destination_canonical_name,'rank',1,'year',year)

                    #FIXME: this breaks design pattern of NLP processing to support microservices pattern on front end
                    rconn.zincrby(f'edges_scored:{source_entity_id}:{destination_entity_id}',1, sentence_key)

            execute('SADD','processed_docs_stage3_%s_{%s}' % (role,shard_id),sentence_key)
        else:
            if debug:
                log(f"Matcher Alteady processed {sentence_key} for rol {role}")



bg = GearsBuilder('KeysReader')
bg.foreach(process_item)
bg.count()
bg.register('sentence:*',  mode="async_local",onRegistered=OnRegisteredAutomata)
