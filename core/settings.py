BOT_NAME = 'mexibot'

SPIDER_MODULES = [
    'core.spiders'
]

NEWSPIDER_MODULE = 'core.spiders'

ITEM_PIPELINES = {
    'core.pipelines.CSVPipeline': 300,
    'core.pipelines.ArticlePipeline': 400
}

DATA_DIRECTORY = "data"
ARTICLE_DIRECTORY = "articles"