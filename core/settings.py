BOT_NAME = 'mexibot'

SPIDER_MODULES = [
    'core.spiders.oaxaca_quadratin'
]

NEWSPIDER_MODULE = 'core.spiders'

ITEM_PIPELINES = {
    'core.pipelines.CSVPipeline': 300
}

OUTPUT_DIRECTORY = "data"