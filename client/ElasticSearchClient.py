from elasticsearch import Elasticsearch

class ElasticSearch:
    def __init__(self) -> None:
        pass

    def get_client(config):
        return Elasticsearch(config)

    async def save(rows: list, index:str, client):
        if len(rows) > 0:
            body = []
            for entry in rows:
                body.append({'index': {'_index': index, '_id' : entry.date.strftime("%Y-%m-%d") +'-'+ entry.isu}})
                body.append(entry.to_dict())
            client.bulk(body=body)

