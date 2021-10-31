from embedding import extractEmbeddingAction

actions = {
    'extractEmbedding': extractEmbeddingAction
}

def handler(event, context): 
    action = event['action']
    payload = event['payload']

    if action not in actions:
        return {
            'type': 'InvalidArgumentError',
            'message': 'Action not in actions'
        }

    return actions[action](payload)