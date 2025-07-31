from src.embeddings_utils import embed_texts, search_top_k


def expand_clip(index:int, segments:list, clip_length:float = 10.0) -> list:
    """
    Expande un clip dado su índice y la duración deseada.
    """
    start = segments[index]['start']
    end = segments[index]['end']
    
    expanded_start = max(0, start - clip_length / 2)
    expanded_end = min(segments[-1]['end'], end + clip_length / 2)
    
    expanded_segments = []
    for segment in segments:
        if segment['start'] >= expanded_start and segment['end'] <= expanded_end:
            expanded_segments.append(segment)
    return expanded_segments

def search_clips(query: str, model, embeddings, segments, top_k: int = 5, clip_length: float = 10.0) -> list:

    query_embedding = embed_texts(model, [query])[0]
    results = search_top_k(query_embedding, embeddings, top_k=top_k)

    expanded_results = []
    for idx, distance in results:
        segment = segments[idx]
        expanded_segments = expand_clip(idx, segments, clip_length=clip_length)
        _expanded_result = {
            "start": min(segment['start'], expanded_segments[0]['start']),
            "end": max(segment['end'], expanded_segments[-1]['end']),
            "text": "".join([s['text'] for s in expanded_segments]),
            "score": distance
        }
        expanded_results.append(_expanded_result)

    return expanded_results
    