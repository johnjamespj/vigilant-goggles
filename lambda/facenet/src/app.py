import time
from embedding import extractEmbeddingAction
from face import getFaceAction
from compareFace import compareFaceAction

actions = {
    'extractEmbedding': extractEmbeddingAction,
    'extractFaceAction': getFaceAction,
    'compareFaces': compareFaceAction
}

def handler(event, context): 
    action = event['action']
    payload = event['payload']

    if action not in actions:
        return {
            'type': 'InvalidArgumentError',
            'message': 'Action not in actions'
        }

    start = time.process_time()
    res = actions[action](payload)
    timeTaken = time.process_time() - start

    return {
        'result': res,
        'timeTaken': timeTaken
    }