import celery

celeryapp = celery.Celery('romanesco',
    backend='mongodb://localhost/romanesco',
    broker='mongodb://localhost/romanesco')

analysis = {
    "name": "append_tables",
    "inputs": [{"name": "a", "type": "table", "format": "objectlist"}, {"name": "b", "type": "table", "format": "objectlist"}],
    "outputs": [{"name": "c", "type": "table", "format": "objectlist"}],
    "script": "c = a + b",
    "mode": "python"
}

async_result = celeryapp.send_task("romanesco.run", [analysis], {
    "inputs": {
        "a": {"format": "objectlist", "data": [{"aa": 1, "bb": 2}]},
        "b": {"format": "objectlist", "data": [{"aa": 3, "bb": 4}]}
    },
    "outputs": {
        "c": {"format": "objectlist.json", "uri": "file://output.json"}
    }
})

print async_result.get()
