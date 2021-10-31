from embedding import extractEmbeddingAction

actions = {
    'extractEmbedding': extractEmbeddingAction
}

def handler(event, context): 
    action = event['action']
    payload = event['payload']
    return actions[action](payload)